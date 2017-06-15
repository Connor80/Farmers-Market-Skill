from bs4 import BeautifulSoup
import requests
import csv
import itertools

v = "Popcorn"
hours = []
vendor = []

def processVendorName(v):
    vendorSynonymDict = {}
    vendorSynonymDict['Popcorn'] = "Doc-Popcorn"
    vendorSynonymDict['Mexican'] = "taqueria-la-ventana"
    if v in vendorSynonymDict:
        return vendorSynonymDict[v]
    else:
        return v

def getHours(v):
    url = 'https://dallasfarmersmarket.org/directory/{}'.format(v).replace(" ", "-")
 #   headers = {}
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = requests.post(url, headers=headers)
    r = requests.get(req)
    soup = BeautifulSoup(req, "lxml")

    url_hours = soup.find("div", {"class":"w2dc-field-output-block-9"}).get_text().replace("\n", " ").replace("\t", " ").replace("\r", " ").replace("\s+", " ").encode('ascii', 'ignore').decode('ascii')
    url_vendor = soup.find("h2", {"itemprop":"name"}).get_text().encode('ascii', 'ignore').decode('ascii')
    hours.append(url_hours)
    vendor.append(url_vendor)
    for m, n in list(zip(hours,vendor)):
        list1 = (n,m)
    return list1




def stateHours(v):
    if (v is None):
 #       reprompt_show = render_template("reprompt_vendor")
#        return question(reprompt_vendor)
        print("None")
    else:
        filVendor = processVendorName(v)
        hours = getHours(filVendor)
        v_name = hours[0]
        v_hours = hours[1]
        if ("Hours:" in v_hours):
            v_hours = v_hours.replace("Hours:", "")
#        vendorHours_msg = render_template('vendor_hours', v=v, list1=list1)
#        return statement(vendorHours_msg)
        print("The hours for " + v_name + " are " + v_hours + ".")

stateHours(v)
