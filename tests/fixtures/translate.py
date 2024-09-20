import pytest

from common_packages.translate.youdao import YoudaoTranslate
from common_packages.translate.microsoft import MicrosoftTranslate


@pytest.fixture(scope="function")
def youdao_op(global_config):
    """用于在`每个测试用例`中初始化有道翻译对象"""
    config: dict = global_config()
    youdao = YoudaoTranslate(**config["translate"]["youdao"])


@pytest.fixture(scope="function")
def microsoft_op(global_config):
    """用于在`每个测试用例`中初始化微软翻译对象"""
    config: dict = global_config()
    microsoft = MicrosoftTranslate(**config["translate"]["microsoft"])
