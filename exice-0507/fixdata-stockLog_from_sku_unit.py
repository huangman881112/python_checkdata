import json
import Action

import excute_log_abstract as excuteabcLog
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

filename = "D:\\tmp\\stock_log\\tmp-stocklog.xlsx"


class OccpyWmsClass:
    req_exam_str_other = comutils.OTHER_OUTBOUND

    def __init__(self):
        super().__init__()

    def execute_log_2_sku(self, skuList):
        for sku in skuList:
            for prop in sku:
                if prop.endswith("Qty") and sku[prop] != 0:
                    sku[prop] = sku[prop] * -1
        return skuList

    def execute_log_total_qty(self, skuList):
        for sku in skuList:
            for prop in sku:
                if prop.endswith("Qty") and prop != 'totalQty' and sku[prop] != 0:
                    sku[prop] = 0
        return skuList

    def execute_log_sku(self, skuList):
        for sku in skuList:
            for prop in sku:
                if prop.endswith("Qty") and sku[prop] != 0:
                    sku[prop] = sku[prop]
        return skuList

    def execute_log_req(self, req_exam):
        # print(req_exam["billNo"])
        org_bill = req_exam["billNo"]
        # bills = comutils.getBillList()
        # if org_bill not in bills:
        #     return None
        skulist = req_exam["skuList"]
        # skulist = self.execute_log_2_sku(skulist)
        req_exam["skuList"] = self.execute_log_total_qty(skulist)
        req_exam["operationTypeEnum"] = "NULL"
        return req_exam


wmsOccpy = OccpyWmsClass()
res = excuteabcLog.execute_stock_log(filename, comutils.OTHER_OUTBOUND, wmsOccpy, 0, False)
print(res)