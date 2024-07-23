import datetime
import json
import time

import pandas as pd

import commonUtil as cu


import requests
import json


def delete_redi_key():
    key_prefix = "INV:SALES:RULE:INFO::rule_USTemu"
    keylist=[]

    for i in range(1,51):
        key_str = key_prefix + str(i)
        keylist.append(key_str)
        i+=1
    print(keylist)
    res = cu.deleteKeyRedis(keylist)
    print(res)

#print(cu.getWmsStoregeStock("FTPLPB-0274","112","obj"))


bill_list = cu.getTransBillList()
bill_list = json.loads(bill_list)

cu.get



# delete_redi_key()