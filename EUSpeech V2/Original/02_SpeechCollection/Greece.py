# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 09:53:12 2019

@title:  Link collection Greece

@author: samunico
"""

#%% setup
# from lxml import html
# from urllib import request
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import datetime
import csv
completelinks = []
date = []
speaker = []
country = []
language = []
title = []
deadlinks = []
now=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
linkpath =  "C:/Users/samunico/OneDrive/Dokumente/Studium/"+\
            "Amsterdam/Gijs/Speeches/Scraping/I - Linkscraping/"+\
            "CompleteLinks/Greece_"+now+".csv"
headers = {'User-Agent': 'Chrome/41.0.2228.0'}



#%% link collection
author1="A. Tsipras"
author2="K. Mitsotakis" 
dateswitch = time.strptime("08/07/2019","%d/%m/%Y")
startdate = time.strptime("26/01/2015","%d/%m/%Y")
location="Greece"
lang="GR"
xpathlink='//*[@id="td-outer-wrap"]//div[2]/h3/a'
xpathdate='//*[@id="td-outer-wrap"]//div[2]/div[1]/span/time'
strtodate="%Y-%m-%d"
linktodate=".*/([0-9]+/[0-9]+/[0-9]+)/.*"
linkbase = 'https://primeminister.gr/'
fetchurl = 'https://primeminister.gr/category/activity/speeches'

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")

# xpaths for Selenium
xpathbtn = '//*[@id="td-outer-wrap"]/div[3]/div/div/div[1]/div/div[{}]/a'

# open browser
driver = webdriver.Chrome(options=opts)
driver.get(fetchurl)

# scroll down page
for i in range(0,5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
for no in range(0, 30):
    button = driver.find_element_by_xpath(xpathbtn.format(32+no*10))
    try:
        button.click()
        time.sleep(5)
    except NoSuchElementException:
        time.sleep(10)
        button.click()
        time.sleep(5)
        
        
templinks = driver.find_elements_by_xpath(xpathlink)
tempdates = driver.find_elements_by_xpath(xpathdate)


# identify and collect links, write into csv
c = 0
t = 0
m = 0
with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    for lk, dt in zip(templinks, tempdates):
        row = []
        tmpdt=time.strptime(dt.get_attribute('datetime')[:10], strtodate)
        row.append(time.strftime("%d-%m-%Y",tmpdt))
        row.append(location)
        if tmpdt < dateswitch and tmpdt > startdate:                  
            row.append(author1)
            t += 1
        elif tmpdt > dateswitch:
            row.append(author2)
            m += 1
        else:
            print('Stopping collection at {}'.format(time.strftime("%d-%m-%Y",tmpdt)))
            break
        row.append(lang)
        row.append(lk.get_attribute('text'))
        row.append(lk.get_attribute('href'))
        writer.writerow(row)
        c += 1
print("Finished collecting {} links; {} for Tsipras; {} for Mitsotakis".format(c,t,m))
driver.quit()

#%% speechscraper
# import and vars
import csv
from urllib import request
from lxml import html
import time
import datetime

speechdir = 'C:/Users/samunico/OneDrive/Dokumente/Studium/Amsterdam/Gijs/Speeches/Scraping/II - Speechscraping/Speeches'
xpath = '//*[@class="td-post-content"]//text()'
deadlinks = []
i = 0
mis = 0
unw = 0

headers = {'User-Agent': 'Chrome/41.0.2228.0'}


#%% speech collection

print('Start fetching speeches...\n')

dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

with open(linkpath, mode="r",encoding="utf-8") as fi: # Change to correct directory before importing
    with open(speechdir+"/speeches_final.csv", mode="a", encoding="utf-8") as fo: # Change to correct directory before importing
        reader = csv.reader(fi,delimiter=",")
        writer = csv.writer(fo, lineterminator = '\n')
        for row in reader:
            print("\tFetching speech #", str(i+1), '...' , end = "\r")
            for attempt in range(3):
                try:
                    fetchlink = row[5]
                    req = request.Request(url = str(fetchlink), headers = headers)
                    tree = html.fromstring(request.urlopen(req).read().decode(encoding="utf-8"))
                except request.HTTPError:
                    print("Whoops, that went wrong, retrying page "+ fetchlink +" for "+ row[2] + " "+ row[3])
                    if attempt == 2:
                        print("Fetching page " + fetchlink +" for "+ row[2] + " "+ row[3] + " failed due to HTTPError")
                        deadlinks.append(fetchlink)
                        mis += 1
                        continue
                    time.sleep(10)
                except request.URLError:
                    print("Whoops, that went wrong, retrying page "+ fetchlink +" for "+ row[2] + " "+ row[3])
                    if attempt == 2:
                        print("Fetching page " + fetchlink +" for "+ row[2] + " "+ row[3] + " failed due to URLError")
                        deadlinks.append(fetchlink)
                        mis += 1
                        continue
                    time.sleep(10)
                except:
                    print("Whoops, that went wrong, retrying page "+ fetchlink +" for "+ row[2] + " "+ row[3])
                    if attempt == 2:
                        print("Fetching page " + fetchlink +" for "+ row[2] + " "+ row[3] + " failed due to Unknown Error")
                        deadlinks.append(fetchlink)
                        mis += 1
                        continue
                    time.sleep(10)
                                                            
            txt = tree.xpath(xpath)
            if txt == []:
                print('No speech found for\n\t', fetchlink, '\n\t using xpath: ', xpath)
                deadlinks.append(fetchlink)
                mis += 1
                continue
                
            txtstr = ''
            
            for t in txt:
                txtstr += t + ' '
            cleantxt = re.sub("\r|\n|\t|\\xa0|\* \* \*"," ",txtstr.lstrip())
            
            regex = ".*}(.*)"
            try:
                cleantxt = re.match(regex, cleantxt).group(1)
            except AttributeError:
                pass
            
            cleantxt = re.sub(' +', ' ', cleantxt)
            
            if len(cleantxt)<200:
                print(cleantxt)
                print('\tVery short speech: ', str(row), '\n\tSKIPPING SPEECH')
                deadlinks.append(fetchlink)
                mis += 1
                continue
            
            row.append(cleantxt)
            writer.writerow(row)
            i += 1
            # time.sleep(randint(1,3))


#%% write into existing datafile

with open(speechdir+"/deadlinks_"+dt+".csv", mode="w",encoding="utf-8") as fo: # Change to correct directory before importing
    writer = csv.writer(fo, lineterminator = '\n')
    for dl in deadlinks:
        writer.writerow(dl)  
 

print('Finished fetching {} greek speeches'.format(str(i)))
print('Collection of {} links failed'.format(str(mis)))



