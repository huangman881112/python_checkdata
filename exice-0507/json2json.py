import json
from openpyxl import Workbook
from datetime import datetime

# filename = "d:\\tmp\\tmp.xlsx"
tmpfile = "d:\\tmp\\tmp.txt"

content = ''
with open(tmpfile, 'r', encoding='utf-8') as file:
    # content = file.read()  # 一次性读取整个文件内容
    # 或者使用以下方式逐行读取
    for line in file:
        content += line
    # print(content)

# 加载现有的Excel文件

content = json.loads(content)
split = content["skuList"]

for sku in split:
    sku["totalQty"] = 0

content["skuList"] = split
content = json.dumps(content)
print(content)

# 保存对文件的更改

