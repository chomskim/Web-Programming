#-*- coding: utf-8 -*-
'''
Created on 2018. 4. 27.

@author: cskim
'''
from dbhelper import DBHelper

DB = DBHelper()

for k in DB.name2CodeMap:
    print (k, DB.name2CodeMap[k])
    
from base64 import b64encode
import os   
print (b64encode(os.urandom(24)).decode('utf-8'))