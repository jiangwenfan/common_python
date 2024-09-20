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
### sms
腾讯云
```python

```

- [x] 可选导入模块,未安装时,提示安装!

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
