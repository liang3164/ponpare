# -*- coding: utf-8 -*-
### Kaggle Scripts: Ponpare Coupon Purchase Prediction ###
### Author: MichelJ ###

# Read the data files, using Pandas, and do some simple processing

import os
import math
import pandas as pd
import numpy as np



#read in all the input data
# cpdtr <- read.csv("../input/coupon_detail_train.csv")
# cpltr <- read.csv("../input/coupon_list_train.csv")
# cplte <- read.csv("../input/coupon_list_test.csv")
# ulist <- read.csv("../input/user_list.csv")
cpdtr = pd.read_csv("./input/coupon_detail_train.csv", names = ['ITEM_COUNT','I_DATE','SMALL_AREA_NAME','PURCHASEID_hash','USER_ID_hash','COUPON_ID_hash'])
cpltr = pd.read_csv("./input/coupon_list_train.csv")
cplte = pd.read_csv("./input/coupon_list_test.csv")
ulist = pd.read_csv("./input/user_list.csv")
areas = pd.read_csv("./input/prefecture_locations.csv")
cpvtr = pd.read_csv("./input/coupon_visit_train.csv", names = ['PURCHASE_FLG','I_DATE','PAGE_SERIAL','REFERRER_hash','VIEW_COUPON_ID_hash','USER_ID_hash','SESSION_ID_hash','PURCHASEID_hash'])


#making of the train set
train = cpdtr,cpltr
train = train["COUPON_ID_hash","USER_ID_hash",
                  "GENRE_NAME","DISCOUNT_PRICE","PRICE_RATE",
                  "USABLE_DATE_MON","USABLE_DATE_TUE","USABLE_DATE_WED","USABLE_DATE_THU",
                  "USABLE_DATE_FRI","USABLE_DATE_SAT","USABLE_DATE_SUN","USABLE_DATE_HOLIDAY",
                  "USABLE_DATE_BEFORE_HOLIDAY","ken_name","small_area_name"]
#combine the test set with the train
cplte$USER_ID_hash <- "dummyuser"
cpchar <- cplte[,c("COUPON_ID_hash","USER_ID_hash",
                   "GENRE_NAME","DISCOUNT_PRICE","PRICE_RATE",
                   "USABLE_DATE_MON","USABLE_DATE_TUE","USABLE_DATE_WED","USABLE_DATE_THU",
                   "USABLE_DATE_FRI","USABLE_DATE_SAT","USABLE_DATE_SUN","USABLE_DATE_HOLIDAY",
                   "USABLE_DATE_BEFORE_HOLIDAY","ken_name","small_area_name")]

train <- rbind(train,cpchar)
#NA imputation
train[is.na(train)] <- 1
#feature engineering
train$DISCOUNT_PRICE <- 1/log10(train$DISCOUNT_PRICE)
train$PRICE_RATE <- (train$PRICE_RATE*train$PRICE_RATE)/(100*100)
#convert the factors to columns of 0's and 1's
train <- cbind(train[,c(1,2)],model.matrix(~ -1 + .,train[,-c(1,2)],
                                                    contrasts.arg=lapply(train[,names(which(sapply(train[,-c(1,2)], is.factor)==TRUE))], contrasts, contrasts=FALSE)))

#separate the test from train
test <- train[train$USER_ID_hash=="dummyuser",]
test <- test[,-2]
train <- train[train$USER_ID_hash!="dummyuser",]

#data frame of user characteristics
uchar <- aggregate(.~USER_ID_hash, data=train[,-1],FUN=mean)
uchar$DISCOUNT_PRICE <- 1
uchar$PRICE_RATE <- 1

#Weight Matrix: GENRE_NAME DISCOUNT_PRICE PRICE_RATE USABLE_DATE_ ken_name small_area_name
require(Matrix)
W <- as.matrix(Diagonal(x=c(rep(3,13), rep(1,1), rep(0,1), rep(0,9), rep(3,47), rep(4,55))))

#calculation of cosine similairties of users and coupons
score = as.matrix(uchar[,2:ncol(uchar)]) %*% W %*% t(as.matrix(test[,2:ncol(test)]))
#order the list of coupons according to similairties and take only first 10 coupons
uchar$PURCHASED_COUPONS <- do.call(rbind, lapply(1:nrow(uchar),FUN=function(i){
  purchased_cp <- paste(test$COUPON_ID_hash[order(score[i,], decreasing = TRUE)][1:10],collapse=" ")
  return(purchased_cp)
}))

#make submission
submission <- merge(ulist, uchar, all.x=TRUE)
submission <- submission[,c("USER_ID_hash","PURCHASED_COUPONS")]
write.csv(submission, file="cosine_sim.csv", row.names=FALSE)
