# common_packages
封装了一些通用的功能

打包
```bash
python -m build
```
安装
```bash
pip install common_packages-0.1.0.tar.gz
```
pypi
https://pypi.org/project/common-packages/#description

依赖
```bash
    "requests",
    'pika',
    "tencentcloud-sdk-python-tmt",
    "kafka-python",
    "clickhouse-driver",
    "numpy",
    "pandas",
    "sqlalchemy",
    "pymysql",
    "azure-cognitiveservices-speech",
```

单元测试:
```bash
pytest
```

### 1. db utils
- [x] mysql
```python
# mysql配置
mysql_config = {
  "host": "xxx"
  "port": xxx
  "user" : "xxx"
  "password" :"xxx"
  "database" : "xxx"
}

mysql_op = MysqlOperator(**mysql_config)

# 接口1: 获取所有表名
tables: set[str] = mysql_op.fetch_all_tables()

# 接口2: 执行`查询sql`,返回执行结果
data: DataFrame, columns: list[str] = mysql_op.fetch_specify_sql_data("SELECT * FROM customers")

# 接口3: 执行`插入sql`，使用指定dataframe数据，指定表名
need_insert_data = [
    {"customer_name": "test1", "email": "test1@gmail.com"},
    {"customer_name": "test2", "email": "test2@gmail.com"},
]
need_insert_dataframe = pd.DataFrame(need_insert_data)
rows: int = mysql_op.insert_database_mysql(need_insert_dataframe, "customers")
```

### 1. translation
> 封装翻译接口
>

- [x] mircrosoft 翻译
```python

```
- 参考：
  - []()
    - 创建文本翻译服务
  - [tts文档](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/index-text-to-speech)
    - 创建tts服务：在`Azure` --> `Azure AI services` --> `语音服务`

- 将要支持的:
  - [ ] google 翻译
  - [ ] Deepl 翻译
  - [ ] openAI 翻译
- 不打算支持的:
  - tencent 翻译,翻译质量较差
- [ ] youdao 翻译
```python
```

### 2. Ai接口
> 解释句子,分析长难句
- [ ] openAI 翻译
- [ ] gemini 翻译

### sms
腾讯云
```python

```

- [x] 可选导入模块,未安装时,提示安装!
