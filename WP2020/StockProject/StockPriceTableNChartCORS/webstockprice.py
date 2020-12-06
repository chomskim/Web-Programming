'''
Created on 2018. 11. 18.

@author: cskim
'''
import os
import uuid

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from flask import Flask
from flask import render_template
from flask import url_for
from flask import session
from flask import jsonify
from flask import make_response
from flask import request

import json
import urllib.parse
from urllib.request import urlopen

import utils

UAMP = '\uFF06' # 2-byte '&' 
try:
    font_name = matplotlib.font_manager.FontProperties(fname="./static/fonts/malgun.ttf").get_name()
    plt.rcParams['font.family'] = font_name
    #print ("font_name=%s" % font_name)
except:
    font_name = 'sans-serif'
    plt.rcParams['font.family'] = font_name
    plt.rcParams['font.sans-serif'] = ['Tahoma', 'DejaVu Sans', 'Lucida Grande', 'Verdana']
plt.rcParams["figure.figsize"] = (6.4, 4.8)

app = Flask(__name__)
app.secret_key = 'StvaKy0d9ebU8LfOWX6rBazllGizVNxf'

#GETPRICE_URL = "http://localhost:5008/getprice/{}"
#GETPRICE_URL = "http://192.168.100.193/stockapi/getprice/{}"
GETPRICE_URL = "http://220.67.121.119/stockapi/getprice/{}"

@app.route("/")
def home():
    #print("--request.headers--")
    #print(request.headers)
    response = make_response(render_template("home.html", stockNames=utils.stockNames))
    response.headers['Access-Control-Allow-Origin'] = '*'
    #print("--response.headers--")
    #print(response.headers)
    return response

@app.route("/getprice/")
@app.route("/getprice/<days>")
def getprice(days=""):
    session['ndays'] = 30 if days == "" else int(days)
    url = GETPRICE_URL.format(days)
    print (url, "<{}>".format(days))
    priceJson = urlopen(url).read().decode("utf-8")
    print (priceJson)
    
    priceDF = pd.read_json(priceJson, orient='split')
    headList = ['date'] + list(priceDF.columns)
    rowList = []
    for da in priceDF.index:
        pr_list = priceDF.loc[da]
        strpr_list = ['{:.0f}'.format(pr) for pr in pr_list]
        row = [da]+strpr_list
        rowList.append(row)
    
    return jsonify({ 'head':headList, 'rows':rowList })

@app.route("/getplot/<query>")
def getplot(query):
        
    svg = ''
        
    if not session.get('uid'):
        session['uid'] = uuid.uuid4()
    #print ("session['uid']=%s"%session['uid'])
        
    if session.get('ndays'):
        days = session.get('ndays')
    else:
        days = 30    
    print ("<query={}><days={}>".format(query, days))
    
    selList = query.split('&')        
    if not set(selList).issubset(utils.stockNames):
        #print (selList)
        return {'svg': svg}
        
    url = GETPRICE_URL.format(days)
    print ("<url={}><days={}>".format(url, days))
    priceJson = urlopen(url).read().decode("utf-8")
    #print (priceJson)
    
    priceDF = pd.read_json(priceJson, orient='split')
    #print(priceDF)
    
    selList = [co.replace('KT'+ UAMP+'G', 'KT&G') for co in selList]
    drawDF = priceDF[selList].astype(int)
    drawDF.plot.line()
    
    tempSvgFile = './static/temp/plot_%s.svg'%session['uid']
    plt.savefig(tempSvgFile, format='svg')
    #plt.savefig('./static/price_plot.png', format='png')
    with open(tempSvgFile, 'rt', encoding='UTF8') as svgfile:
        svg = svgfile.read()
        #print ({'svg': svg})
    """
    try:
        os.remove(tempSvgFile)
    except OSError as e:
        #print ("SVG File Read Error: %s - %s." % (e.filename, e.strerror))
        pass
    #"""
    #return send_file('./static/price_plot.png', mimetype='image/png')
    return jsonify({'svg': svg})
    
    
if __name__ == '__main__':
    app.run(port=5001, debug=True)
