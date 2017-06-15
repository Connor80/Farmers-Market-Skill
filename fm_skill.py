from bs4 import BeautifulSoup
import urllib.request
import csv
import itertools
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")

hours = []
vendor = []

@ask.launch
def new_ask():
    welcome = render_template('welcome')
    reprompt = render_template('reprompt')
    return question(welcome) \
        .reprompt(reprompt)

def processVendorName(v):
    vendorSynonymDict = {}
    vendorSynonymDict['popcorn'] = "doc popcorn"
    vendorSynonymDict['Mexican'] = "taqueria la ventana"
    if v in vendorSynonymDict:
        return vendorSynonymDict[v]
    else:
        return v

def getHours(v):
    url = 'https://dallasfarmersmarket.org/directory/{}'.format(v).replace(" ", "-")
    headers = {}
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    r = urllib.request.urlopen(req)
    soup = BeautifulSoup(r, "lxml")

    url_hours = soup.find("div", {"class":"w2dc-field-output-block-9"}).get_text().replace("\n", " ").replace("\t", " ").replace("\r", " ").replace("\s+", " ").encode('ascii', 'ignore').decode('ascii')
    url_vendor = soup.find("h2", {"itemprop":"name"}).get_text().encode('ascii', 'ignore').decode('ascii')
    hours.append(url_hours)
    vendor.append(url_vendor)
    for m, n in list(zip(hours,vendor)):
        list1 = (n,m)
    return list1



@ask.intent('VendorHoursIntent')
def stateHours(v):
    if (v is None):
        reprompt_show = render_template("reprompt_vendor")
        return question(reprompt_vendor)
    else:
        filVendor = processVendorName(v)
        hours = getHours(filVendor)
        v_name = hours[0]
        v_hours = hours[1]
        if ("Hours:" in v_hours):
            v_hours = v_hours.replace("Hours:", "")
        vendorHours_msg = render_template('vendor_hours', v=v, v_name = v_name, v_hours = v_hours)#, list1=list1)
        return statement(vendorHours_msg)

if __name__ == '__main__':
    app.run(debug=True)
