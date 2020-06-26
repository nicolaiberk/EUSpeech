#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 09:14:15 2020

LInk COllection Covid: Tricky Cases

@author: Nicolai Berk
"""

from urllib import request
from random import randint
import time
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import csv
import os

#%% Sweden
# selenium

linkpath = 'ADD/PATH/HERE'

fetchlink = 'https://www.government.se/speeches/'
author="S.Loefven"
location="Sweden"
lang="EN"
xpathmp='//*[@id="tabs--primo--alpha-fragment-1-result"]/div[2]/div/h2/span[2]/strong[1]'
regexmp="[0-9]+"
strtodate="%d %B %Y"
num = 0
i = 0
mindate = "12 June 2019"
deadlinks = []

#xpaths for selenium
xpcookie = '/html/body/div[1]/div/div/div[2]/button'
xpspeaker1 = '//*[@id="tabs--primo--alpha-fragment-1"]/div/div[3]/button'
xpspeaker2 = '//*[@id="tab1-2144"]'
xpnext = "//a[contains(text(),'Next')]"
xpobj = '//*[@id="tabs--primo--alpha-fragment-1-result"]/div[2]/div/div[2]/ul/li[{}]/div/a'
xptime = '//*[@id="tabs--primo--alpha-fragment-1-result"]/div[2]/div/div[2]/ul/li[{}]/div/div/p/time' 

# setup page according to requirements using selenium
driver = webdriver.Chrome()
driver.get(fetchlink)
time.sleep(randint(1,2))

btcookie = driver.find_element_by_xpath(xpcookie)
btcookie.click()
time.sleep(randint(1,2))

btspeaker1 = driver.find_element_by_xpath(xpspeaker1)
btspeaker1.click()
btspeaker2 = driver.find_element_by_xpath(xpspeaker2)
btspeaker2.click()
time.sleep(randint(1,2))

maxpages = driver.find_element_by_xpath(xpathmp)
maxno = int(int(maxpages.text)/10)+1


with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    for attempt in range(3):
        try:
            while num < maxno:
                for n in range(10):
                    obj = driver.find_element_by_xpath(xpobj.format(n+1))
                    row = []
                    timeobj =  driver.find_element_by_xpath(xptime.format(n+1))
                    tmpdt = time.strptime(timeobj.text, strtodate)
                    
                    if tmpdt <= time.strptime(mindate, strtodate):
                        num = maxno+1
                        break
                    
                    row.append(time.strftime("%d-%m-%Y", tmpdt))
                    row.append(author)
                    ttf = re.sub("\r|\n|\t","",obj.text.lstrip())
                    row.append(ttf)
                    row.append(obj.get_attribute('href'))
                    writer.writerow(row)
                    i += 1                
                btnext = driver.find_element_by_xpath(xpnext)
                btnext.click()
                num += 1            
                time.sleep(randint(1,3))
        except request.HTTPError:
            print("Whoops, that went wrong, retrying page "+str(num+1)+" for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(num+1) + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink.format(num+1))
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page "+str(num+1)+" for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(num+1) + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink.format(num+1))
            time.sleep(10)
        except NoSuchElementException:
            break

driver.close()
    
print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")

#%% Sweden (SV)

fetchlink = 'https://www.regeringen.se/tal/'
author="S.Loefven"
location="Sweden"
lang="SV"
xpathmp='//*[@id="tabs--primo--alpha-fragment-1-result"]/div[2]/div/h2/span[2]/strong[1]'
regexmp="[0-9]+"
strtodate="%d %m %Y"
mindate = "12 06 2019"
num = 0
speechlinks = []
i = 0

#xpaths for selenium
xpcookie = '/html/body/div[1]/div/div/div[2]/button'
xpspeaker1 = '//*[@id="tabs--primo--alpha-fragment-1"]/div/div[3]/button'
xpspeaker2 = '//*[@id="tab1-2119"]'
xpnext = '//*[@id="tabs--primo--alpha-fragment-1-result"]/div[2]/div/div[2]/ol/li[*]/a'
xpobj = '//*[@id="tabs--primo--alpha-fragment-1-result"]/div[2]/div/div[2]/ul/li[{}]/div/a'
xptime = '//*[@id="tabs--primo--alpha-fragment-1-result"]/div[2]/div/div[2]/ul/li[{}]/div/div/p/time' 

# setup page according to requirements using selenium
driver = webdriver.Chrome()
driver.get(fetchlink)
time.sleep(randint(1,2))

btcookie = driver.find_element_by_xpath(xpcookie)
btcookie.click()
time.sleep(randint(1,2))

btspeaker1 = driver.find_element_by_xpath(xpspeaker1)
btspeaker1.click()
btspeaker2 = driver.find_element_by_xpath(xpspeaker2)
btspeaker2.click()
time.sleep(randint(1,2))

maxpages = driver.find_element_by_xpath(xpathmp)
maxno = int(int(maxpages.text)/10)+1

with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    for attempt in range(3):
        try:
            while num < maxno:
                for n in range(10):
                    obj = driver.find_element_by_xpath(xpobj.format(n+1))
                    timeobj =  driver.find_element_by_xpath(xptime.format(n+1))
                    tmpdt_d = re.match('([0-9]+) (.*) ([0-9]+)', timeobj.text).group(1)
                    mstr = re.match('([0-9]+) (.*) ([0-9]+)', timeobj.text).group(2)
                    tmpdt_y = re.match('([0-9]+) (.*) ([0-9]+)', timeobj.text).group(3)
                    if (mstr == 'januari'):
                        tmpdt_m = '01'
                    elif (mstr == 'februari'):
                        tmpdt_m = '02'
                    elif (mstr == 'mars'):
                        tmpdt_m = '03'
                    elif (mstr == 'april'):
                        tmpdt_m = '04'
                    elif (mstr == 'maj'):
                        tmpdt_m = '05'
                    elif (mstr == 'juni'):
                        tmpdt_m = '06'
                    elif (mstr == 'juli'):
                        tmpdt_m = '07'
                    elif (mstr == 'augusti'):
                        tmpdt_m = '08'
                    elif (mstr == 'september'):
                        tmpdt_m = '09'
                    elif (mstr == 'oktober'):
                        tmpdt_m = '10'
                    elif (mstr == 'november'):
                        tmpdt_m = '11'
                    elif (mstr == 'december'):
                        tmpdt_m = '12'
                    else:
                        tmpdt_m = 'err'
                    tmpdt=time.strptime((tmpdt_d+' '+tmpdt_m+' '+tmpdt_y), strtodate)
                    
                    if tmpdt <= time.strptime(mindate, strtodate):
                        num = maxno+1
                        break
                    
                    row = []
                    row.append(time.strftime("%d-%m-%Y", tmpdt))
                    row.append(author)
                    ttf = re.sub("\r|\n|\t","",obj.text.lstrip())
                    row.append(ttf)
                    row.append(obj.get_attribute('href'))
                    writer.writerow(row)
                    i += 1
                btnext = driver.find_elements_by_xpath(xpnext)
                btnext[-1].click()
                num += 1            
                time.sleep(randint(1,3))
        except request.HTTPError:
            print("Whoops, that went wrong, retrying page "+str(num+1)+" for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(num+1) + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink.format(num+1))
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page "+str(num+1)+" for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(num+1) + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink.format(num+1))
            time.sleep(10)
        except NoSuchElementException:
            break

driver.close()

print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")

with open(linkpath+"deadlinks", mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    for link in deadlinks:
        writer.writerow(link)


