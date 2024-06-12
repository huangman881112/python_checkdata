from datetime import datetime
import secrets
import string
import time

from openpyxl import Workbook
from openpyxl import load_workbook
import pandas as pd
import requests
import json

import commonUtil as comutils





zpoNo = "ZPO24032200477"
skuCode = "FRSSPF-0116"
bill_nolist = []



for bill_no in bill_nolist:
    param_body = comutils.getApiList()[comutils.PURCHASE_ZPO_LIST_PARA_BODY]
    param_body[comutils.PURCHASE_ZPO_LIST_PARA_BODY_ZPOID] = bill_no
    response = requests.post(comutils.getApiList()[comutils.PURCHASE_ZPO_LIST_URL], json=param_body, headers=headers)
    po_res = json.loads(response.text)
    po_list = po_res[comutils.DATA][comutils.LIST]
    print(po_list)
    po_no = po_list[0][comutils.PURCHASE_DETAIL_PARA_BODY_POID]

    zpo_param_body = comutils.getApiList()[comutils.PURCHASE_DETAIL_PARA_BODY]
    res={}
    zpo_param_body["poId"] = po_no
    skulist = []
    skulist.append(skuCode)
    zpo_param_body[comutils.PURCHASE_DETAIL_PARA_BODY_CINVCODELIST] = skulist
    # qty = int(bill_nolist[bill_no])
    # print(qty)
    zpo_response = requests.post(comutils.getApiList()[comutils.PURCHASE_DETAIL_URL], json=zpo_param_body, headers=comutils.getHeaders())
    print(zpo_response.text)
    response_data = json.loads(zpo_response.text)
    response_records = response_data["data"]
    zpolist = response_data["data"]["poDetailEntityPageInfo"]["list"]
    for zpo in zpolist:
        if zpo["cpoId"] == zpoNo:
            produc_transit_qty = zpo["ziquantityQty"]-zpo["ireceivedQty"]- zpo["reservationQty"]-zpo["straightHairQty"]
            res["zpo"] = zpoNo
            res["produc_transit"] = produc_transit_qty
            res["skuCode"] = skuCode
            print(res)
    rec_str = json.dumps(response_records)
    # print(bill_no,qty)

