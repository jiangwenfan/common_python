import pytest

from common_packages.translate.microsoft import TranslateMicrosoft

# from common_packages.translate.youdao import YoudaoTranslate

# @pytest.fixture(scope="class")
# def youdao_op(global_config):
#     """用于在`每个测试用例`中初始化有道翻译对象"""
#     config: dict = global_config()
#     youdao = YoudaoTranslate(**config["translate"]["youdao"])


@pytest.fixture(scope="class")
def translate_microsoft_obj(global_config):
    """用于在`每个测试用例`中初始化微软翻译对象"""
    config: dict = global_config["translate"]["microsoft"]
    tts_microsoft_config = global_config["tts"]["microsoft"]
    microsoft_obj = TranslateMicrosoft(
        **config, tts_microsoft_config=tts_microsoft_config
    )
    return microsoft_obj
