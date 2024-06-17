import json
import Action

import excute_abstract as excuteabc
import commonUtil as comutils

# 目标URL


sales_order_out = """
{
	"billNo": "AF24053100527",
	"billStatusEnum": "FINISH",
	"billTime": "2024-05-31T12:00:06.912",
	"billTypeEnum": "SALE_OUTBOUND_WMS",
	"operationTypeEnum": "HOLD",
	"originBillNo": "GOC65167864",
	"skuList": [
		{
			"badHoldQty": 0,
			"badQty": 0,
			"freezeQty": 0,
			"holdQty": -1,
			"inTransitQty": 0,
			"oldSkuCode": "OETETA-0016",
			"platform": "10002",
			"skuCode": "OETETA-0016",
			"store": "10339",
			"totalQty": -1,
			"useQty": 0
		}
	],
	"warehouseCode": "18"
}
"""

filename = "d:\\tmp\\tmp-errorlog.xlsx"
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


class OccpyFbaRClass:

    def __init__(self):
        super().__init__()

    def exeute_ro(self, skuList):
        for sku in skuList:
            sku["inTransitQty"] = 0
        return skuList

    def excute_req(self, req_exam):
        billno = req_exam["billNo"]
        # BillList = comutils.getBillList()
        # if req_exam["originBillNo"] not in BillList:
        #     req_exam=None
        #     return

        skuList = req_exam["skuList"]
        if billno.startswith("RO"):
            req_exam["operationTypeEnum"] = "PUTAWAY"
            req_exam["skuList"] = self.exeute_ro(skuList)
        return req_exam


class OccpyRmaClass:
    def __init__(self):
        super().__init__()

    def execute_qc(self, skuList):
        newskulist = []
        for sku in skuList:
            if sku["holdQty"] < 0:
                continue
            sku = json.dumps(sku)
            sku_exam = comutils.init_data(sku, None)
            sku_exam["totalQty"] = sku_exam["holdQty"]
            newskulist.append(sku_exam)
        return newskulist

    def excute_req(self, req_exam):
        billno = req_exam["billNo"]
        # BillList = comutils.getBillList()
        # if req_exam["originBillNo"] not in BillList:
        #     req_exam=None
        #     return

        skuList = req_exam["skuList"]
        if billno.startswith("QC"):
            req_exam["skuList"] = self.execute_qc(skuList)
        return req_exam




class PurchaseProducerClass:
    def __init__(self):
        super().__init__()

    def execute_pur(self, skulist, zpo):
        po = comutils.getPurchasePO(zpo)
        for sku in skulist:
            comutils.getPurchaseZpoDetail(po, sku["skuCode"])
        return skulist


    def execute_putaway_pur_with_no_occpy(self,skulist):
        for sku in skulist:
            qty = sku["holdQty"]
            sku["useQty"] = qty*-1
            sku["holdQty"] = 0
            sku["totalQty"] = qty*-1
        return skulist

    def excute_req(self, req_exam):
        skulist = req_exam["skuList"]
        req_exam["operationTypeEnum"] = "NULL"
        req_exam["skuList"] = self.execute_putaway_pur_with_no_occpy(skulist)
        return req_exam


class OtherOutboundClass:

    def __init__(self):
        super().__init__()

    def execute_otherout(self, skuList):
        return skuList

    def execute_req(self, req_exam):
        skulist = req_exam["skuList"]

        req_exam["skuList"] = self.execute_otherout(skulist)
        return req_exam


class CommonClass:
    def __init__(self):
        super().__init__()

    def excute_req(self, req_exam):
        return req_exam


wmsOccpy = PurchaseProducerClass()
result = excuteabc.excute_error_log(filename, wmsOccpy, 0, True)
print(result)
