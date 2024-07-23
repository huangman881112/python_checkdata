from datetime import datetime
import json
import time

from openpyxl import Workbook

from openpyxl import load_workbook

import commonUtil as comutils

import excute_abstract as excuteabstract




OTHER_INBOUND = """
{
	"billNo": "RD24060414077",
	"billStatusEnum": "FINISH",
	"billTime": "2024-06-04T06:47:56.982",
	"billTypeEnum": "OTHER_INBOUND",
	"operationTypeEnum": "PUTAWAY",
	"originBillNo": "RD24060414077",
	"skuList": [
		{
			"badHoldQty": 0,
			"badQty": 0,
			"freezeQty": 0,
			"holdQty": 1,
			"inTransitQty": 0,
			"oldSkuCode": "FTPLPB-0183",
			"platform": "10001",
			"skuCode": "FTPLPB-0183",
			"store": "10415",
			"totalQty": 1,
			"useQty": 0
		}
	],
	"warehouseCode": "11"
}
"""






filename = "d:\\tmp\\tmp-sku_unit_stock.xlsx"





class OccpyWmsClass:

    req_exam = None

    def __init__(self):
        super().__init__()

    def execute_log_2_sku(self, skuList):
        for sku in skuList:
            qty = int(sku["holdQty"])
            sku["holdQty"] = qty * -1
            sku["totalQty"] = qty * -1
        return skuList

    def execute_log__1_sku(self, skuList):
        for sku in skuList:
            qty = int(sku["holdQty"])
            sku["holdQty"] = qty * -1
            sku["usedQty"] = qty * 1
            sku["totalQty"] = 0
        return skuList

    def execute_sku(self, skuList):
        for sku in skuList:
            for prop in sku:
                if prop.endswith("Qty") and sku[prop] != 0 and prop != "holdQty":
                    sku[prop] = sku[prop] * -1
        return skuList

    def execute_sku_total(self, skuList):
        for sku in skuList:
            for prop in sku:
                if prop.endswith("Qty") and sku[prop] != 0 and prop != "totalQty":
                    sku[prop] = 0
        return skuList

    def execute_req(self, req_exam):
        # print(req_exam["billNo"])
        # org_bill = req_exam["billNo"]
        # bills = comutils.getBillList()
        # if org_bill not in bills:
        #     return None
        skulist = req_exam["skuList"]
        req_exam["skuList"] = self.execute_sku_total(skulist)
        req_exam["operationTypeEnum"]="NULL"
        return req_exam


class BadQtyClass:

    req_exam = None


    def __init__(self):
        super().__init__()

    def execute_bad_sku(self, skuList):
        for sku in skuList:
            qty = sku["holdQty"]
            sku["badQty"] = qty
            sku["totalQty"] = qty
            sku["holdQty"] = 0
        return skuList

    def execute_req(self, req_exam):
        # print(req_exam["billNo"])
        # org_bill = req_exam["billNo"]
        # bills = comutils.getBillList()
        # if org_bill not in bills:
        #     return None
        skulist = req_exam["skuList"]
        req_exam["skuList"] = self.execute_bad_sku(skulist)
        req_exam["operationTypeEnum"] = "NULL"
        return req_exam


class headTransClass:

    req_exam = comutils.HEAD_SHIPMENT

    def __init__(self):
        super().__init__()


    def execute_sku(self, skuList):
        for sku in skuList:
            qty = sku["holdQty"]
            sku["badQty"] = qty
            sku["totalQty"] = qty
            sku["holdQty"] = 0
        return skuList


    def execute_req(self, req_exam):
        # print(req_exam["billNo"])
        # org_bill = req_exam["billNo"]
        # bills = comutils.getBillList()
        # if org_bill not in bills:
        #     return None
        skulist = req_exam["skuList"]
        req_exam["skuList"] = self.execute_sku(skulist)
        # req_exam["operationTypeEnum"] = "NULL"
        return req_exam


class wmsHeadTransClass:

    req_exam = comutils.HEAD_TRANS_OUT

    def __init__(self):
        super().__init__()


    def execute_sku(self, skuList):
        for sku in skuList:
            qty = sku["holdQty"]
            sku["badQty"] = qty
            sku["totalQty"] = qty
            sku["holdQty"] = 0
        return skuList


    def execute_req(self, req_exam):
        # print(req_exam["billNo"])
        # org_bill = req_exam["billNo"]
        # bills = comutils.getBillList()
        # if org_bill not in bills:
        #     return None
        skulist = req_exam["skuList"]
        req_exam["skuList"] = self.execute_sku(skulist)
        # req_exam["operationTypeEnum"] = "NULL"
        return req_exam



class PurchaseTransitClass:
    req_exam = comutils.PURCHASE_PRODUCE_TRANSIT

    def __init__(self):
        super().__init__()

    def excute_pur_transit_sku(self, skuList):
        for sku in skuList:
            qty = int(sku["inTransitQty"])
            sku["inTransitQty"] = qty
        return skuList

    def execute_req(self, req_exam):
        billNo = req_exam["billNo"]
        req_exam["originBillNo"] = billNo
        skuList = req_exam["skuList"]
        req_exam["skuList"] = self.excute_pur_transit_sku(skuList)

        return req_exam





class otherInboundClass:

    req_exam = None

    def __init__(self):
        super().__init__()


    def execute_sku(self, skuList):
        for sku in skuList:
            qty = sku["totalQty"]
            sku["useQty"] = qty
            sku["totalQty"] = qty
            sku["holdQty"] = 0
        return skuList

    def execute_sku_totalQty(self, skuList):
        for sku in skuList:
            qty = sku["totalQty"]
            sku["useQty"] = qty
            sku["totalQty"] = qty
            sku["holdQty"] = 0
        return skuList

    #集散仓库存站点初始化规则(上海集散仓/佛山集散仓)
    #1.SKU尾缀“-E”"-DS" 站点<EU>
    #2.SKU尾缀“-UK”站点<UK>
    #3.没有以上3种尾缀的站点<US>
    #
    #
    def execute_uk_sku(self, skuList):
        skulistnew = []

        for sku in skuList:

            qty = sku["totalQty"]*-1
            sku["useQty"] = qty
            sku["totalQty"] = qty
            sku["holdQty"] = 0
            sku_q = comutils.init_data(sku,None,"json")
            sku_w = comutils.init_data(sku,None,"json")
            if sku["skuCode"].endswith("-E") or sku["skuCode"].endswith("-DS"):
                sku_w["site"] = "EU"
            elif sku["skuCode"].endswith("-UK"):
                sku_w["site"] = "UK"
            else:
                sku_w["site"] = "US"
            sku_w["badQty"] = qty
            sku_w["useQty"] = qty*-1
            sku_w["totalQty"] = 0

            skulistnew.append(sku_q)
            skulistnew.append(sku_w)
        return skulistnew


    def execute_req(self, req_exam):
        # print(req_exam["billNo"])
        # org_bill = req_exam["billNo"]
        # bills = comutils.getBillList()
        # if org_bill not in bills:
        #     return None
        skulist = req_exam["skuList"]
        req_exam["skuList"] = self.execute_uk_sku(skulist)
        req_exam["operationTypeEnum"] = "NULL"
        return req_exam


wmsOccpy = wmsHeadTransClass()
resut = excuteabstract.execute_stock_with_unit(filename,wmsOccpy.req_exam, wmsOccpy, 0, False)
print(resut)