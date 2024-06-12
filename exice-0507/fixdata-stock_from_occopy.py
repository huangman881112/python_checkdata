from datetime import datetime
import json
import Action

import excute_abstract as excuteabc
import commonUtil as comutils

# 目标URL


filename = "d:\\tmp\\tmp-occoupy.xlsx"
tmpfile = "d:\\tmp\\tmp.txt"


class OccpyWmsClass:
    def __init__(self):
        super().__init__()

    def excute_2_sku(self, skuList):
        for sku in skuList:
            qty = int(sku["holdQty"])
            sku["holdQty"] = qty * -1
            sku["totalQty"] = qty * -1
        return skuList

    def excute__1_sku(self, skuList):
        for sku in skuList:
            qty = int(sku["holdQty"])
            sku["holdQty"] = qty * -1
            sku["usedQty"] = qty * 1
            sku["totalQty"] = 0
        return skuList

    def excute_sku(self, skuList):
        # for sku in skuList:
        #     qty = int(sku["holdQty"])
        #     sku["holdQty"] = qty * -1
        #     sku["totalQty"] = qty * -1
        return skuList

    def excute_req(self, req_exam):
        # BillList = comutils.getBillList()
        # if req_exam["originBillNo"] not in BillList:
        #     req_exam=None
        #     return
        result = comutils.getSalesOrders(req_exam["originBillNo"])
        skuList = req_exam["skuList"]
        if 'orderStatus' in result and result["orderStatus"] == 2:
            billNo = result["warehouseOrderId"]
            req_exam["billNo"] = billNo
            req_exam["remark"] = billNo
            req_exam["skuList"] = self.excute_2_sku(skuList)
        elif 'orderStatus' in result and result["orderStatus"] == -1:
            req_exam["skuList"] = self.excute__1_sku(skuList)
        else:
            print(req_exam)
            req_exam = None
        return req_exam


class nullBillClass:

    def __init__(self):
        super().__init__()

    def excute_transit_sku(self, skuList):
        for sku in skuList:
            qty = int(sku["holdQty"])
            sku["inTransitQty"] = qty * -1
            sku["holdQty"] = 0
            sku["totalQty"] = 0
        return skuList

    def excute_hold_sku(self, skuList):
        for sku in skuList:
            qty = int(sku["holdQty"])
            sku["holdQty"] = qty * -1
            sku["totalQty"] = qty * -1
        return skuList

    def excute_bad_hold_sku(self, skuList):
        for sku in skuList:
            qty = int(sku["holdQty"])
            sku["badHoldQty"] = qty * -1
            sku["totalQty"] = qty * -1
            sku["holdQty"] = 0
        return skuList

    def excute_req(self, req_exam):
        now_date = datetime.now()
        billNo = now_date.strftime("%y%m%d") + "_inv_fix_occpy"
        req_exam["originBillNo"] = billNo
        req_exam["remark"] = billNo
        req_exam["billNo"] = billNo
        skuList = req_exam["skuList"]
        opertypes = comutils.getOperType()
        opertype = str(req_exam["operationTypeEnum"])
        if opertype in opertypes:
            req_exam["operationTypeEnum"] = opertypes[req_exam["operationTypeEnum"]]
            if opertype.startswith("BAD"):
                req_exam["skuList"] = self.excute_bad_hold_sku(skuList)
            else:
                req_exam["skuList"] = self.excute_hold_sku(skuList)
        else:
            req_exam["skuList"] = self.excute_transit_sku(skuList)
        return req_exam


class HeadTransClass:
    req_exam = comutils.HEAD_TRANS_OUT

    def __init__(self):
        super().__init__()


    def excute_ship_hold_sku(self, skuList):
        for sku in skuList:
            qty = int(sku["holdQty"])
            sku["holdQty"] = qty * -1
            sku["totalQty"] = qty * -1
        return skuList

    def excute_req(self, req_exam):
        billNo = req_exam["billNo"]
        req_exam["originBillNo"] = billNo
        skuList = req_exam["skuList"]
        req_exam["skuList"] = self.excute_ship_hold_sku(skuList)

        return req_exam


class PurchaseTransitClass:
    req_exam = comutils.PURCHASE_PRODUCE_TRANSIT

    def __init__(self):
        super().__init__()

    def excute_pur_transit_sku(self, skuList):
        for sku in skuList:
            qty = int(sku["inTransitQty"])
            sku["inTransitQty"] = qty * -1
        return skuList

    def excute_req(self, req_exam):
        billNo = req_exam["billNo"]
        req_exam["originBillNo"] = billNo
        skuList = req_exam["skuList"]
        req_exam["skuList"] = self.excute_pur_transit_sku(skuList)

        return req_exam


wmsOccpy = PurchaseTransitClass()
result = excuteabc.excute_occpy(filename, wmsOccpy.req_exam, wmsOccpy, 0, False)
print(result)
