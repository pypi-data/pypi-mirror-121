import inject

from gordo_dataset.assets_config import AssetsConfig
from gordo_dataset.resource_assets_config import load_assets_config


def config(binder: inject.Binder):
    binder.bind(AssetsConfig, load_assets_config())


def configure_once():
    inject.configure_once(config)
