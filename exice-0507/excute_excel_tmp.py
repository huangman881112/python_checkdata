import datetime
import json
import time

from openpyxl import Workbook

from openpyxl import load_workbook

import pandas as pd

import commonUtil as comu
import requests
import json


def getsubDbNo(dbno):
    body = {"ctvcode":"DB24070800288","cdefine13":"","ciwhcode":"","cowhcode":"","cinvcode":"","oldSku":"",
            "startdate":"2024-06-09","enddate":"2024-07-10","isover":"",
            "isshipmentId":"","shipmentId":"","billtype":2,"current":1,"size":10}
    body["ctvcode"]= dbno
    response = requests.post("https://wms-web.yintaerp.com/wms-web/wh/transfer/list",json=body,headers=comu.getHeaders())
    # print(response.text)
    res = json.loads(response.text)
    id = res["data"]["records"][0]["id"]
    detailBoyd = {"id":"548852","transtype":2}
    detailBoyd["id"]=id
    response = requests.post("https://wms-web.yintaerp.com/wms-web/wh/transfer/detail/list", json=detailBoyd,
                             headers=comu.getHeaders())
    # print(response.text)
    res_sub = json.loads(response.text)
    sub_no = res_sub["data"][0]["cTVCode"]
    return sub_no

dbno = "DB24070700546"
getsubDbNo(dbno)