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
cr_name = []
cr_hours = []
c_r = []

@ask.launch
def new_ask():
    welcome = render_template('welcome')
    reprompt = render_template('reprompt')
    return question(welcome) \
        .reprompt(reprompt)

@ask.intent('WakeIntent')
def wake():
    welcome = render_template('welcome')
    reprompt = render_template('reprompt')
    return question(welcome) \
        .reprompt(reprompt)

def processVendorName(v):
    vendorSynonymDict = {}
    vendorSynonymDict['popcorn'] = "doc popcorn"
    vendorSynonymDict['Mexican'] = "taqueria la ventana"
    vendorSynonymDict['ice cream'] = "coolhaus"
    vendorSynonymDict['pizza'] = "Cane Rosso"
    if v in vendorSynonymDict:
        return vendorSynonymDict[v]
    else:
        return v

def getHours(v):
    if v == "Cane Rosso":
        url = 'http://www.canerosso.com/deep-ellum'
        req = urllib.request.Request(url)
        r = urllib.request.urlopen(req)
        soup = BeautifulSoup(r, "lxml")
        rosso_hours = soup.find("div", {"class":"html-block"}).get_text() \
            .replace(";", " and").replace("Mon", "Monday").replace("Thurs", "Thursday") \
            .replace("Wed", "Wednesday").replace(":", " ").replace("BRUNCH", "Brunch is ") \
            .replace("HAPPY HOUR", "Happy Hour is ").replace("PM", "PM. ") \
            .replace("and", "for lunch, then re open for dinner from") \
            .replace("PMFri", "PM Friday").replace("Sat", "Saturday").replace("Sun", "Sunday") \
            .replace("HOURS", "").replace("Fri", "Friday").replace("-", " to ") \
            .replace("Monday to Thursday", "Monday through Thursday,") \
            .replace("Monday to Wednesday", "Monday through Wednesday,") \
            .replace("Saturday to Sunday", "Saturday and Sunday,")
        rosso_name = soup.find("div", {"id":"OT_logoLink"}).get_text() \
            .replace(" - Deep Ellum (188800), Dallas - Fort Worth Reservations", "")
        cr_name.append(rosso_name)
        cr_hours.append(rosso_hours)
        for m, n in list(zip(cr_name, cr_hours)):
            c_r = (m,n)
        return c_r
    else:
        url = 'https://dallasfarmersmarket.org/directory/{}'.format(v).replace(" ", "-")
        headers = {}
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        r = urllib.request.urlopen(req)
        soup = BeautifulSoup(r, "lxml")

        url_hours = soup.find("div", {"class":"w2dc-field-output-block-9"}).get_text() \
            .replace("\n", " ").replace("\t", " ").replace("\r", " ") \
            .replace("\s+", " ").encode('ascii', 'ignore').decode('ascii')
        url_vendor = soup.find("h2", {"itemprop":"name"}).get_text() \
            .encode('ascii', 'ignore').decode('ascii')
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
    elif v == "Cane Rosso":
        filVendor = processVendorName(v)
        hours = getHours(filVendor)
        v_name = cr_name[0]
        v_hours = cr_hours[0]
        vendorHours_msg = render_template('vendor_hours', v=v, v_name = v_name, v_hours = v_hours)
        return statement(vendorHours_msg) \
            .standard_card(title='Cane Rosso',
                       text=v_hours,
                       small_image_url='https://static1.squarespace.com/static/55c9f9bce4b0423ff5aafd5f/55c9fe36e4b0e3531a263a71/55e61d42e4b0143776db8162/1441144132245/IlCaneRossoLogo_Red+with+Type_Woodcut_Vertical-01.jpg?format=500w')
    else:
        filVendor = processVendorName(v)
        hours = getHours(filVendor)
        v_name = hours[0]
        v_hours = hours[1]
        if ("Hours:" in v_hours):
            v_hours = v_hours.replace("Hours:", "")
        vendorHours_msg = render_template('vendor_hours', v=v, v_name = v_name, v_hours = v_hours)
        return statement(vendorHours_msg) \
            .standard_card(title=v_name,
                       text=v_hours,
                       small_image_url='https://pbs.twimg.com/profile_images/507678913531633665/vz6QhK_B.jpeg',
                       large_image_url='https://dallasfarmersmarket.org/wp-content/uploads/2015/11/the-market-map.jpg')

if __name__ == '__main__':
    app.run(debug=True)
