import datetime
import json
import time

from openpyxl import Workbook

from openpyxl import load_workbook

import pandas as pd

import commonUtil as comu
import requests
import json


res = comu.getWmsStoregeStock("FRSSPF-0177","01","int")
print(res)