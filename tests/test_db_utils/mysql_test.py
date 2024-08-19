import pytest

import logging

logging.basicConfig(level=logging.INFO)


@pytest.mark.usefixtures("start_stop_mysql")
class TestMysqlOperator:
    def test_fetch_all_tables(self, mysql_op):
        actual_tables: set[str] = mysql_op.fetch_all_tables()
        actual_tables_num = len(actual_tables)

        expected_tables = {"customers", "orders"}
        excepted_tables_num = len(expected_tables)

        assert excepted_tables_num == actual_tables_num
        assert expected_tables == actual_tables

    def test_fetch_specify_sql_data(self, mysql_op):
        data, columns, rows = mysql_op.fetch_specify_sql_data("SELECT * FROM customers")

        expected_columns = ["customer_id", "customer_name", "email"]

        assert columns == expected_columns
        assert rows == 3

    def test_insert_database_mysql(self, mysql_op, clean_insert_data):
        # mysql_op.insert_database_mysql(data2, "gallery")
        print("插入数据....")
