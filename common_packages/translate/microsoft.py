import uuid

import requests

from common_packages.translate import LanguageCodeOfBackend, SentenceInfo, WordInfo
from common_packages.tts.microsoft import TTSMicrosoft

pos_tag_table = {
    "ADJ": ("Adjectives", "形容词"),
    "ADV": ("Adverbs", "副词"),
    "CONJ": ("Conjunctions", "连词"),
    "DET": ("Determiners", "限定词"),
    "MODAL": ("Verbs", "动词"),
    "NOUN": ("Nouns", "名词"),
    "PREP": ("Prepositions", "介词"),
    "PRON": ("Pronouns", "代词"),
    "VERB": ("Verbs", "动词"),
    "OTHER": ("Other", "其他"),
}


class TranslateMicrosoft:
    def __init__(
        self,
        text_endpoint: str,
        word_endpoint: str,
        location_region: str,
        key: str,
        tts_microsoft_config: dict,
    ):
        self.text_endpoint = text_endpoint
        self.word_endpoint = word_endpoint
        self.location_region = location_region
        self.key = key
        self.part_params = {"api-version": "3.0"}
        self.tts_microsoft_obj = TTSMicrosoft(**tts_microsoft_config)

    def _send_word_request(
        self,
        word: str,
        source_language_code: LanguageCodeOfBackend,
        target_language_code: LanguageCodeOfBackend,
    ) -> dict:
        """发送单词翻译请求
        [文档](https://learn.microsoft.com/en-us/azure/ai-services/translator/reference/v3-0-dictionary-lookup)
        [词典示例](https://learn.microsoft.com/en-us/azure/ai-services/translator/reference/v3-0-dictionary-examples)
        """
        # 1. 转换语言代码
        source_language_code = self._change_language_code(source_language_code)
        target_language_code = self._change_language_code(target_language_code)

        # 2. 构造请求查询参数: 源语言,目标语言
        params = self.part_params | {
            "from": source_language_code,
            "to": target_language_code,
        }

        # 3.1 获取 access_token
        access_token = self.tts_microsoft_obj.fetch_access_token()

        # 3. 构造请求头: key,location,content-type
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Ocp-Apim-Subscription-Key": self.key,
            "Ocp-Apim-Subscription-Region": self.location_region,
            "Content-type": "application/json",
            "X-ClientTraceId": str(uuid.uuid4()),
        }

        # 4. 构造请求体: 要翻译的word
        body = [{"Text": word}]

        # 5. 发送请求
        try:
            response = requests.post(
                self.word_endpoint, params=params, headers=headers, json=body
            )
        except Exception as e:
            _ = f"microsoft 词典翻译请求连接失败: {self.text_endpoint} {params} {headers} {body}"
            raise ValueError(_ + e)
        if response.status_code != 200:
            raise ValueError(f"microsoft 词典翻译响应错误: {response.status_code}")

        # 6.返回原生响应
        response: list[dict] = response.json()

        # 7. 断言必须只有一个翻译结果
        assert len(response) == 1, f"microsoft词典翻译响应格式错误: {response}"
        # 返回的结果
        _ = {
            # 直接翻译的结果
            "normalizedSource": "fly",
            # 润色之后的结果
            "displaySource": "fly",
            "translations": [
                {
                    # 相当于直接翻译的结果
                    "normalizedTarget": "飞",
                    # 润色之后的
                    # 以最适合最终用户显示的形式提供源术语
                    "displayTarget": "飞",
                    "posTag": "VERB",
                    # 一个介于 0.0 和 1.0 之间的值，“训练数据中的概率”
                    # 翻译的词频。保留1位,四舍五入进位。
                    # round(n*100,1)
                    "confidence": 0.2898,
                    "prefixWord": "",
                    # 单词的其他
                    "backTranslations": [
                        {
                            "normalizedText": "fly",
                            "displayText": "fly",
                            "numExamples": 15,
                            "frequencyCount": 4995,
                        },
                        {
                            "normalizedText": "flying",
                            "displayText": "flying",
                            "numExamples": 15,
                            "frequencyCount": 1931,
                        },
                        {
                            "normalizedText": "flew",
                            "displayText": "flew",
                            "numExamples": 15,
                            "frequencyCount": 968,
                        },
                    ],
                },
            ],
        }
        return response[0]

    def _send_sentence_request(
        self,
        text: str,
        source_language_code: LanguageCodeOfBackend,
        target_language_code: LanguageCodeOfBackend,
    ) -> dict:
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
            "Ocp-Apim-Subscription-Key": self.key,
            "Ocp-Apim-Subscription-Region": self.location_region,
            "Content-type": "application/json",
            "X-ClientTraceId": str(uuid.uuid4()),
        }

        # 4. 构造请求体: 要翻译的文本
        body = [{"text": text}]

        # 5. 发送请求
        try:
            response = requests.post(
                self.text_endpoint, params=params, headers=headers, json=body
            )
        except Exception as e:
            _ = f"microsoft 翻译请求连接失败: {self.text_endpoint} {params} {headers} {body}"
            raise ValueError(_ + e)
        if response.status_code != 200:
            raise ValueError(f"microsoft 翻译响应错误: {response.status_code}")

        # 6.返回原生响应
        response: list[dict] = response.json()
        assert len(response) == 1, f"microsoft翻译响应格式错误1: {response}"

        # 解析1
        response_dict: dict = response[0]
        assert "translations" in response_dict, f"microsoft翻译响应格式错误2: {response_dict}"
        _ = {
            "translations": [
                {
                    "text": "J'aimerais vraiment conduire votre voiture autour du pâté de maisons plusieurs fois!",
                    "to": "fr",
                },
            ]
        }

        # 2. 解析原生响应
        response_dict2: list[dict] = response_dict["translations"]
        assert len(response_dict2) == 1, f"microsoft翻译响应格式错误3: {response_dict2}"
        _ = [
            {
                "text": "J'aimerais vraiment conduire votre voiture autour du pâté de maisons plusieurs fois!",
                "to": "fr",
            },
        ]

        # 3. 返回结果
        res: dict = response_dict2[0]
        _ = (
            {
                "text": "J'aimerais vraiment conduire votre voiture autour du pâté de maisons plusieurs fois!",
                "to": "fr",
            },
        )
        return res

    def _send_tts_request(self, text: str, _text_language_code: str) -> bytes:
        """发送tts请求
        # HACK 当前只能生成英文的音频
        """
        wav_data = self.tts_microsoft_obj.convert_text_to_speech(text)
        return wav_data

    @staticmethod
    def _change_language_code(language_code_of_backend: LanguageCodeOfBackend) -> str:
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

    @staticmethod
    def _change_pos_tag(pos_tag: str) -> str:
        """将microsft的词性标签转换为人类可读的词性标签"""

        # 将此术语与词性标签关联的字符串
        if pos_tag not in pos_tag_table:
            raise ValueError(f"microsoft不支持的词性标签: {pos_tag}")
        return pos_tag_table[pos_tag]

    @staticmethod
    def _change_frequency(self, frequency: float) -> float:
        """将microsoft的词频转换为人类可读的词频"""
        return round(frequency * 100, 1)

    @staticmethod
    def _sort_shapes(self, raw_shapes: list[dict]) -> list[dict]:
        """对单词的其他形式进行排序.从大到小"""
        return sorted(
            raw_shapes, key=lambda shape: shape["frequencyCount"], reverse=True
        )

    def translate_word(
        self,
        word: str,
        source_language_code: LanguageCodeOfBackend,
        target_language_code: LanguageCodeOfBackend,
    ) -> dict:
        """翻译word,使用字典接口查询"""
        # 1. 获取sentence原生响应
        raw_response: dict = self._send_word_request(
            word, source_language_code, target_language_code
        )
        normalized_word = raw_response["normalizedSource"]

        # 2. 获取word的tts结果
        word_audio: bytes = self._send_tts_request(normalized_word, None)
        # 补充word单词发音
        raw_response["audio_data"] = word_audio

        # 返回最终结果
        return raw_response

    def translate_sentence(
        self,
        text: str,
        source_language_code: LanguageCodeOfBackend,
        target_language_code: LanguageCodeOfBackend,
    ) -> dict:
        """翻译句子,使用文本翻译接口查询
        返回:
            {
                "text":"xxx",
                "to":"xxx",
                "audio_data": bytes
            }
        """

        # 1. 获取sentence原生响应
        # text 是翻译后的文本, to 是目标语言代码
        raw_result: dict = self._send_sentence_request(
            text, source_language_code, target_language_code
        )

        # 2.1 获取text的tts结果
        text_audio: bytes = self._send_tts_request(text, None)
        # 2.2 增加text的发音
        raw_result["audio_data"] = text_audio

        # 3. 增加原始文本
        raw_result["sentence"] = text

        return raw_result

    @classmethod
    def format_word_response(cls, response: dict) -> WordInfo:
        """将相应结果处理为了WordInfo"""
        normalized_word = response["normalizedSource"]
        display_word = response["displaySource"]

        # 所有变体.
        _ = {
            "normalizedText": "fly",
            "displayText": "fly",
            "numExamples": 15,
            "frequencyCount": 4995,
        }
        raw_shapes: list[dict] = []

        # 翻译结果
        translations: list[dict] = []

        all_raw_translations: list[dict] = response["translations"]
        for raw_translation in all_raw_translations:
            # 添加翻译
            item = {
                "normalized": raw_translation["normalizedTarget"],
                "display": raw_translation["displayTarget"],
                "pos_tag": cls._change_pos_tag(raw_translation["posTag"]),
                "frequency": cls._change_frequency(raw_translation["confidence"]),
            }
            translations.append(item)

            # 其他变体
            shape = raw_translation["backTranslations"]
            raw_shapes.extend(shape)

        # 单词其他形式.变体排序
        sorted_shapes = cls._sort_shapes(raw_shapes)

        res = {
            "normalized_word": normalized_word,
            "display_word": display_word,
            "translation": translations,
            "shapes": sorted_shapes,
            "audio_data": response["audio_data"],
            "extended_info": {},
        }
        return res

    @classmethod
    def format_sentence_response(cls, response: dict) -> SentenceInfo:
        """将相应结果处理为了SentenceInfo"""
        sentence = response["sentence"]
        translation = [response["text"]]
        audio_data = response["audio_data"]

        res = {
            "sentence": sentence,
            "translation": translation,
            "audio_data": audio_data,
        }
        return res
