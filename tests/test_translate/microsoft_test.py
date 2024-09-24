class TestMicrosoft:
    def test__change_language_code(self, translate_microsoft_obj):
        assert translate_microsoft_obj._change_language_code("zh-CN") == "zh-Hans"
        assert translate_microsoft_obj._change_language_code("en") == "en"

    def test___send_tts_request(self, translate_microsoft_obj):
        wav_data = translate_microsoft_obj._send_tts_request("hello world", "en")
        # print(wav_data, type(wav_data))
        assert isinstance(wav_data, bytes)
        assert len(wav_data) > 100

    def test__send_word_request(self, translate_microsoft_obj):
        res = translate_microsoft_obj._send_word_request("fly", "en", "zh-CN")
        print(res, type(res))
        # _ = [{"translations": [{"text": "你好", "to": "zh-Hans"}]}]
        # assert isinstance(res, list)
        # assert len(res) == 1
        # assert isinstance(res[0], dict)
        # assert "translations" in res[0]
        # translations = res[0]["translations"]
        # assert isinstance(translations, list)
        # assert len(translations) == 1
        # assert isinstance(translations[0], dict)
        # assert "text" in translations[0]
        # assert "to" in translations[0]
        # print(res, type(res))

    def test__send_sentence_request(self, translate_microsoft_obj):
        res = translate_microsoft_obj._send_sentence_request(
            "I would really like to drive your car around the block several times!",
            "en",
            "zh-CN",
        )
        _ = [{"translations": [{"text": "我真的很想开着你的车绕着街区转好几圈！", "to": "zh-Hans"}]}]
        assert isinstance(res, list)
        assert len(res) == 1
        assert isinstance(res[0], dict)
        assert "translations" in res[0]
        translations = res[0]["translations"]
        assert isinstance(translations, list)
        assert len(translations) == 1
        assert isinstance(translations[0], dict)
        assert "text" in translations[0]
        assert "to" in translations[0]
        # print(res, type(res))

    # def test_translate_word(): ...

    # def test_translate_sentence(): ...

    # def test_format_word_response(): ...

    # def test_format_sentence_response(): ...

    # def test_download_audio_file(): ...
