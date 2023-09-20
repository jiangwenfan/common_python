import tomllib

import pytest


# TODO test perf
def get_config():
    # TODO validate config

    # read config
    with open("./secret.toml","rb") as f:
        try:
            config: dict = tomllib.load(f)
        except Exception as e:
            raise f"load config failed, error: {e}"
    return config
