from common_packages.translate import SentenceInfo, Translate, WordInfo
from typing import Literal
import requests, uuid, json

LanguageCodeOfBackend = Literal["zh-CN", "zh-TW", "en", "fr", "ja", "de", "es", "ko"]


class MicrosoftTranslate(Translate):
    def __init__(self, subscription_key, endpoint):
        self.endpoint = "https://api.cognitive.microsofttranslator.com/translate"
        self.key = "<your-translator-key>"
        self.location = "<YOUR-RESOURCE-LOCATION>"
        self.part_params = {"api-version": "3.0"}

    def _send_word_request(self):
        """发送单词翻译请求"""
        ...

    def _send_sentence_request(
        self,
        text: str,
        source_language_code: LanguageCodeOfBackend,
        target_language_code: LanguageCodeOfBackend,
    ):
        """发送句子翻译请求\n
        [文本翻译接口](https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation-overview)
        """
        # 1. 转换语言代码
        source_language_code = self._change_language_code(source_language_code)
        target_language_code = self._change_language_code(target_language_code)

        # 2. 构造请求查询参数: 源语言,目标语言
        params = self.part_params | {
            "from": source_language_code,
            "to": target_language_code,
        }

        # 3. 构造请求头: key,location,content-type
        headers = {
            "Ocp-Apim-Subscription-Key": key,
            # location required if you're using a multi-service or regional (not global) resource.
            "Ocp-Apim-Subscription-Region": location,
            "Content-type": "application/json",
            "X-ClientTraceId": str(uuid.uuid4()),
        }

        # 4. 构造请求体: 要翻译的文本
        body = [{"text": text}]

        # 5. 发送请求
        try:
            response = requests.post(
                self.endpoint, params=params, headers=headers, json=body
            )
        except Exception as e:
            _ = f"microsoft 翻译请求连接失败: {self.endpoint} {params} {headers} {body}"
            raise ValueError(_ + e)
        if response.status_code != 200:
            raise ValueError(f"microsoft 翻译响应错误: {response.status_code}")

        # 6.返回原生响应
        response = response.json()
        return response

    def _send_tts_request(self, text: str, target_language_code: LanguageCodeOfBackend):
        """发送tts请求"""
        ...

    def _change_language_code(
        self, language_code_of_backend: LanguageCodeOfBackend
    ) -> str:
        """转换语言代码,将language_backend后端的语言代码转换为microsoft的语言代码
        [microsoft支持的语言](https://learn.microsoft.com/en-us/azure/ai-services/translator/reference/v3-0-languages)
        """
        match language_code_of_backend:
            case "zh-CN":
                # 简体中文. 将后端的`zh-CN`转换为微软`zh-Hans`
                return "zh-Hans"
            case "zh-TW":
                # 繁体中文. 将后端的`zh-TW`转换为微软`zh-Hant`
                return "zh-Hant"
            case "en" | "ja":
                # en: 英语, ja: 日语 等，不需要转换
                return language_code_of_backend
            case _:
                raise ValueError(f"microsoft不支持的语言代码: {language_code_of_backend}")

    def translate_word(
        self,
        word: str,
        source_language_code: LanguageCodeOfBackend,
        target_language_code: LanguageCodeOfBackend,
    ) -> dict:
        """翻译word,使用字典接口查询"""

    def translate_sentence(
        self,
        text: str,
        source_language_code: LanguageCodeOfBackend,
        target_language_code: LanguageCodeOfBackend,
    ):
        """翻译句子,使用文本翻译接口查询"""
        _ = [
            {
                "translations": [
                    {
                        "text": "J'aimerais vraiment conduire votre voiture autour du pâté de maisons plusieurs fois!",
                        "to": "fr",
                    },
                ]
            }
        ]
        # 1. 获取sentence原生响应
        raw_response = self._send_sentence_request(
            text, source_language_code, target_language_code
        )
        # 2. 解析原生响应
        raw_result: list[dict] = raw_response[0]["translations"]
        assert len(raw_result) == 1, f"microsoft翻译响应格式错误: {raw_response}"
        # text 是翻译后的文本, to 是目标语言代码
        raw_result: dict = raw_result[0]

        # TODO 获取tts结果

        # 4. 合并结果返回

        print(raw_response)

    @classmethod
    def format_word_response(cls, response: dict) -> WordInfo:
        """将相应结果处理为了WordInfo"""
        pass

    @classmethod
    def format_sentence_response(cls, response: dict) -> SentenceInfo:
        """将相应结果处理为了SentenceInfo"""
        pass

    @classmethod
    def download_audio_file(cls, url: str) -> bytes:
        """下载音频文件"""
        pass
