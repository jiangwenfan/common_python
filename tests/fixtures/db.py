import pytest

from common_packages.db_utils.mysql import MysqlOperator


@pytest.fixture
def mysql_op(global_config):
    mysql_config: dict = global_config["db"]["mysql"]
    mysql_op = MysqlOperator(**mysql_config)

    return mysql_op


@pytest.fixture
def clean_insert_data(mysql_op):
    print("清理之前")
    actual_rows = mysql_op.fetch_specify_sql_data("SELECT * FROM `customers`")[-1]
    print("000>", actual_rows)
    assert actual_rows == 3

    yield "clean"
    print("清理之后")
    mysql_op.execute_sql("DELETE FROM `customers` WHERE `customer_id` > %s;", (3,))

    actual_rows = mysql_op.fetch_specify_sql_data("SELECT * FROM `customers`")[-1]
    assert actual_rows == 3
