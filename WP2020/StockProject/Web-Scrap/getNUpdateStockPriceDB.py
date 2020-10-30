# -*- coding: utf-8 -*-
'''
Created on 2019. 1. 10.

@author: cskim
'''
import numpy as np
import pandas as pd
from datetime import datetime

import mysql.connector
import urllib.request
import xml.etree.ElementTree as ET

import dbconfig

XMLDIR = 'C:\\Temp\\xml-all'

def connect():
    return mysql.connector.connect(
    host=dbconfig.db_host, 
    user=dbconfig.db_user, 
    password=dbconfig.db_password,
    database=dbconfig.db_name)

conn = connect()
cursor = conn.cursor()
code_list = []
priceDF = pd.DataFrame(columns=['date', 'code', 'name', 
                                'open_price', 'high_price', 'low_price', 'close_price', 
                                'cap_amount', 'volume', 'tot_amount'],)

def convertDate8To10(date8):
    dstr = date8.split('/')
    yy = '20'+dstr[0]
    return '20%s-%s-%s' % (dstr[0], dstr[1], dstr[2])

def getPortCodeList():
    global code_list
    query = 'select port_code from univ_port_table'
    cursor.execute (query)
    
    for row in cursor:
        code_list.append(row[0][1:])
    
def getStockPriceXMLFiles():
    global XMLDIR
    global code_list
        
    for scode in code_list:
        url = "http://asp1.krx.co.kr/servlet/krx.asp.XMLSiseEng?code=%s" % scode
        fp = urllib.request.urlopen(url)
        xmlbytes = fp.read()
        xmlstr = xmlbytes.decode("utf8")
        fp.close()
        with open("%s\\xml_%s.xml" % (XMLDIR,scode), "w") as text_file:
            text_file.write(xmlstr)

def buildPriceDFFromXML(code):
    global XMLDIR
    global priceDF
    
    xmlfile_name = "%s/xml_%s.xml" % (XMLDIR,code)
    #print (xmlfile_name)
    with open(xmlfile_name, mode='rt') as xml_file:
        xmldoc = xml_file.read()
        #print(xmldoc)
        root = ET.fromstring(xmldoc.strip())
    
        si = root.find('TBL_StockInfo')
        st_amount = 0 if si.attrib['Amount']=='' else int(si.attrib['Amount'].replace(',', ''))
        st_name = si.attrib['JongName']
        for ds in root.iter('DailyStock'):
            pr = {'code':code, 'name':st_name}
            pr['date'] = convertDate8To10(ds.attrib['day_Date'])
            pr['open_price'] = int(ds.attrib['day_Start'].replace(',', ''))
            pr['high_price'] = int(ds.attrib['day_High'].replace(',', ''))
            pr['low_price'] = int(ds.attrib['day_Low'].replace(',', ''))
            pr['close_price'] = int(ds.attrib['day_EndPrice'].replace(',', ''))
            pr['cap_amount'] = None if st_amount==None else int(st_amount * pr['close_price'] / 1000000)
            pr['volume'] = int(ds.attrib['day_Volume'].replace(',', ''))
            pr['tot_amount'] = st_amount
            #print (pr)
            priceDF = priceDF.append(pr, ignore_index=True)

def buildPriceDFFromXMLFiles():
    global code_list
    
    for scode in code_list:
        buildPriceDFFromXML(scode)



if __name__ == "__main__":
    getPortCodeList()
    print ("Get Stock Price XML Files")
    getStockPriceXMLFiles()
    print ("Build Stock PriceDF")
    buildPriceDFFromXMLFiles()
    #print (priceDF.head(10))
    #print (priceDF.tail(10))
    #print (priceDF.dtypes)
    print ("Update Stock Price DB")
    #updateStockPriceDB()