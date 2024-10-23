import requests


class SearchLocationAmap:
    """高德地图API搜索地理位置
    - 使用2.0版本的API
    """

    def __init__(self, key: str):
        self.key = key
        self.base_url = "https://restapi.amap.com/v3/config/district"
