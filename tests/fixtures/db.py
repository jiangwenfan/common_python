import pytest

from common_packages.db_utils.mysql import MysqlOperator


from .utils import parse_container_status
import subprocess
import time


@pytest.fixture(scope="class")
def start_stop_mysql():
    """用于在`整个mysql测试类`中启动和关闭mysql服务"""
    print("启动临时mysql服务, test_services/compose-mysql.yml")
    subprocess.run(
        [
            "docker",
            "compose",
            "-f",
            "test_services/compose-mysql.yml",
            "up",
            "-d",
        ],
        check=True,
    )
    # 等待mysql服务启动，如果超过120秒还没有成功启动，则则退出
    num = 0
    while num < 120:
        health_status = parse_container_status("temp-mysql")
        if health_status == "healthy":
            print("mysql服务启动成功....")
            break
        num += 1
        time.sleep(1)
    else:
        raise TimeoutError("mysql服务启动超时")

    yield "mysql"

    print("关闭临时mysql服务, test_services/compose-mysql.yml")
    # subprocess.run(
    #     [
    #         "docker",
    #         "compose",
    #         "-f",
    #         "test_services/compose-mysql.yml",
    #         "down",
    #     ],
    #     check=True,
    # )


@pytest.fixture(scope="function")
def mysql_op(global_config):
    """用于在`每个测试用例`中初始化mysql操作对象"""
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
