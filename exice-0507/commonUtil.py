import json
import string
import secrets

import requests

url = 'https://inv-web.yintaerp.com/api/inv/invWarehouseRatio/executeLogicStock'
sales_order_url = 'https://inv-web.yintaerp.comyinta-business-web/frontend/goc/listByPage'


def getToken():
    token_str = ''
    with open('token', 'r', encoding='utf-8') as file:
        # content = file.read()  # 一次性读取整个文件内容
        # 或者使用以下方式逐行读取
        for line in file:
            token_str += line
    return token_str


def getHeaders():
    # 请求头信息
    headers = {
        "Content-Type": "application/json",  # 假设API期望接收JSON格式的数据
        "Authorization": getToken()  # 例如，使用Bearer Token进行身份验证
        # "Custom-Header": "CustomValue"  # 自定义请求头字段
    }
    # print(result)
    return headers


def init_data(rma_exampl, ignored_data,type=None):
    result = {}
    if type is None or type == "str":
        rma_exampl = json.loads(rma_exampl)
    for data_pro in rma_exampl:
        if data_pro is not None and data_pro == ignored_data:
            continue
        result[data_pro] = rma_exampl[data_pro]
    # print(result)
    return result


def geneare_str(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string


def getSalesOrders(order_no):
    body = {"startSysCreateTime": "", "endSysCreateTime": "", "noType": "ERP单号", "no": order_no,
            "buyerInfoType": "买家ID", "skuList": [], "total": 1, "pageSize": 10, "pageNum": 1, "tabType": 1,
            "orderStatus": 12}
    response = requests.post(getApiList()[ORDER_URL], json=body, headers=getHeaders())
    # print(response.text)
    resultj = json.loads(response.text)
    if resultj["code"] == 200 and len(resultj["data"]["list"]) > 0:
        return resultj["data"]["list"][0]
    return resultj


def getPurchasePO(zop_no):
    body = getApiList()[PURCHASE_ZPO_LIST_PARA_BODY]
    body["zpoId"] = zop_no
    response = requests.post(getApiList()[PURCHASE_ZPO_LIST_URL], json=body, headers=getHeaders())
    # print(response.text)
    resultj = json.loads(response.text)
    if resultj["code"] == 200 and len(resultj["data"]["list"]) > 0:
        return resultj["data"]["list"][0]
    return resultj


def getPurchaseZpoDetail(po, skuCode):
    body = getApiList()[PURCHASE_DETAIL_PARA_BODY]
    body["poId"] = po
    body["cinvCodeList"].append(skuCode)
    response = requests.post(getApiList()[PURCHASE_DETAIL_URL], json=body, headers=getHeaders())
    # print(response.text)
    resultj = json.loads(response.text)
    if resultj["code"] == 200 and len(resultj["data"]["list"]) > 0:
        return resultj["data"]["list"][0]
    return resultj


DATA = "data"
LIST = "list"
RECORDS = "records"
STOCK_URL = "stock_url"
STOCK_LOG_URL = "stock_log_url"

HEAD_LIST_URL = "head_list_url"
HEAD_LIST_PARA_BODY = "head_list_para_body"
HEAD_DETAIL_URL = "head_detail_url"
HEAD_SUPPLYSTRAIGHT_LIST_URL = "head_supplyStraight_list_url"
HEAD_SUPPLYSTRAIGHT_LIST_PARA_BODY = "head_supplyStraight_list_para_body"
HEAD_SUPPLYSTRAIGHT_LIST_ALL_URL = "head_supplyStraight_list_all_url"
HEAD_SUPPLYSTRAIGHT_LIST_ALL_PARA_BODY = "head_supplyStraight_list_all_para_body"
HEAD_SUPPLYSTRAIGHT_LIST_ALL_PARA_BODY_STATUS = "status"
HEAD_SUPPLYSTRAIGHT_LIST_ALL_PARA_BODY_CINVCODE = "cinvCode"
HEAD_SUPPLYSTRAIGHT_LIST_ALL_PARA_BODY_PAGESIZE = "pageSize"
HEAD_SUPPLYSTRAIGHT_LIST_ALL_PARA_BODY_CURRENTPAGE = "currentPage"

HEAD_SUPPLYSTRAIGHT_DETAIL_URL = "head_supplyStraight_detail_url"
HEAD_SUPPLYSTRAIGHT_DETAIL_PARA_BODY = "head_supplyStraight_detail_para_body"
HEAD_SUPPLYSTRAIGHT_DETAIL_PARA_BODY_PLANNO = "planNo"

ORDER_URL = "order_url"

HEAD_DEPOTRESERVATION_LIST_URL = "head_depotReservation_list_url"
HEAD_DEPOTRESERVATION_PARA_BODY = "head_depotReservation_para_body"
HEAD_DEPOTRESERVATION_PARA_BODY_COMPLETESTATUS = "completeStatus"

PURCHASE_ZPO_LIST_URL = "purchase_list_url"
PURCHASE_ZPO_LIST_PARA_BODY = "purchase_list_para_body"
PURCHASE_ZPO_LIST_PARA_BODY_ZPOID = "zpoId"
PURCHASE_ZPO_LIST_PARA_BODY_SKUCODE = "cinvCode"

PURCHASE_DETAIL_URL = "purchase_detail_url"
PURCHASE_DETAIL_PARA_BODY = "purchase_detail_para_body"
PURCHASE_DETAIL_PARA_BODY_POID = "poId"
PURCHASE_DETAIL_PARA_BODY_CINVCODELIST = "cinvCodeList"

WMS_STORAGE_INV_URL = "wms_storage_inv_url"
WMS_STORAGE_INV_PARA_BODY = "wms_storage_inv_para_body"
WHCODE = "whCode"
SKUCODE = "skuCode"

INV_OCCPY_URL = "inv_occpy_url"
INV_OCCPY_PARA_BODY = "inv_occpy_para_body"
WAREHOUSECODE = "whCode"
OLD_SKU_CODE = "oldSkuCode"

INV_STOCK_QUERY_URL = "inv_stock_query_url"
INV_STOCK_QUERY_PARA_BODY = "inv_stock_query_para_body"

INV_OCCPY_BIZTYPELIST = "bizTypeList"
PUR_PRODUCE_IN_TRANSIT = "PUR_PRODUCE_IN_TRANSIT"
PUR_IN_TRANSIT = "PUR_IN_TRANSIT"


def getBillLists(url, body, startPage, pageSize, status, bill_list, skuCode):
    print(url)
    suplr_strt_para_body = getApiList()[body]
    if HEAD_SUPPLYSTRAIGHT_LIST_ALL_PARA_BODY_STATUS in suplr_strt_para_body:
        suplr_strt_para_body[HEAD_SUPPLYSTRAIGHT_LIST_ALL_PARA_BODY_STATUS] = status
    elif HEAD_DEPOTRESERVATION_PARA_BODY_COMPLETESTATUS in suplr_strt_para_body:
        suplr_strt_para_body[HEAD_DEPOTRESERVATION_PARA_BODY_COMPLETESTATUS] = status
    suplr_strt_para_body[HEAD_SUPPLYSTRAIGHT_LIST_ALL_PARA_BODY_PAGESIZE] = pageSize
    suplr_strt_para_body[HEAD_SUPPLYSTRAIGHT_LIST_ALL_PARA_BODY_CURRENTPAGE] = startPage
    if skuCode is not None:
        suplr_strt_para_body[HEAD_SUPPLYSTRAIGHT_LIST_ALL_PARA_BODY_CINVCODE] = skuCode
    suplr_strt_response = requests.post(getApiList()[url],
                                        json=suplr_strt_para_body, headers=getHeaders())
    suplr_strt_res = json.loads(suplr_strt_response.text)
    # print(suplr_strt_res[commutils.DATA])
    for record in suplr_strt_res[DATA][RECORDS]:
        if "planNo" in record:
            bill_list.append(record["planNo"])
        elif "reservationID" in record:
            bill_list.append(record["reservationID"])
    startPage += 1
    while suplr_strt_res[DATA]["total"] > (startPage - 1) * pageSize:
        print(startPage)
        return getBillLists(url, body, startPage, pageSize, status, bill_list)

    return bill_list


def getbilllistswithprop(url: object, body: object, bill_list: object, skuCode: object = None) -> object:
    """

    :param url:
    :param body:
    :param bill_list:
    :param skuCode:
    :return:
    """
    startPage = body["current"]
    pageSize = body["size"]
    if skuCode is not None:
        body[HEAD_SUPPLYSTRAIGHT_LIST_ALL_PARA_BODY_CINVCODE] = skuCode
    suplr_strt_response = requests.post(url,
                                        json=body, headers=getHeaders())
    suplr_strt_res = json.loads(suplr_strt_response.text)
    # print(suplr_strt_res[commutils.DATA])
    for record in suplr_strt_res[DATA][RECORDS]:
        if skuCode is not None and skuCode in record:
            if type(bill_list) == int:
                bill_list += record[skuCode]
            elif type(bill_list) == list:
                bill_list.append(record[skuCode])
        else:
            bill_list.append(record)
    startPage += 1
    while suplr_strt_res[DATA]["total"] > (startPage - 1) * pageSize:
        print(startPage)
        body["current"] = startPage
        return getbilllistswithprop(url, body, bill_list, skuCode)

    return bill_list


def getAllbilllist(skuCode, status, billlist):
    for status in status:
        billlist = getBillLists(HEAD_SUPPLYSTRAIGHT_LIST_ALL_URL, HEAD_SUPPLYSTRAIGHT_LIST_ALL_PARA_BODY,
                                1, 100, status, billlist, skuCode)
        billlist = getBillLists(HEAD_DEPOTRESERVATION_LIST_URL, HEAD_DEPOTRESERVATION_PARA_BODY,
                                1, 100, status, billlist, skuCode)

    return billlist


def getWmsStoregeStock(skucCode, warehouseCode, type):
    url = getApiList(WMS_STORAGE_INV_URL)
    body = getApiList(WMS_STORAGE_INV_PARA_BODY)
    body[SKUCODE] = skucCode
    body[WHCODE] = warehouseCode
    if type == "int":
        res = getbilllistswithprop(url, body, 0, "invQty")
    else:
        res = getbilllistswithprop(url, body, [], None)
    print(skucCode, "_", res)
    return res


def getInvstockbySku(skucode, whcode):
    body = getApiList()[INV_STOCK_QUERY_PARA_BODY]
    body["skuCode"] = skucode
    body["warehouseCode"] = whcode
    response = requests.post(getApiList()[INV_STOCK_QUERY_URL], json=body, headers=getHeaders())
    # print(response.text)
    resultj = json.loads(response.text)
    if resultj["code"] == 200 and len(resultj["data"]["records"]) > 0:
        return resultj["data"]["records"][0]
    return resultj






def getOccpyBySku(skuCode,oldSkuCode, whcode,biztype):
    body = getApiList()[INV_OCCPY_PARA_BODY]
    body["skuCode"] = skuCode
    body["oldSkuCode"] = oldSkuCode
    body["whCode"] = whcode
    bizTypeList = []
    bizTypeList.append(biztype)
    body["bizTypeList"] = bizTypeList
    response = requests.post(getApiList()[INV_OCCPY_URL], json=body, headers=getHeaders())
    # print(response.text)
    resultj = json.loads(response.text)
    if resultj["code"] == 200 and len(resultj["data"]["records"]) > 0:
        return resultj["data"]["records"]
    return resultj



storelist = """
{"FBA-25-EU":"11366",
"FBA-25-UK":"11367",
"FBA-01":"10333",
"FBA-02":"10334",
"FBA-03":"10335",
"FBA-04":"10336",
"FBA-05":"10337",
"FBA-06":"10338",
"FBA-07":"10339",
"FBA-08":"10340",
"FBA-04-CA":"10341",
"eBay":"10415",
"FBA-09":"10417",
"FBA-10":"10418",
"FBA-11":"10440",
"FBA-12":"10441",
"FBA-13":"10442",
"FBA-14":"10443",
"FBA-15":"10468",
"FBA-16":"10469",
"FBA-17":"10470",
"FBA-18":"10471",
"FBA-19":"10479",
"FBA-20":"10506",
"FBA-21":"10537",
"FBA-22-UK":"10887",
"WFS-01":"10906",
"FBA-22-EU":"11104",
"FBA-01-DI":"11131",
"CG-01":"11154",
"FBA-01-UK-DI":"11349",
"FBA-01-EU-DI":"11350",
"FBA-26-UK":"11351",
"FBA-26-EU":"11352",
"FBA-27-UK":"11823",
"FBA-27-EU":"11824"


}

"""


def getstorelist():
    storelist_json = json.loads(storelist)
    return storelist_json


platformlist = """
{
"Amazon":"10002",
"ebay":"10001"
}

"""


def getplatformlist():
    storelist_json = json.loads(platformlist)
    return storelist_json


def getApiList(para_str=None):
    apiList = ''
    with open('api_list', 'r', encoding='utf-8') as file:
        # content = file.read()  # 一次性读取整个文件内容
        # 或者使用以下方式逐行读取
        for line in file:
            apiList += line
    apiList = json.loads(apiList)
    if para_str is not None:
        return apiList[para_str]
    return apiList


def getskuList():
    sku_str_list = ''
    with open('sku_list_log_0', 'r', encoding='utf-8') as file:
        # content = file.read()  # 一次性读取整个文件内容
        # 或者使用以下方式逐行读取
        for line in file:
            sku_str_list += line
    return sku_str_list


def getBillList():
    bill_list = ''
    with open('orders_list', 'r', encoding='utf-8') as file:
        # content = file.read()  # 一次性读取整个文件内容
        # 或者使用以下方式逐行读取
        for line in file:
            bill_list += line
        # print(bill_list)
    return bill_list


def getwarehouse_list():
    warehouseList = json.loads(warehouse_codes)
    return warehouseList


OPERTYPE = """
{
"QCO_HOLD":"QCO",
"GOOD_PUTAWAY_HOLD":"PUTAWAY",
"BAD_PUTAWAY_HOLD":"PUTAWAY",
"GOOD_SHIP_HOLD":"SHIP_HOLD",
"GOOD_OUT_HOLD":"HOLD",
"BAD_OUT_HOLD":"HOLD"

}

"""


def getOperType():
    opertype = json.loads(OPERTYPE)
    return opertype


FILE_PROFIX = "D:/file/python_result/"



SKU_EXAM_STR = """
{
			"badHoldQty": 0,
			"badQty": 0,
			"freezeQty": 0,
			"holdQty": 0,
			"inTransitQty": 0,
			"oldSkuCode": "FTPLPB-0183",
			"platform": "10001",
			"site":"US",
			"skuCode": "FTPLPB-0183",
			"store": "10415",
			"totalQty": 1,
			"useQty": 1
		}
"""


OTHER_INBOUND = """
{
	"billNo": "RD24060414077",
	"billStatusEnum": "FINISH",
	"billTime": "2024-06-04T06:47:56.982",
	"billTypeEnum": "OTHER_INBOUND",
	"operationTypeEnum": "NULL",
	"originBillNo": "RD24060414077",
	"skuList": [
		{
			"badHoldQty": 0,
			"badQty": 0,
			"freezeQty": 0,
			"holdQty": 0,
			"inTransitQty": 0,
			"oldSkuCode": "FTPLPB-0183",
			"platform": "10001",
			"site":"US",
			"skuCode": "FTPLPB-0183",
			"store": "10415",
			"totalQty": 1,
			"useQty": 1
		}
	],
	"warehouseCode": "11"
}
"""

OTHER_OUTBOUND = """
{
	"billNo": "SHBLDB24060300025",
	"billStatusEnum": "FINISH",
	"billTime": "2024-06-03T15:27:22.972",
	"billTypeEnum": "OTHER_OUTBOUND",
	"operationTypeEnum": "NULL",
	"originBillNo": "SHBLDB24060300025",
	"skuList": [
		{
			"badHoldQty": 0,
			"badQty": 0,
			"freezeQty": 0,
			"holdQty": -1,
			"inTransitQty": 0,
			"oldSkuCode": "HEFTVT-P025",
			"platform": "10001",
			"site":"US",
			"skuCode": "HEFTVT-P025",
			"store": "10415",
			"totalQty": -1,
			"useQty": 0
		}
	],
	"warehouseCode": "04"
}
"""

HEAD_TRANS_SHIPOUT = """
{
	"operationTypeEnum": "SHIP_HOLD",
	"skuList": [
		{
			"freezeQty": 0,
			"holdQty": -50,
			"useQty": 0,
			"totalQty": -50,
			"inTransitQty": 0,
			"store": "10415",
			"platform": "10001",
			"site":"US",
			"badQty": 0,
			"oldSkuCode": "FTHKAM-1002",
			"skuCode": "FTHKAM-1002",
			"badHoldQty": 0
		}
	],
	"originBillNo": "2404H-G53-CA03",
	"warehouseName": "佛山集散仓",
	"cooperator": "赢他",
	"billTypeEnum": "WMS_STRAIGHT_WAREHOUSRE",
	"warehouseCode": "58",
	"billTime": 1714992127000,
	"whType": "oneself",
	"billNo": "2404H-G53-CA03",
	"billStatusEnum": "FINISH"
}
"""

HEAD_SHIPMENT = """
{
	"billNo": "2404H-G160-CA03",
	"billStatusEnum": "FINISH",
	"billTime": "2024-05-23T15:11:53",
	"billTypeEnum": "HEAD_SHIPMENT",
	"cooperator": "赢他",
	"operationTypeEnum": "HEAD_IN_TRANSIT",
	"originBillNo": "2404H-G160-CA03",
	"skuList": [
		{
			"badHoldQty": 0,
			"badQty": 0,
			"freezeQty": 0,
			"holdQty": 0,
			"inTransitQty": 89,
			"oldSkuCode": "FTOFOD-6034",
			"platform": "10001",
			"site":"US",
			"skuCode": "FTOFOD-6034",
			"store": "10415",
			"totalQty": 0,
			"useQty": 0
		}
	],
	"warehouseCode": "110",
	"warehouseName": "加州3号仓",
	"whType": "oneself"
}

"""

SALES_ORDER_JIE_DAN = """
{
	"billNo": "GOC65167864",
	"billStatusEnum": "FINISH",
	"billTime": "2024-05-31T12:00:06.912",
	"billTypeEnum": "SALE_OUTBOUND_ORDERS",
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
			"platform": "10001",
			"site":"US",
			"skuCode": "OETETA-0016",
			"store": "10415",
			"totalQty": 0,
			"useQty": 1
		}
	],
	"warehouseCode": "18"
}
"""

SALES_ORDER_OUT = """
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
			"site":"US",
			"skuCode": "OETETA-0016",
			"store": "10339",
			"totalQty": -1,
			"useQty": 0
		}
	],
	"warehouseCode": "18"
}
"""

warehouse_codes = """{"01": "上海集散仓", "2": "头程海运虚拟仓", "3": "上海待质检仓", "4": "上海不良品仓","5": "虚拟报废仓","06": "百世詹姆斯堡正品仓",
"10": "百世洛杉矶正品仓","11": "西雅图正品仓","7": "西雅图二手件仓","9": "西雅图配件仓","8": "西雅图报废仓","12": "FBA-01","13": "FBA-02",
"14": "FBA-03","15": "FBA-04","16": "FBA-05","17": "FBA-06","18": "FBA-07","19": "调拨虚拟仓","20": "FBA-04-CA",
"21": "华南工厂虚拟仓","22": "华东工厂虚拟仓","23": "新泽西正品仓","24": "FBA-08","25": "FBA-09","26": "YITALLC","27": "头程空运虚拟仓",
"28": "FBA-10","29": "无忧达亚特兰大","30": "上海不良品业务仓","31": "FBA-11","32": "FBA-12","33": "FBA-13","34": "FBA-14",
"35": "新泽西二手件仓","36": "上海集散仓-样品仓","37": "西雅图-不良品仓","38": "西雅图二手件-不良品仓","39": "新泽西-不良品仓","40": "FBA-15",
"41": "FBA-16","42": "FBA-17","43": "FBA-18","44": "FBA-19","45": "百世詹姆斯堡-不良品仓","46": "百世洛杉矶-不良品仓",
"47": "无忧达亚特兰大-不良品仓","48": "FBA-20","49": "FBA-21","50": "亚特兰大美南正品仓","51": "新泽西二手件-不良品仓","52": "亚特兰大美南二手件",
"53": "亚特兰大美南-不良品仓","54": "洛杉矶正品仓","55": "洛杉矶不良品仓","56": "FBA-22-UK","57": "WFS-01","58": "佛山集散仓","59": "佛山不良品仓",
"60": "佛山不良品业务仓","61": "NJ正品仓","62": "NJ-不良品仓","63": "TX正品仓","64": "TX-不良品仓","65": "FBA-22-EU","66": "FBA-01-DI",
"67": "4PX-德国法兰克福正品仓","68": "4PX-德国法兰克福-不良品仓","69": "4PX-英国莱切斯特正品仓","70": "4PX-英国莱切斯特-不良品仓","71": "CG-01",
"72": "WFS-02","73": "FBA-26-UK","74": "FBA-26-EU","75": "FBA-01-EU-DI","76": "FBA-01-UK-DI","77": "FBA-25-EU",
"78": "FBA-25-UK","79": "CG-02","80": "加州2号仓","81": "加州2号仓不良品仓","82": "FBA-01-EU","83": "FBA-01-UK","84": "ONUS-ONT",
"85": "ONUS-ONT-DS","86": "ONUS-CHINO","87": "ONUS-CHINO-DS","88": "ONUS-NJ-001","89": "ONUS-NJ-001-DS",
"90": "ONUS-NJ-002","91": "ONUS-NJ-002-DS","92": "ONUS-GA","93": "ONUS-GA-DS","94": "Dewell-NJ","95": "Dewell-NJ-DS",
"96": "德州2号仓","97": "德州2号仓不良品仓","98": "龙辕-CA","99": "龙辕-NJ","100": "龙辕-CA-DS","101": "龙辕-NJ-DS","102": "DUKE-ONT",
"103": "DUKE-ONT-DS","104": "Best-CA","105": "Best-CA-DS","106": "Best-NJ","107": "Best-NJ-DS","108": "中链英国仓",
"109": "中链英国仓-DS","110": "加州3号仓","111": "加州3号仓不良品仓","112": "亚特兰大2号仓","113": "亚特兰大2号仓不良品仓","114": "FBA-02-CA",
"115": "谷仓德国3仓良品仓","116": "谷仓德国3仓不良品仓","117": "谷仓英国16仓良品仓","118": "谷仓英国16仓不良品仓","119": "谷仓德国1号仓良品仓",
"120": "谷仓德国1号仓不良品仓","121": "FBA-27-UK","122": "FBA-27-EU","123": "谷仓德国7号仓良品仓","124": "谷仓德国7号仓不良品仓"}"""

PURCHASE_PRODUCE_TRANSIT = """
{
	"billNo": "ZPO24030400689",
	"billStatusEnum": "FINISH",
	"billTime": "2024-06-12T04:03:29.037",
	"billTypeEnum": "TMS_STRAIGHT_WAREHOUSRE",
	"operationTypeEnum": "PUR_PRODUCE_IN_TRANSIT",
	"originBillNo": "2405H-G76-CA03",
	"repairOpt": false,
	"skuList": [
		{
			"badHoldQty": 0,
			"badQty": 0,
			"freezeQty": 0,
			"holdQty": 0,
			"inTransitQty": 8,
			"oldSkuCode": "CETCTC-6035",
			"platform": "10001",
			"site":"US",
			"skuCode": "CETCTC-6035",
			"store": "10415",
			"totalQty": 0,
			"useQty": 0
		}
	],
	"warehouseCode": "01"
}
"""

PURCHASE_RECEIVE_TRANSIT = """ 
{
	"billNo": "2406H-G142-GA02",
	"billStatusEnum": "FINISH",
	"billTime": "2024-06-14T13:19:00.329",
	"billTypeEnum": "TMS_STRAIGHT_WAREHOUSRE",
	"operationTypeEnum": "PUR_RECEIVE_IN_TRANSIT",
	"originBillNo": "2406H-G142-GA02",
	"repairOpt": false,
	"skuList": [
		{
			"badHoldQty": 0,
			"badQty": 0,
			"freezeQty": 0,
			"holdQty": 0,
			"inTransitQty": -100,
			"oldSkuCode": "BFTLPT-2011",
			"platform": "10001",
			"site":"US",
			"skuCode": "BFTLPT-2011",
			"store": "10415",
			"totalQty": 0,
			"useQty": 0
		}
	],
	"warehouseCode": "01"
}

"""
