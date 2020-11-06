import feedparser
from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import redirect
from flask import url_for
from flask import session

import datetime
import json
import urllib.request

app = Flask(__name__)
app.secret_key = 'jXn2r5u8x/A?D(G+KbPeShVmYp3s6v9y'

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=cb932829eacb6a0e9ee4f38bfbf112ed"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=b23c94daab584f4580e4e2bf75cbcf7e"

DEFAULTS = {'publication': 'bbc',
            'city': 'Seoul,KR',
            'currency_from': 'USD',
            'currency_to': 'KRW'
            }
CURRENCIES = ['USD', 'KRW','GBP','EUR','JPY']

def get_value_with_fallback(key):
    if request.form.get(key):
        return request.form.get(key)
    elif session.get('sessionObj'):
        return session['sessionObj'][key]
    else:
        return DEFAULTS[key]


@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        # get customised headlines, based on user input or default
        publication = get_value_with_fallback("publication")
        city = get_value_with_fallback("city")
        currency_from = get_value_with_fallback("currency_from")
        currency_to = get_value_with_fallback("currency_to")
        
        sessionObj = {
            'publication':publication, 
            'city':city, 
            'currency_from':currency_from, 
            'currency_to':currency_to,
            }
        print ('POST -- sessionObj=', sessionObj)        
        session['sessionObj'] = sessionObj
        return redirect(url_for('home')) # GET Method

    # no cookies used
    if session.get('sessionObj') is None:
        session['sessionObj'] = DEFAULTS

    sessionObj = session['sessionObj']
    publication = sessionObj["publication"]
    city = sessionObj["city"]
    currency_from = sessionObj["currency_from"]
    currency_to = sessionObj["currency_to"]
                
    print('Return -- sessionObj=',sessionObj)
    # return template
    articles = get_news(publication)
    weather = get_weather(city)
    rate, currencies = get_rate(currency_from, currency_to)
    
    response = render_template("home.html", 
                               articles=articles,
                               weather=weather, 
                               currency_from=currency_from,
                               currency_to=currency_to, 
                               rate=rate, 
                               currencies=sorted(CURRENCIES))
    return response


def get_rate(frm, to):
    all_currency = urllib.request.urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency.decode('utf-8')).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate / frm_rate, parsed.keys())


def get_news(publication):
    feed = feedparser.parse(RSS_FEEDS[publication.lower()])
    return feed['entries']


def get_weather(query):
    query = urllib.parse.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data.decode('utf-8'))
    weather = None
    if parsed.get('weather'):
        weather = {'description': parsed['weather'][0]['description'],
                   'temperature': parsed['main']['temp'],
                   'city': parsed['name'],
                   'country': parsed['sys']['country']
                   }
    return weather

if __name__ == "__main__":
    app.run(port=5000, debug=True)
