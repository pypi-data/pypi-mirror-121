import logging

from urllib.parse import quote
from dataclasses import dataclass

from gordo_dataset.file_system import FileSystem
from gordo_dataset.sensor_tag import SensorTag, extract_tag_name
from gordo_dataset.exceptions import ConfigException
from gordo_dataset.assets_config import AssetsConfig, PathSpec
from .file_type import FileType
from .ncs_file_type import NcsFileType, load_ncs_file_types
from .constants import DEFAULT_MAX_FILE_SIZE
from .partition import Partition, YearPartition

from typing import (
    List,
    Iterable,
    Tuple,
    Optional,
    Dict,
    Iterator,
    Union,
    Set,
    TypeVar,
    cast,
)
from collections import defaultdict, OrderedDict
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass(frozen=True)
class Location:
    """
    Represents location of the tag in the data lake
    """

    path: str
    file_type: FileType
    partition: Optional[Partition] = None


@dataclass(frozen=True)
class TagLocations:
    """
    Locations of the tags for each partition
    """

    orig_tag: Union[str, SensorTag]
    tag: Optional[SensorTag] = None
    locations: Optional[Dict[Partition, Location]] = None

    @property
    def tag_name(self):
        return extract_tag_name(self.orig_tag)

    def available(self) -> bool:
        return self.tag is not None and self.locations is not None

    def partitions(self) -> List[Partition]:
        if not self.available():
            return []
        return sorted(cast(Dict[Partition, Location], self.locations).keys())

    def get_location(self, partition: Union[int, Partition]) -> Optional[Location]:
        curr_partition: Partition = cast(Partition, partition)
        if type(partition) is int:
            curr_partition = YearPartition(cast(int, partition))
        if not self.available():
            return None
        return cast(Dict[Partition, Location], self.locations).get(curr_partition)

    def __iter__(self) -> Iterator[Tuple[SensorTag, Partition, Location]]:
        if self.available():
            locations = cast(Dict[Partition, Location], self.locations)
            for partition in self.partitions():
                yield cast(SensorTag, self.tag), cast(Partition, partition), locations[
                    partition
                ]


PathSpecWithTag = Tuple[PathSpec, Union[str, SensorTag]]


TAG_DIRS_OPTIONAL_SUFFIXES = "."


class NcsLookup:
    """
    Class which could be used for finding tags data in the data lake storage
    """

    @classmethod
    def create(
        cls,
        storage: FileSystem,
        ncs_type_names: Optional[Iterable[str]] = None,
        storage_name: Optional[str] = None,
        max_file_size: Optional[int] = DEFAULT_MAX_FILE_SIZE,
    ) -> "NcsLookup":
        ncs_file_types = load_ncs_file_types(ncs_type_names)
        return cls(storage, ncs_file_types, storage_name, max_file_size=max_file_size)

    def __init__(
        self,
        storage: FileSystem,
        ncs_file_types: List[NcsFileType],
        storage_name: Optional[str] = None,
        max_file_size: Optional[int] = DEFAULT_MAX_FILE_SIZE,
    ):
        self.storage = storage
        self.ncs_file_types = ncs_file_types
        if storage_name is None:
            storage_name = storage.name
        self.storage_name = storage_name
        self.max_file_size = max_file_size

    @staticmethod
    def quote_tag_name(tag_name: str) -> str:
        return quote(tag_name, safe=" ")

    @staticmethod
    def _validate_tag_equality(
        tag1: Union[str, SensorTag], tag2: Union[str, SensorTag]
    ):
        # TODO better docstring
        type_tag1, type_tag2 = type(tag1), type(tag2)
        if type_tag1 is SensorTag and type_tag2 is SensorTag:
            if cast(SensorTag, tag1).asset != cast(SensorTag, tag2).asset:
                raise ValueError(
                    "Tags %s and %s with the same name but different assets"
                    % (repr(tag1), repr(tag2))
                )
        for _type in (str, SensorTag):
            if type_tag1 is _type:
                if type_tag2 is not _type:
                    tag_name1 = extract_tag_name(tag1)
                    tag_name2 = extract_tag_name(tag2)
                    if tag_name1 == tag_name2:
                        raise ValueError(
                            "Tags %s and %s has different type but the same name"
                            % (repr(tag1), repr(tag2))
                        )

    def tag_dirs_lookup(
        self, specs: List[PathSpecWithTag]
    ) -> Iterable[Tuple[str, Optional[Tuple[str, SensorTag]]]]:
        # TODO better docstring
        # TODO split this method
        """
        Takes list of tags and find directories related to them in the data lake storage

        Parameters
        ----------
        specs: List[Tuple[PathSpec, Union[str, SensorTag]]]

        Returns
        -------

        """
        storage = self.storage
        path_tag_and_specs: Dict[str, Dict[str, PathSpecWithTag]] = {}
        tag_paths: Dict[str, Set[str]] = defaultdict(set)
        unique_tags: Dict[str, Union[str, SensorTag]] = {}
        for path_spec, tag in specs:
            base_dir = path_spec.full_path(storage)
            if base_dir not in path_tag_and_specs:
                path_tag_and_specs[base_dir] = {}
            tag_and_spec = path_tag_and_specs[base_dir]
            tag_name_orig: str = extract_tag_name(tag)
            if tag_name_orig in unique_tags:
                self._validate_tag_equality(tag, unique_tags[tag_name_orig])
            else:
                unique_tags[tag_name_orig] = tag
            tag_name = self.quote_tag_name(tag_name_orig).upper()
            if tag_name in tag_and_spec:
                raise ValueError(
                    "Found duplicate for tag '%s' in '%s' with spec '%s'"
                    % (tag_name_orig, base_dir, tag_and_spec[tag_name])
                )
            tag_and_spec[tag_name] = (path_spec, tag)
            tag_paths[tag_name].add(base_dir)

        found_tags: Dict[str, Dict[str, Optional[Tuple[str, PathSpecWithTag]]]] = {
            tag_name: OrderedDict() for tag_name in tag_paths.keys()
        }

        def check_if_tag_already_found(
            check_tag_name: str,
        ) -> Optional[Tuple[str, Optional[Tuple[str, SensorTag]]]]:
            if check_tag_name not in tag_paths:
                return None
            if len(found_tags[tag_name]) == len(tag_paths[tag_name]):
                _, orig_tag = tag_and_specs[tag_name]
                orig_tag_name = extract_tag_name(orig_tag)
                for path_spec_with_tag in found_tags[tag_name].values():
                    if path_spec_with_tag is not None:
                        found_path, (found_path_spec, found_tag) = path_spec_with_tag
                        sensor_tag = self._normalize_tag(
                            found_tag, found_path_spec.asset
                        )
                        return orig_tag_name, (found_path, sensor_tag)
                return orig_tag_name, None
            return None

        for base_dir, tag_and_specs in path_tag_and_specs.items():
            for path, file_info in self.storage.ls(base_dir):
                if file_info is not None and file_info.isdir():
                    dir_path, file_name = self.storage.split(path)
                    file_tag_name = file_name.upper()
                    found_tag_name: Optional[str] = None
                    if file_tag_name in tag_and_specs:
                        found_tag_name = file_tag_name
                    else:
                        for tag_suffix in TAG_DIRS_OPTIONAL_SUFFIXES:
                            if file_tag_name + tag_suffix in tag_and_specs:
                                found_tag_name = file_tag_name + tag_suffix
                                break
                    if found_tag_name is not None:
                        if base_dir in found_tags[found_tag_name]:
                            logger.error(
                                "Found duplicate tag dir '%s' in '%s'",
                                found_tag_name,
                                base_dir,
                            )
                            continue
                        found_tags[found_tag_name][base_dir] = (
                            path,
                            tag_and_specs[found_tag_name],
                        )
                        result = check_if_tag_already_found(found_tag_name)
                        if result is not None:
                            yield result
                            del tag_paths[found_tag_name]
            for tag_name, tag_path_specs in tag_and_specs.items():
                if base_dir not in found_tags[tag_name]:
                    found_tags[tag_name][base_dir] = None
                result = check_if_tag_already_found(tag_name)
                if result is not None:
                    yield result
                    del tag_paths[tag_name]

    def _validate_file(self, full_path: str):
        storage = self.storage
        if self.max_file_size is not None:
            file_info = storage.info(full_path)
            if file_info.size > self.max_file_size:
                logger.debug(
                    "Size of file '%s' is %d bytes that bigger than the maximum file size %d bytes"
                    % (full_path, file_info.size, self.max_file_size)
                )
                return False
        return True

    def files_lookup(
        self,
        tag_dir: str,
        tag: SensorTag,
        partitions: Iterable[Partition],
        orig_tag: Optional[Union[str, SensorTag]] = None,
    ) -> TagLocations:
        """
        Finds files (possible parquet or CSV) in tag directory in the data lake storage

        Parameters
        ----------
        tag_dir: str
        tag: SensorTag
        partitions: Iterable[Partition]
            List of partitions for finding files
        orig_tag: Union[str, SensorTag]

        Returns
        -------
        TagLocations

        """
        storage = self.storage
        ncs_file_types = self.ncs_file_types
        tag_name = self.quote_tag_name(tag.name)
        locations = {}
        for partition in partitions:
            found = False
            for ncs_file_type in ncs_file_types:
                if ncs_file_type.check_partition(partition):
                    for path_partition, full_path in ncs_file_type.paths(
                        storage, tag_dir, tag_name, [partition]
                    ):
                        if storage.exists(full_path) and self._validate_file(full_path):
                            file_type = ncs_file_type.file_type
                            locations[partition] = Location(
                                full_path, file_type, path_partition
                            )
                            found = True
                            break
                    if found:
                        break
        orig_tag = tag if orig_tag is None else orig_tag
        return TagLocations(
            orig_tag=orig_tag, tag=tag, locations=locations if locations else None
        )

    @staticmethod
    def _normalize_tag(tag: Union[str, SensorTag], asset: Optional[str] = None):
        if type(tag) is str:
            if asset is None:
                raise ConfigException("asset should be specified along with base_name")
            return SensorTag(tag, asset)
        return tag

    def assets_config_tags_lookup(
        self,
        asset_config: AssetsConfig,
        tags: List[Union[str, SensorTag]],
        base_dir: Optional[str] = None,
        asset: Optional[str] = None,
    ) -> Iterable[Tuple[str, Optional[Tuple[str, SensorTag]]]]:
        # TODO better docstring
        """
        Takes assets paths from ``AssetsConfig`` and find tag paths in the data lake storage

        Parameters
        ----------
        asset_config: AssetsConfig
        tags: List[Union[str, SensorTag]]
        base_dir: Optional[str]
        asset: Optional[str]

        Returns
        -------

        """
        storage = self.storage
        storage_name = storage.name
        specs: List[PathSpecWithTag] = []
        if not base_dir:
            for tag in tags:
                tag_name: str
                if type(tag) is SensorTag:
                    sensor_tag = cast(SensorTag, tag)
                    tag_name = sensor_tag.name
                    asset = sensor_tag.asset
                else:
                    tag_name = cast(str, tag)
                path_specs = asset_config.get_paths(storage_name, tag_name, asset)
                if not path_specs:
                    raise ValueError(
                        "Cant find tag '%s' in storage '%s'", tag_name, storage_name
                    )
                for path_spec in path_specs:
                    specs.append((path_spec, tag))
        else:
            path_spec = PathSpec(cast(str, asset), base_dir, "")
            for tag in tags:
                sensor_tag = self._normalize_tag(tag, asset)
                specs.append((path_spec, sensor_tag))
        yield from self.tag_dirs_lookup(specs)

    def _thread_pool_lookup_mapper(
        self,
        tag_lookup: Tuple[str, Optional[Tuple[str, SensorTag]]],
        partitions: List[Partition],
        tag_by_name: Dict[str, Union[str, SensorTag]],
    ) -> TagLocations:
        tag_name, tag_with_path = tag_lookup
        orig_tag = tag_by_name.get(tag_name, tag_name)
        if tag_with_path is not None:
            tag_dir, tag = tag_with_path
            return self.files_lookup(tag_dir, tag, partitions, orig_tag=orig_tag)
        else:
            return TagLocations(orig_tag)

    @staticmethod
    def _inf_iterator(v: T) -> Iterable[T]:
        while True:
            yield v

    @classmethod
    def _tags_by_names(
        cls, tags: List[Union[str, SensorTag]]
    ) -> Dict[str, Union[str, SensorTag]]:
        orig_tags: Dict[str, Union[str, SensorTag]] = {}
        for tag in tags:
            tag_name = extract_tag_name(tag)
            if tag_name in orig_tags:
                cls._validate_tag_equality(tag, orig_tags[tag_name])
            else:
                orig_tags[tag_name] = tag
        return orig_tags

    def lookup(
        self,
        asset_config: AssetsConfig,
        tags: List[Union[str, SensorTag]],
        partitions: Iterable[Partition],
        threads_count: int = 1,
        base_dir: Optional[str] = None,
        asset: Optional[str] = None,
    ) -> Iterable[TagLocations]:
        """
        Takes assets paths from ``AssetsConfig`` and find tags files paths in the data lake storage

        Parameters
        ----------
        asset_config: AssetsConfig
        tags: List[SensorTag]
        partitions: Iterable[Partition]
        threads_count: int
            Number of threads for internal `ThreadPool`. Do not uses thread pool if 1
        base_dir: Optional[str]
        asset: Optional[str]
            Should be specified when base_dir is not None

        Returns
        -------

        """
        if not threads_count or threads_count < 1:
            raise ConfigException("thread_count should bigger or equal to 1")
        multi_thread = threads_count > 1

        tag_by_names = self._tags_by_names(tags)
        tag_lookups = self.assets_config_tags_lookup(
            asset_config, tags, base_dir=base_dir, asset=asset
        )
        partitions_tuple = tuple(partitions)
        if multi_thread:
            with ThreadPoolExecutor(max_workers=threads_count) as executor:
                result = executor.map(
                    self._thread_pool_lookup_mapper,
                    tag_lookups,
                    self._inf_iterator(partitions_tuple),
                    self._inf_iterator(tag_by_names),
                )
                for tag_locations in result:
                    yield tag_locations
        else:
            for tag_name, path_with_tag in tag_lookups:
                orig_tag = tag_by_names.get(tag_name, tag_name)
                if path_with_tag is not None:
                    tag_dir, tag = path_with_tag
                    yield self.files_lookup(
                        tag_dir, tag, partitions_tuple, orig_tag=orig_tag
                    )
                else:
                    yield TagLocations(orig_tag)
