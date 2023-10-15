from common_packages.utils.utils import calculate_relative_value

from . import get_config


def test_calculate_relative_value():
    res = calculate_relative_value(
        input_data=[1, 2, 3, 4, 5], db_data=[3, 4, 5, 6, 7, 8]
    )
    print(res)


test_calculate_relative_value()
