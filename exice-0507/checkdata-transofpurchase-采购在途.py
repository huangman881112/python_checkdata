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





zpoNo = ""
# skuCode = "FTPLPB-0292"
bill_nolist = []
skuList  =[]
sku_str= """FTBFVT-4007"""
# skuList.append(skuCode)
bill_nolist.append(zpoNo)

skuList = sku_str.split(",",-1)
res={}
zpo_res_list = []
zpo_res_list_ = []
for sku in skuList:
    param_body = comutils.getApiList()[comutils.PURCHASE_ZPO_LIST_PARA_BODY]
    # param_body[comutils.PURCHASE_ZPO_LIST_PARA_BODY_ZPOID] = bill_no
    param_body[comutils.PURCHASE_ZPO_LIST_PARA_BODY_SKUCODE] = sku
    response = requests.post(comutils.getApiList()[comutils.PURCHASE_ZPO_LIST_URL], json=param_body, headers=comutils.getHeaders())
    # print(response.text)
    po_res = json.loads(response.text)
    po_list = po_res[comutils.DATA][comutils.LIST]
    # print(po_list)

    res["zpo_inv_qty"] = 0
    sum_purchase_amount = 0
    for po_no in po_list:
        year = int( po_no["poId"][2:4])
        if year < 23:
            continue
        # po_no = po_list[0][comutils.PURCHASE_DETAIL_PARA_BODY_POID]
        zpo_param_body = comutils.getApiList()[comutils.PURCHASE_DETAIL_PARA_BODY]
        zpo_param_body["poId"] = po_no["poId"]
        skulist = []
        skulist.append(sku)
        zpo_param_body[comutils.PURCHASE_DETAIL_PARA_BODY_CINVCODELIST] = skulist
        # qty = int(bill_nolist[bill_no])
        # print(qty)
        zpo_response = requests.post(comutils.getApiList()[comutils.PURCHASE_DETAIL_URL], json=zpo_param_body, headers=comutils.getHeaders())
        # print(zpo_response.text)
        response_data = json.loads(zpo_response.text)
        if "data" in response_data:
            response_records = response_data["data"]
            zpolist = response_data["data"]["poDetailEntityPageInfo"]["list"]
            for zpo in zpolist:
                zpo_res = dict()
                if  (zpoNo!="" and zpo["cpoId"] == zpoNo) or zpo[comutils.PURCHASE_ZPO_LIST_PARA_BODY_SKUCODE] == sku:
                    produc_transit_qty = zpo["ziquantityQty"]-zpo["ireceivedQty"]- zpo["reservationQty"]-zpo["straightHairQty"]-zpo["closeQty"]
                    zpo_res["pur_zpo"] = zpo["cpoId"]
                    zpo_res["po"] = po_no["poId"]
                    zpo_res["produc_transit"] = produc_transit_qty
                    zpo_res["skuCode"] = sku
                    zpo_res["oldSkuCode"] = zpo["zoldSku"]
                    store_code = comutils.getstorelist()[zpo["store"]]
                    platfrom_code = comutils.getplatformlist()[zpo["zplatform"]]
                    oldSkuCode = zpo["zoldSku"]
                    zpo_res["store_code"]= store_code
                    zpo_res["platfrom_code"]= platfrom_code
                    # zpo_res_list.append(zpo_res)
                    # print(res)
                    # sum_purchase_amount += produc_transit_qty
                    inv_para_body = comutils.getApiList()[comutils.INV_OCCPY_PARA_BODY]
                    inv_para_body[comutils.SKUCODE]=sku
                    bizType=[]
                    bizType.append(comutils.PUR_PRODUCE_IN_TRANSIT)
                    inv_para_body[comutils.WAREHOUSECODE]="01"
                    inv_para_body[comutils.OLD_SKU_CODE]=oldSkuCode
                    inv_para_body["platform"]=platfrom_code
                    inv_para_body["store"]=store_code
                    inv_para_body[comutils.INV_OCCPY_BIZTYPELIST]=bizType
                    # print(inv_para_body)
                    response = requests.post(comutils.getApiList()[comutils.INV_OCCPY_URL], json=inv_para_body,
                                             headers=comutils.getHeaders())
                    # print(response.text)
                    inv_res = json.loads(response.text)
                    inv_sku_list = inv_res[comutils.DATA][comutils.RECORDS]
                    zpo_res["zpo_inv_qty"] = 0
                    if len(inv_sku_list)>0:
                        # print(inv_sku_list)
                        for inv_sku in inv_sku_list:
                            if  inv_sku["billNo"] == zpo_res["pur_zpo"]:
                                zpo_res["zpo"] = inv_sku["billNo"]
                                zpo_res["zpo_inv_qty"] = inv_sku["qty"]
                                break
                            # elif zpo_res["produc_transit"]>0:
                            #      zpo_res["zpo"] = inv_sku["billNo"]
                            #      zpo_res["zpo_inv_qty"] += inv_sku["qty"]
                            #     break
                    zpo_res["produc_transit_dif"] = zpo_res["produc_transit"]-zpo_res["zpo_inv_qty"]
                    if zpo_res["produc_transit_dif"]>0:
                        zpo_res_list.append(zpo_res)
                        print(zpo_res)
                    else:
                        zpo_res_list_.append(zpo_res)
    print(zpo_res_list)
    print(zpo_res_list_)