from typing import Iterable, Set, Optional, Dict, cast, List

from .assets_config import AssetsConfig
from .resource_assets_config import LEGACY_DEFAULT_STORAGE

from .sensor_tag import (
    tag_to_json,
    extract_tag_name,
    Tag,
    SensorTag,
    normalize_sensor_tag,
    legacy_normalize_sensor_tag,
    load_sensor_tag,
)


def tags_to_json_representation(tags: Iterable[Tag]) -> dict:
    tags_metadata = {}
    for tag in tags:
        tag_name = extract_tag_name(tag)
        json_repr = tag_to_json(tag)
        if type(json_repr) is str:
            continue
        tags_metadata[tag_name] = json_repr
    return tags_metadata


def _get_dataset_meta(build_metadata: dict) -> Optional[dict]:
    if "dataset" in build_metadata:
        if "dataset_meta" in build_metadata["dataset"]:
            return build_metadata["dataset"]["dataset_meta"]
    return None


def _tags_from_build_metadata(build_metadata: dict) -> Optional[dict]:
    dataset_meta = _get_dataset_meta(build_metadata)
    if dataset_meta is not None:
        if "tag_loading_metadata" in dataset_meta:
            tag_loading_metadata = dataset_meta["tag_loading_metadata"]
            return tag_loading_metadata.get("tags")
    return None


def _storage_from_build_metadata(build_metadata: dict) -> Optional[str]:
    dataset_meta = _get_dataset_meta(build_metadata)
    if dataset_meta is not None:
        if "data_provider" in dataset_meta:
            provider_metadata = dataset_meta["data_provider"]
            return provider_metadata.get("storage_name")
    return None


_list_of_tags_exception_message = (
    "The list of tags should be placed on"
    " dataset.dataset_meta.tag_loading_metadata.tags path"
)


def sensor_tags_from_build_metadata(
    build_metadata: dict,
    tag_names: Set[str],
    *,
    with_legacy_tag_normalization: bool = True,
    assets_config: Optional[AssetsConfig] = None,
    storage: Optional[str] = None,
    asset: Optional[str] = None,
) -> Dict[str, SensorTag]:
    # TODO better docstring
    # TODO unit-tests
    if with_legacy_tag_normalization:
        if assets_config is None:
            raise ValueError(
                "assets_config should be provided with_legacy_tag_normalization"
            )
    tags_build_metadata = _tags_from_build_metadata(build_metadata)
    sensor_tags: Dict[str, SensorTag] = {}
    if tags_build_metadata is None:
        if with_legacy_tag_normalization:
            tag_list = cast(List[Tag], list(tag_names))
            for tag in tag_list:
                curr_assets_config = cast(AssetsConfig, assets_config)
                if storage is None:
                    storage = _storage_from_build_metadata(build_metadata)
                curr_storage: str = (
                    storage if storage is not None else LEGACY_DEFAULT_STORAGE
                )
                sensor = normalize_sensor_tag(curr_assets_config, tag, asset=asset)
                sensor_tag = legacy_normalize_sensor_tag(
                    curr_assets_config, curr_storage, sensor
                )
                sensor_tags[extract_tag_name(sensor_tag)] = sensor_tag
            return sensor_tags
        raise ValueError(
            "Unable to find tags information in build_metadata. "
            + _list_of_tags_exception_message
        )
    for tag_name in tag_names:
        if tag_name not in tags_build_metadata:
            raise ValueError(
                "Unable to find tag '%s' information in build_metadata. "
                + _list_of_tags_exception_message
            )
        tag_metadata = tags_build_metadata[tag_name]
        sensor_tag = load_sensor_tag(tag_metadata)
        sensor_tags[sensor_tag.name] = sensor_tag
    return sensor_tags
