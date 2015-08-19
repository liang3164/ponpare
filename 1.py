# -*- coding: utf-8 -*-
### Kaggle Scripts: Ponpare Coupon Purchase Prediction ###
### Author: MichelJ ###

# Read the data files, using Pandas, and do some simple processing

import os
import math
import pandas as pd
import numpy as np



#read in all the input data
cpdtr = pd.read_csv("./input/coupon_detail_train.csv")
cpltr = pd.read_csv("./input/coupon_list_train.csv")
cplte = pd.read_csv("./input/coupon_list_test.csv")
ulist = pd.read_csv("./input/user_list.csv")
areas = pd.read_csv("./input/prefecture_locations.csv")
cpvtr = pd.read_csv("./input/coupon_visit_train.csv", names = ['PURCHASE_FLG','I_DATE','PAGE_SERIAL','REFERRER_hash','VIEW_COUPON_ID_hash','USER_ID_hash','SESSION_ID_hash','PURCHASEID_hash'])


# def load_merged_actions():
#
# 	rs_dict = {}
#
#
# 	for i in len(cpvtr):
#
# 		u_id = cpvtr['USER_ID_hash'][i]
# 		coupon_id = cpvtr['VIEW_COUPON_ID_hash'][i]
# 		flg = cpvtr['PURCHASE_FLG'][i]
#
# 		if (u_id, coupon_id) not in rs_dict:
#             rs_dict[(u_id, coupon_id)] = []
# 		rs_dict[(u_id, coupon_id)].append(flg)
#     return rs_dict
#

## from datetime import datetime
## date_object = datetime.strptime('2011-02-14 12:07:22', '%Y-%m-%d %H:%M:%S')




