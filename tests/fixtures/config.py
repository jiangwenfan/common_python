import tomllib

import pytest


@pytest.fixture
def global_config():
    """获取配置文件"""
    # TODO validate config

    # read config
    with open("tests/secret.toml", "rb") as f:
        try:
            config: dict = tomllib.load(f)
        except Exception as e:
            raise f"load config failed, error: {e}"
    return config
