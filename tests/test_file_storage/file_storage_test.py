import sys

sys.path.append("..")
from common_packages.file_storage import LocalStorage, TencentCos
from common_packages.utils import image_utils

from .. import get_config


class TestLocalStorage:
    def test_save_file(self):
        config: dict = get_config()
        content: bytes = "abc测试123!@!@".encode()
        local = LocalStorage(**config["storage"]["local"])
        status, file_path = local.save("test_save_file.txt", content)
        assert status == True
        assert (
            file_path
            == f'{config["storage"]["local"]["storage_home_dir"]}test_save_file.txt'
        )

    def test_load_file(self):
        config: dict = get_config()
        local = LocalStorage(**config["storage"]["local"])
        status, content = local.load("test_save_file.txt")
        assert status == True
        assert content == "abc测试123!@!@".encode()

    def test_save_image(self):
        config: dict = get_config()
        image: bytes = image_utils.create_image(100, 100, (255, 255, 255))
        local = LocalStorage(**config["storage"]["local"])
        status, file_path = local.save("test_save_image.png", image)
        assert status == True
        assert (
            file_path
            == f'{config["storage"]["local"]["storage_home_dir"]}test_save_image.png'
        )

    def test_load_image(self):
        config: dict = get_config()
        local = LocalStorage(**config["storage"]["local"])
        status, content = local.load("test_save_image.png")
        assert status == True
        assert content == image_utils.create_image(100, 100, (255, 255, 255))


class TestTencentCosStorage:
    def test_save_image(self):
        config: dict = get_config()
        bucket = config["storage"]["tencent_cos"]["bucket"]
        region = config["storage"]["tencent_cos"]["region"]
        secret_key = config["storage"]["tencent_cos"]["secret_key"]
        secret_id = config["storage"]["tencent_cos"]["secret_id"]
        tencent_cos = TencentCos(
            bucket=bucket, region=region, secret_key=secret_key, secret_id=secret_id
        )
        tencent_cos = TencentCos(
            bucket=bucket, region=region, secret_key=secret_key, secret_id=secret_id
        )
        image: bytes = image_utils.create_image(100, 100, (255, 255, 255))
        status, file_name = tencent_cos.save(
            filename="cos_save_image.png", content=image
        )
        assert status == True
        assert file_name == "cos_save_image.png"

    def test_load_image(self):
        config: dict = get_config()
        bucket = config["storage"]["tencent_cos"]["bucket"]
        region = config["storage"]["tencent_cos"]["region"]
        secret_key = config["storage"]["tencent_cos"]["secret_key"]
        secret_id = config["storage"]["tencent_cos"]["secret_id"]
        tencent_cos = TencentCos(
            bucket=bucket, region=region, secret_key=secret_key, secret_id=secret_id
        )
        key = "cos_save_image.png"
        status, content = tencent_cos.load(key)
        assert status == True
        assert content == image_utils.create_image(100, 100, (255, 255, 255))
