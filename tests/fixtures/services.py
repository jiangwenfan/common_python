import pytest

from .utils import parse_container_status
import subprocess
import time


@pytest.fixture(scope="class")
def start_stop_mysql():
    """在测试会话开始时执行的代码"""
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
