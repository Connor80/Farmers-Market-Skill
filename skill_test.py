from bs4 import BeautifulSoup
import urllib.request
import csv
import itertools

v = "Cane Rosso"
hours = []
vendor = []

def processVendorName(v):
    vendorSynonymDict = {}
    vendorSynonymDict['pop'] = "Doc Popcorn"
    vendorSynonymDict['Mexican'] = "taqueria la ventana"
    vendorSynonymDict['ice cream'] = "coolhaus"
    vendorSynonymDict['pizza'] = "Cane Rosso"
    if v in vendorSynonymDict:
        return vendorSynonymDict[v]
    else:
        return v

def getHours(v):
    if (v == "Cane Rosso"):
        url = 'http://www.canerosso.com/deep-ellum'
        req = urllib.request.Request(url)
        r = urllib.request.urlopen(req)
        soup = BeautifulSoup(r, "lxml")

        url = 'http://www.canerosso.com/deep-ellum'
        req = urllib.request.Request(url)
        r = urllib.request.urlopen(req)
        soup = BeautifulSoup(r, "lxml")
        rosso_hours = soup.find("div", {"class":"html-block"}).get_text().replace(";", " and").replace("Mon", "Monday").replace("Thurs", "Thursday").replace(":", " ").replace("Fri", "Friday").replace("Sat", "Saturday").replace("Sun", "Sunday").replace("HOURS", "")

        return rosso_hours
    else:
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

def stateHours(v):
    if v is None:
        print("None")
    elif v == "Cane Rosso":
        filVendor = processVendorName(v)
        hours = getHours(filVendor)
        cane_name = "Cane Rosso"
        cane_hours = hours
        print("The hours for " + str(cane_name) + " are " + str(cane_hours) + ".")
    else:
        filVendor = processVendorName(v)
        hours = getHours(filVendor)
        v_name = hours[0]
        v_hours = hours[1]
        if ("Hours:" in v_hours):
            v_hours = v_hours.replace("Hours:", "")
        print("The hours for " + v_name + " are " + v_hours + ".")

stateHours(v)
