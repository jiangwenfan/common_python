import json
import sys

sys.path.append("..")
import json
import logging

from common_packages.db_utils import MysqlOperator

from . import get_config

logging.basicConfig(level=logging.INFO)


class TestMysqlOperator:
    def test_mysql(self):
        config: dict = get_config()
        mysql = MysqlOperator(**config["db"]["mysql"])
        tables: set[str] = mysql.fetch_all_tables()
        # print(tables)

        data = mysql.fetch_specify_sql_data("select * from `gallery` limit 5;")
        # # print(data)

        data2 = mysql.delete_auto_increment_column(data[0])
        print(data2)

        mysql.insert_database_mysql(data2, "gallery")
