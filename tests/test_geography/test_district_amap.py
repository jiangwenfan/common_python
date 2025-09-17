class TestChinaDistrictAmap:
    def test_get_privince(self, china_district_amap):
        privinces = china_district_amap.get_privince()
        # 1. 断言外层list结构
        assert isinstance(privinces, list) is True
        # 断言全国有34个省级行政区
        assert len(privinces) == 34
        # 2. 断言内层dict结构
        privince = privinces[0]
        assert isinstance(privince, dict) is True
        assert len(privince["adcode"]) > 0
        assert len(privince["name"]) > 0
        assert privince["level"] == "province"

    def test_get_city(self, china_district_amap):
        provinces = [
            {"name": "河南省", "adcode": "410000"},
            {"name": "四川省", "adcode": "510000"},
        ]
        for province in provinces:
            city_info = china_district_amap.get_city(
                province["name"], province["adcode"]
            )
            # 1. 断言外层list结构
            assert isinstance(city_info, list) is True
            # 2. 断言内层dict结构
            city = city_info[0]
            assert isinstance(city, dict) is True
            assert len(city["citycode"]) > 0
            assert len(city["adcode"]) > 0
            assert len(city["name"]) > 0
            assert city["level"] == "city"

    def test_get_district(self, china_district_amap):
        cities = [
            # 河南省洛阳市
            {"name": "洛阳市", "code": "0379", "adcode": "410300"},
            # 辽宁省鞍山市
            {"name": "鞍山市", "code": "0412", "adcode": "210300"},
            # 青海省海西蒙古族藏族自治州
            {"name": "海西蒙古族藏族自治州", "code": "0977", "adcode": "632800"},
        ]
        for city in cities:
            district_info = china_district_amap.get_district(
                city["name"], city["code"], city["adcode"]
            )
            # 1. 断言外层list结构
            assert isinstance(district_info, list) is True
            # 2. 断言内层dict结构
            district = district_info[0]
            assert isinstance(district, dict) is True
            assert len(district["adcode"]) > 0
            assert len(district["name"]) > 0
            assert district["level"] == "district"
