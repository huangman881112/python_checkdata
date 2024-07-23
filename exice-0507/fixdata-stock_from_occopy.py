from datetime import datetime
import json
import Action

import excute_abstract as excuteabc
import commonUtil as comutils

# 目标URL


filename = "d:\\tmp\\tmp-occoupy.xlsx"
tmpfile = "d:\\tmp\\tmp.txt"


class OccpySalesClass:


    req_exam = comutils.SALES_ORDER_JIE_DAN

    def __init__(self):
        super().__init__()


    def execute_sku(self,skulist):
        for sku in skulist:
            qty = int(sku["holdQty"])
            sku["holdQty"] = qty * -1
        return skulist


    def excute_req(self, req_exam):
        # BillList = comutils.getBillList()
        # if req_exam["originBillNo"] not in BillList:
        #     req_exam=None
        #     return
        result = comutils.getSalesOrders(req_exam["originBillNo"])
        skuList = req_exam["skuList"]
        # 释放预占库存
        if 'orderStatus' in result and result["orderStatus"] == 99:
            req_exam["skuList"] = self.execute_sku(skuList)
        # else:
            # print(req_exam)
            # req_exam = None
        return req_exam



class OccpyWmsClass:


    req_exam = comutils.SALES_ORDER_OUT

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
            sku["useQty"] = qty * 1
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
        # print(result)
        skuList = req_exam["skuList"]
        if 'orderStatus' in result and result["orderStatus"] == 2:
            billNo = result["warehouseOrderId"]
            req_exam["billNo"] = billNo
            req_exam["remark"] = billNo
            req_exam["skuList"] = self.excute_2_sku(skuList)
        elif 'orderStatus' in result and result["orderStatus"] == -1:
            req_exam["skuList"] = self.excute__1_sku(skuList)
            req_exam["billTypeEnum"] = "SALE_OUTBOUND_ORDERS"
        elif 'orderStatus' in result and result["orderStatus"] == 99:
            req_exam["skuList"] = self.excute__1_sku(skuList)
            req_exam["billTypeEnum"] = "SALE_OUTBOUND_ORDERS"
        else:
            print(req_exam)
            req_exam = None
        return req_exam


class nullBillClass:
    req_exam=None
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

    def excute_rever_hold_sku(self, skuList):
        for sku in skuList:
            qty = int(sku["holdQty"])
            sku["holdQty"] = qty * -1
            sku["useQty"] = qty
            sku["totalQty"] = 0
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
        print(req_exam["operationTypeEnum"])
        self.excute_rever_hold_sku(skuList)
        # opertype = str(req_exam["operationTypeEnum"])
        # if opertype in opertypes:
        #     req_exam["operationTypeEnum"] = opertypes[req_exam["operationTypeEnum"]]
        #     if "OUT_HOLD" in opertype:
        #         if opertype.startswith("BAD"):
        #             req_exam["skuList"] = self.excute_bad_hold_sku(skuList)
        #         else:
        #             req_exam["skuList"] = self.excute_rever_hold_sku(skuList)
        #     elif "PUWAWAY_HOLD" in opertype :
        #         print(opertype)
        return req_exam

#头程出运
class HeadTransClass:
    req_exam = comutils.HEAD_TRANS_SHIPOUT

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


#采购生产在途
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



#采购收货在途
class PuchaseReceiveTransitClass:

    req_exam = comutils.PURCHASE_RECEIVE_TRANSIT

    def __init__(self):
        super().__init__()

    def excute_pur_receivce_transit_sku(self, skuList):
        for sku in skuList:
            qty = int(sku["inTransitQty"])
            sku["inTransitQty"] = qty * -1
        return skuList

    def excute_req(self, req_exam):
        billNo = req_exam["billNo"]
        req_exam["originBillNo"] = billNo
        req_exam["operationTypeEnum"] = "PUR_RECEIVE_IN_TRANSIT"
        skuList = req_exam["skuList"]
        req_exam["skuList"] = self.excute_pur_receivce_transit_sku(skuList)
        return req_exam



#头程入库
class HeadTransInbound:

    req_exam = comutils.HEAD_TRANS_INBOUND

    def __init__(self):
        super().__init__()

    def excute_pur_receivce_transit_sku(self, skuList):
        for sku in skuList:
            qty = int(sku["inTransitQty"])
            sku["inTransitQty"] = qty * -1
        return skuList

    def excute_req(self, req_exam):

        skuList = req_exam["skuList"]
        req_exam["skuList"] = self.excute_pur_receivce_transit_sku(skuList)
        return req_exam



class wmsHeadTransClass:

    req_exam = comutils.HEAD_TRANS_OUT

    def __init__(self):
        super().__init__()


    def execute_bad2good_sku(self, skuList):
        for sku in skuList:
            qty = sku["holdQty"]
            sku["holdQty"] = qty*-1
            sku["useQty"] = qty
            sku["totalQty"] = 0
        return skuList

    def execute_releaseHold_sku(self, skuList):
        for sku in skuList:
            qty = sku["holdQty"]
            if qty > 0:
                qty=qty*-1
            sku["holdQty"] = qty
            sku["useQty"] = qty*-1
            sku["totalQty"] = 0
        return skuList

    def execute_outHold_sku(self, skuList):
        for sku in skuList:
            qty = sku["holdQty"]
            if qty > 0:
                qty = qty * -1
            sku["holdQty"] = qty
            sku["totalQty"] = qty
        return skuList

    def excute_req(self, req_exam):
        # print(req_exam["billNo"])
        # org_bill = req_exam["billNo"]
        # bills = comutils.getBillList()
        # if org_bill not in bills:
        #     return None
        skulist = req_exam["skuList"]
        req_exam["skuList"] = self.execute_releaseHold_sku(skulist)
        # req_exam["operationTypeEnum"] = "NULL"
        return req_exam


wmsOccpy =wmsHeadTransClass()
result = excuteabc.excute_occpy(filename, wmsOccpy.req_exam, wmsOccpy, 0, True)
print(result)
