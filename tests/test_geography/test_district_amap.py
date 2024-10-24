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
        privince_name = "河南省"
        privince_adcode = "410000"
        city_info = china_district_amap.get_city(privince_name, privince_adcode)
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
        city_name = "洛阳市"
        city_code = "0379"
        city_adcode = "410300"
        district_info = china_district_amap.get_district(
            city_name, city_code, city_adcode
        )
        # 1. 断言外层list结构
        assert isinstance(district_info, list) is True
        # 2. 断言内层dict结构
        district = district_info[0]
        assert isinstance(district, dict) is True
        assert len(district["adcode"]) > 0
        assert len(district["name"]) > 0
        assert district["level"] == "district"
