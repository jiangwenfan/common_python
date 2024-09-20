import json
import sys

sys.path.append("..")
import json
import logging

from common_packages.tts import TTSMicrosoft

from .. import get_config

logging.basicConfig(level=logging.INFO)


class TestTTSMicrosoft:
    def test_tts(self):
        config: dict = get_config()
        microsoft = TTSMicrosoft(**config["tts"]["microsoft"])
        sentence_response = microsoft.speak(
            "The following quickstarts demonstrate how to create a custom Voice Assistant",
            "test.mp3",
        )
        print(sentence_response)
        # assert len(sentence_response) > 1
