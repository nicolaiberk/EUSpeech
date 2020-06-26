# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 10:21:25 2019

Final Linkscraper

@author: NB
"""
# could add script for metafile describing number of links fetched and
# period fetched from for each speaker (similar to existing file),
# plus relevant comments

#%% setup
from lxml import html
from urllib import request
from random import randint
import time
import re
import math
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import WebDriverException
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.chrome.options import Options
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
            "CompleteLinks/linkset_"+now+".csv"
headers = {'User-Agent': 'Chrome/41.0.2228.0'}

# generate csv and print header
with open(linkpath, mode="w", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    # write header:
    firstrow = ['Date', 'Country', 'Speaker', 'Language', 'Title', 'URL']
    writer.writerow(firstrow)
    


#%% # fetch page for EN speeches by Babis (CZ)  - unclear wether this should be kept due to duplicates
fetchlink="https://www.vlada.cz/scripts/detail.php?pgid=1016&conn=10175&pg="
author="A. Babiš"
location="Czech Republic"
lang="EN"
xpathmp='//*[@id="content"]/div[1]/div[1]/ul/p/text()'
regexmp=".*xa0([0-9]+).*"
xpathlink='//*[@class="record"]/h2/a/@href'
xpathdate='//*[@class="info"]/text()'
strtodate="%d. %m. %Y"
xpathtitle='//*[@class="record"]/h2/a/text()'
linkbase="http://www.vlada.cz"

for attempt in range(5):
    try:
        req=request.Request(url = fetchlink, headers = headers)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        maxpage = (int(re.match('.*from (\d*) total', str(tree.xpath(xpathmp))).group(1))//10)+1
    except request.HTTPError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except request.URLError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except ConnectionResetError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)    
    else:
        break

i = 0

with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    for n in range(maxpage):
        req=request.Request(url = fetchlink+str(n+1), headers = headers)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        tempdate=(tree.xpath(xpathdate))
        temptitle=(tree.xpath(xpathtitle))    
        templinks=tree.xpath(xpathlink)
        
        for dt,tt,lk in zip(tempdate,temptitle,templinks):
            row = []
            tmpdt=time.strptime(dt, strtodate)
            row.append(time.strftime("%d-%m-%Y",tmpdt))
            row.append(location)
            row.append(author)
            row.append(lang)
            row.append(tt)
            row.append(linkbase+lk)
            writer.writerow(row)
            i += 1
        
print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")



#%% fetch page for CZ speeches by Babis
fetchlink="https://www.vlada.cz/scripts/detail.php?pgid=1013&conn=10155&pg="
author="A. Babiš"
location="Czech Republic"
lang="CZ"
xpathmp='//*[@class="pager offset-before-double"]/p/text()'
regexmp=".*xa0([0-9]+).*"
xpathlink='//*[@class="record"]/h2/a/@href'
xpathdate='//*[@class="info"]/text()'
strtodate="%d. %m. %Y"
xpathtitle='//*[@class="record"]/h2/a/text()'
linkbase="http://www.vlada.cz"
i = 0
speechlinks=[]

for attempt in range(5):
    try:
        req=request.Request(url = fetchlink, headers = headers)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        maxpage=str(tree.xpath(xpathmp))
    except request.HTTPError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except request.URLError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except ConnectionResetError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)    
    else:
        break

try:
    maxno=math.ceil(int(re.match(regexmp,maxpage).group(1))/10)
except AttributeError:
    maxno=1
    print("Only 1 result page found/Error occured ("+ author + lang +")")
numbers=list(range(0,int(maxno)))

with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')

    for number in numbers:
        for attempt in range(5):
            try:
                req=request.Request(fetchlink + str(number+1))
                tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
                templinks = tree.xpath(xpathlink)
                tempdate=(tree.xpath(xpathdate))
                temptitle=(tree.xpath(xpathtitle))    
                for dt,tt,lk in zip(tempdate,temptitle, templinks):    
                    tmpdt=time.strptime(dt, strtodate)
                    row = []
                    row.append(time.strftime("%d-%m-%Y",tmpdt))
                    row.append(location)
                    row.append(author)
                    row.append(lang)
                    row.append(tt)
                    row.append(linkbase+lk)
                    writer.writerow(row)
                    i += 1
                time.sleep(randint(1,5))
            except request.HTTPError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 4:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink + str(number+1))
                time.sleep(10)
            except request.URLError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 4:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink + str(number+1))
                time.sleep(10)
            except ConnectionResetError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 4:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink + str(number+1))
                time.sleep(10)
            else:
                break


print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")

#%% Sobotka [EN]
fetchlink="https://web.archive.org/web/20160601140828/http://www.vlada.cz/scripts/detail.php?pgid=1016"
author="B. Sobotka"
location="Czech Republic"
lang="EN"
xpathmp='//*[@class="counter"]/text()'
regexmp=".*from ([0-9]+) total.*"
xpathlink='//*[@class="record"]/h2/a/@href'
xpathdate='//*[@class="info"]/text()'
strtodate="%d. %m. %Y"
xpathtitle='//*[@class="record"]/h2/a/text()'
linkbase="http://www.vlada.cz"
i = 0

with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    try:
        req=request.Request(url = fetchlink, headers = headers)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        templinks = tree.xpath(xpathlink)
        tempdate=(tree.xpath(xpathdate))
        temptitle=(tree.xpath(xpathtitle))    
        for dt,tt,lk in zip(tempdate,temptitle,templinks):    
            tmpdt=time.strptime(dt, strtodate)
            row = []
            row.append(time.strftime("%d-%m-%Y",tmpdt))
            row.append(location)
            row.append(author)
            row.append(lang)
            row.append(tt)
            row.append(linkbase+lk)
            writer.writerow(row)
            i += 1
    except request.HTTPError:
        print("Whoops, that went wrong, retrying page "+fetchlink+" for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching result page " + fetchlink + ' ' + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
        time.sleep(10)
    except request.URLError:
        print("Whoops, that went wrong, retrying page "+fetchlink+" for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching result page " + fetchlink + ' ' + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
        time.sleep(10)
    except ConnectionResetError:
        print("Whoops, that went wrong, retrying page "+fetchlink+" for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching result page " + fetchlink + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)

print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")

#%% Sobotka [CZ]

fetchlinks = []
fetchlinks.append('https://web.archive.org/web/20170406131048/https://www.vlada.cz/scripts/detail.php?pgid=1013') # 16.03.-05.04.2017
fetchlinks.append('https://web.archive.org/web/20170205082751/https://www.vlada.cz/scripts/detail.php?pgid=1013') # 11.01.-02.02.2017
fetchlinks.append('https://web.archive.org/web/20160704134626/http://www.vlada.cz/scripts/detail.php?pgid=1013')  # 15.06.-01.07.2016
fetchlinks.append('https://web.archive.org/web/20160505160348/http://www.vlada.cz/scripts/detail.php?pgid=1013')  # 06.04.-04.05.2016
fetchlinks.append('https://web.archive.org/web/20160403085232/http://www.vlada.cz/scripts/detail.php?pgid=1013')  # 17.03.-01.04.2016
fetchlinks.append('https://web.archive.org/web/20151216184727/http://www.vlada.cz/scripts/detail.php?pgid=1013')  # 26.11.-16.12.2015

author="B. Sobotka"
location="Czech Republic"
lang="CZ"
xpathmp='//*[@class="counter"]/text()'
regexmp=".*from ([0-9]+) total.*"
xpathlink='//*[@class="record"]/h2/a/@href'
xpathdate='//*[@class="info"]/text()'
strtodate="%d. %m. %Y"
xpathtitle='//*[@class="record"]/h2/a/text()'
linkbase="http://www.vlada.cz"
i = 0

for fetchlink in fetchlinks:
    for attempt in range(5):
        try:
            req=request.Request(url = fetchlink, headers = headers)
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            maxpage=str(tree.xpath(xpathmp))
        except request.HTTPError:
            print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
            if attempt == 4:
                print("Fetching first page " + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink)
        except request.URLError:
            print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
            if attempt == 4:
                print("Fetching first page " + author + lang + " failed due to URLError")
                deadlinks.append(fetchlink)
        except ConnectionResetError:
            print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
            if attempt == 4:
                print("Fetching first page " + author + lang + " failed due to ConnectionError")
                deadlinks.append(fetchlink)    
            else:
               break

with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    
    for fetchlink in fetchlinks:
        for attempt in range(5):
            try:
                req=request.Request(url = fetchlink, headers = headers)
                tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
                tempdate=(tree.xpath(xpathdate))
                temptitle=(tree.xpath(xpathtitle))    
                templinks = tree.xpath(xpathlink)
                for dt,tt,lk in zip(tempdate,temptitle,templinks):    
                    tmpdt=time.strptime(dt, strtodate)
                    row = []
                    row.append(time.strftime("%d-%m-%Y",tmpdt))
                    row.append(location)
                    row.append(author)
                    row.append(lang)
                    row.append(tt)
                    row.append(linkbase+lk)
                    writer.writerow(row)
                    i += 1
                time.sleep(randint(1,5))
            except request.HTTPError:
                print("Whoops, that went wrong, retrying page "+fetchlink+" for "+author+ " "+ lang)
                if attempt == 4:
                    print("Fetching result page " + fetchlink + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink)
                time.sleep(10)
            except request.URLError:
                print("Whoops, that went wrong, retrying page "+fetchlink+" for "+author+ " "+ lang)
                if attempt == 4:
                    print("Fetching result page " + fetchlink + author + lang + " failed due to URLError")
                    deadlinks.append(fetchlink)
                time.sleep(10)
            except ConnectionResetError:
                print("Whoops, that went wrong, retrying page "+fetchlink+" for "+author+ " "+ lang)
                if attempt == 4:
                    print("Fetching result page " + fetchlink + author + lang + " failed due to ConnectionError")
                    deadlinks.append(fetchlink)
                time.sleep(10)
            else:
                break

print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")

#%% Newest speeches Macron [FR]
fetchlink = 'https://www.elysee.fr/toutes-les-actualites'
xpbutton = '//*[@id="main"]/section[2]/p/button'
xpathdate = '//*[@id="main"]/article/section[{}]/div/div/p'
xpathtitle = '//*[@id="main"]/article/section[{}]/div/div/a/span[1]'
xpathlink = '//*[@id="main"]/article/section[{}]/div/div/a'
xpcookie = '//*[@id="tarteaucitronPersonalize"]'
author = "E. Macron"
location = "France"
lang = "FR"
stoptime = time.strptime('29-01-2019', '%d-%m-%Y')
i = 0

# setup page according to requirements using selenium
driver = webdriver.Chrome()
driver.get(fetchlink)
time.sleep(randint(1,2))

btcookie = driver.find_element_by_xpath(xpcookie)
btcookie.click()
time.sleep(randint(1,2))


with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
 
    cor = 0
    x = True
    while x == True:
        try:
            tt = driver.find_element_by_xpath(xpathtitle.format((i+1))).text
            dt = driver.find_element_by_xpath(xpathdate.format((i+1)))
            lk = driver.find_element_by_xpath(xpathlink.format((i+1))).get_attribute('href')
        except NoSuchElementException:
            i+=1
            cor += 1
            if i > 1000: # sometimes loop continues without clicking, this 'resets to last position'
                i = i-cor
                btnext = driver.find_element_by_xpath(xpbutton)
                btnext.click()
            continue
        
        day = dt.text.split(' ')[0]
        mstr = dt.text.split(' ')[1].lower()
        if (mstr == 'janvier'):
            month = '01'
        elif (mstr == 'février'):
            month = '02'
        elif (mstr == 'mars'):
            month = '03'
        elif (mstr == 'avril'):
            month = '04'
        elif (mstr == 'mai'):
            month = '05'
        elif (mstr == 'juin'):
            month = '06'
        elif (mstr == 'juillet'):
            month = '07'
        else: 
            print('Unknown date format: ', mstr) # only fetching january to july
        year = dt.text.split(' ')[2]
        tmpdt = time.strptime((day+'-'+month+'-'+year), '%d-%m-%Y')
        if tmpdt > stoptime:
            row = []
            row.append((day+'-'+month+'-'+year))
            row.append(location)
            row.append(author)
            row.append(lang)
            row.append(tt)
            row.append(lk)
            writer.writerow(row)
            i += 1
        else:
            driver.close()
            x = False
            break
        if i > 20 and (i-9) % 20 == 0:
            btnext = driver.find_element_by_xpath(xpbutton)
            btnext.click()
            time.sleep(randint(1,2))

print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")

#%% Fetching remaining links of Macron [FR]
fetchlink="https://www.vie-publique.fr/rechercher/recherche.php?query=&date=&dateDebut=2017/05/17&dateFin=&b=0&skin=cdp&replies=312&filter=&typeloi=&auteur=f/vp_auteurphysique/macron%20emmanuel&filtreAuteurLibre=&typeDoc=f/vp_type_discours/declaration&source=f/vp_type_emetteur/president%20de%20la%20republique&sort=&q="
author="E. Macron"
location="France"
lang="FR"
xpathlink='//*[@id="subcontent"]/ul/li[*]//@href'
xpathdate='//*[@id="subcontent"]/ul/li[*]/p[2]/text()'
strtodate="%d/%m/%Y"
xpathtitle='//*[@id="subcontent"]/ul/li[*]/p/a/text()'
xpathmp='//*[@id="subcontent"]/h2/text()'
i = 0

with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    for attempt in range(3):
        try:
            req=request.Request(url = fetchlink, headers = headers)
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            templinks = tree.xpath(xpathlink)
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt,lk in zip(tempdate,temptitle,templinks):    
                tmpdt=time.strptime(dt, strtodate)
                row = []
                row.append(time.strftime("%d-%m-%Y",tmpdt))
                row.append(location)
                row.append(author)
                row.append(lang)
                ttf = re.match('\d* - (.*)', re.sub("\r|\n|\t","",tt.lstrip())).group(1)
                row.append(ttf)
                row.append(re.match(' *(.*)', lk).group(1))
                writer.writerow(row)
                i += 1
        except request.HTTPError:
            print("Whoops, that went wrong, retrying page for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink)
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink)
            time.sleep(10)
        else:
            break

print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")

#%% Hollande [FR], (from same website)
fetchlink="https://www.vie-publique.fr/rechercher/recherche.php?query=&dateDebut=2015/10/01&dateFin=2017/05/16&replies=569&filter=&date=&auteur=f/vp_auteurphysique/hollande%20francois&filtreAuteurLibre=&skin=cdp&typeDoc=&source=f/vp_type_emetteur/president%20de%20la%20republique&q="
author="F. Hollande"
location="France"
lang="FR"
i = 0

with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    for attempt in range(3):
        try:
            req=request.Request(url = fetchlink, headers = headers)
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            templinks = tree.xpath(xpathlink)
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt,lk in zip(tempdate,temptitle,templinks):    
                tmpdt=time.strptime(dt, strtodate)
                row = []
                row.append(time.strftime("%d-%m-%Y",tmpdt))
                row.append(location)
                row.append(author)
                row.append(lang)
                ttf = re.match('\d* - (.*)', re.sub("\r|\n|\t","",tt.lstrip())).group(1)
                row.append(ttf)
                row.append(re.match(' *(.*)', lk).group(1))
                writer.writerow(row)
                i += 1
        except request.HTTPError:
            print("Whoops, that went wrong, retrying page for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink)
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink)
            time.sleep(10)
        else:
            break

print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")

#%% German speeches Merkel (DE)
fetchlink="https://www.bundeskanzlerin.de/bkin-de/aktuelles/70298!search?formState=eNptjzFTwzAMhf8K9-YMiUlS8FYoe4Gx18E4SshdagdbAXq9_HdkSGBhepLufU_SBY1hejKuowh9wSZXtyoVbfAnaDcNQwb2P9U8Z2iNJf611tAH3O23zyORfcUxWwMOKKq63FQ50qjMbxatFy0XVThK6Gi63hnuvUvBwX_IgqLKENkEhr4uKjH5to3E601vE4Xz2gzeftOP_w23p5eed71kOUvQUOmmMVCMD-_k-F7-7_wfFn1aCfpMzDiYMzU7sVw1FK2AdgpBqL3pJEup-QteuGUC&page="
author="A. Merkel"
location="Germany"
lang="DE"
xpathmp='//*[@id="main"]/div/div/div[3]/div/ul/li[5]/a/@title'
regexmp=".*'Seite ([0-9]+)'.*"
xpathlink='//*[@id="searchResult"]/div/ol/li/h3/a/@href'
strtodate="%Y-%m-%d"
xpathdate='//*[@id="searchResult"]/div/ol/li/p'
xpathtitle='//*[@id="searchResult"]/div/ol/li/h3/a/text()'
linkbase="http://www.bundeskanzlerin.de/"
i = 0

for attempt in range(3):
    try:
        req=request.Request(url = fetchlink, headers = headers)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        maxpage=str(tree.xpath(xpathmp))
    except request.HTTPError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 2:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except request.URLError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 2:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    else:
        break

try:
    maxno=re.match(regexmp,maxpage).group(1)
except AttributeError:
    maxno=1
    print("Only 1 result page found/Error occured ("+ author + lang +")")
numbers=list(range(0,int(maxno)))


with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    for number in numbers:
        for attempt in range(3):
            try:
                req=request.Request(fetchlink + str(number+1))
                tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
                templinks=tree.xpath(xpathlink)
                tempdate=tree.xpath(xpathdate)
                temptitle=(tree.xpath(xpathtitle))    
                for lk,dt,tt in zip(templinks,tempdate,temptitle):
                    if (dt == '\n'):
                        pass
                    else:
                        day = dt.text.split(',')[1].split('\n')[0].split(' ')[1][0:2]
                        mstr = dt.text.split(',')[1].split('\n')[0].split(' ')[2]
                        if (mstr == 'Januar'):
                            month = '01'
                        elif (mstr == 'Februar'):
                            month = '02'
                        elif (mstr == 'März'):
                            month = '03'
                        elif (mstr == 'April'):
                            month = '04'
                        elif (mstr == 'Mai'):
                            month = '05'
                        elif (mstr == 'Juni'):
                            month = '06'
                        elif (mstr == 'Juli'):
                            month = '07'
                        elif (mstr == 'August'):
                            month = '08'
                        elif (mstr == 'September'):
                            month = '09'
                        elif (mstr == 'Oktober'):
                            month = '10'
                        elif (mstr == 'November'):
                            month = '11'
                        elif (mstr == 'Dezember'):
                            month = '12'
                        else:
                            month = 'err'
                        year = dt.text.split(',')[1].split('\n')[0].split(' ')[3]
                        tmpdt=time.strptime((year+'-'+month+'-'+day), strtodate)
                        if (tmpdt < time.strptime('2015-11-01', strtodate)):
                            pass
                        else:
                            row = []
                            row.append(time.strftime("%d-%m-%Y",tmpdt))
                            row.append(location)
                            row.append(author)
                            row.append(lang)
                            ttf = re.sub("\r|\n|\t","",tt.lstrip())
                            row.append(ttf)
                            row.append(linkbase+lk)
                            writer.writerow(row)
                            i += 1
                time.sleep(randint(1,3))
            except request.HTTPError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 2:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink + str(number+1))
                time.sleep(10)
            except request.URLError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 2:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink + str(number+1))
                time.sleep(10)
            else:
                break

print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")


#%% German speeches (EN)
fetchlink = 'https://www.bundeskanzlerin.de/bkin-en/news/864130!search?formState=eNptkMsOgjAQRX_FzJoFKCBh52vvY2lc1DIgCbTYDiox_LtTkRgTd6eTe-5M-oRMEO6FKtBC-oQkDoNZ4ig3uoZUtVXlAemB-t6DXEikn-zxTVEI3gDxCMkHYp-B5-E8msJpmM1CJy63i0ODKC9w4upGFKUSVGrl6o2-85rI98CSMASpzxGd5xZpvOvaounGR6Xl2939Gy7qc0nrkpuUREhh6k5qDFq7uaGiFX9Cob-a1W4h4MM5TSU6zNYcmWRoJYuyNYatrSi4K-hfKRhmAA&limit=50'
author="A. Merkel"
location="Germany"
lang="EN"
xpathlink='//*[@id="searchResult"]/div/ol/li/h3/a/@href'
strtodate="%Y-%b-%d"
xpathdate='//*[@id="searchResult"]/div/ol/li/p'
xpathtitle='//*[@id="searchResult"]/div/ol/li/h3/a/text()'
linkbase="http://www.bundeskanzlerin.de"
i = 0


with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    for attempt in range(3):
        try:
            req=request.Request(url = fetchlink, headers = headers)
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            templinks=tree.xpath(xpathlink)
            tempdate=tree.xpath(xpathdate)
            temptitle=(tree.xpath(xpathtitle))    
            for lk, dt,tt in zip(templinks, tempdate,temptitle):
                if (dt == '\n'):
                    pass
                else:
                    day = dt.text.split(',')[0].split('\n')[1].split(' ')[1]
                    month = dt.text.split(',')[0].split('\n')[1].split(' ')[0]
                    year = dt.text.split(',')[1].split('\n')[0].split(' ')[1]
                    tmpdt=time.strptime((year+'-'+month+'-'+day), strtodate)
                    if (tmpdt < time.strptime('2015-May-01', strtodate)):
                        pass
                    else:
                        row = []
                        row.append(time.strftime("%d-%m-%Y",tmpdt))
                        row.append(location)
                        row.append(author)
                        row.append(lang)
                        ttf = re.sub("\r|\n|\t","",tt.lstrip())
                        row.append(ttf)
                        row.append(linkbase+lk)
                        writer.writerow(row)
                        i += 1
            time.sleep(randint(1,3))
        except request.HTTPError:
            print("Whoops, that went wrong, retrying page " + " for " + author + " "+ lang)
            if attempt == 2:
                print("Fetching result page " + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink)
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page " + " for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink)
            time.sleep(10)
        else:
            break
        
        

print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")


#%% Rutte (EN)
# unclear if EN or NL
fetchlink="https://www.government.nl/documents?keyword=rutte&period-from=01-11-2015&issue=All+topics&element=Ministry+of+General+Affairs&type=Speech&page="
author="M. Rutte"
location="Netherlands"
lang="EN"
xpathmp='//*[@id="content"]/div[1]/h2/span/text()'
regexmp=".*'([0-9]+)'.*"
xpathlink='//*[@class="common results"]/a/@href'
xpathdate='//*[@class="meta"]/text()'
strtodate="\n              Speech | %d-%m-%Y"
xpathtitle='//*[@class="publication"]/h3/text()'
linkbase="https://www.government.nl"
i = 0

for attempt in range(3):
    try:
        req=request.Request(url = fetchlink, headers = headers)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        maxpage=str(tree.xpath(xpathmp))
    except request.HTTPError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 2:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except request.URLError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 2:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    else:
        break

try:
    maxno=math.ceil(int(re.match(regexmp,maxpage).group(1))/10)
except AttributeError:
    maxno=1
    print("Only 1 result page found/Error occured ("+ author + lang +")")
numbers=list(range(0,int(maxno)))


with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    for number in numbers:
        for attempt in range(3):
            try:
                req=request.Request(fetchlink + str(number+1))
                tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
                templinks = tree.xpath(xpathlink)
                tempdate = (tree.xpath(xpathdate))
                temptitle=(tree.xpath(xpathtitle))    
                for dt,tt,lk in zip(tempdate,temptitle, templinks):
                    row = []
                    tmpdt=time.strptime(dt, strtodate)
                    row.append(time.strftime("%d-%m-%Y",tmpdt))
                    row.append(location)
                    row.append(author)
                    row.append(lang)
                    ttf = re.sub("\r|\n|\t","",tt.lstrip())
                    row.append(ttf)
                    row.append(linkbase+lk)
                    writer.writerow(row)
                    i += 1
                time.sleep(randint(1,3))
            except request.HTTPError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 2:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink + str(number+1))
                time.sleep(10)
            except request.URLError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 2:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink + str(number+1))
                time.sleep(10)
            else:
                break
        
print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")


#%% Rutte (NL)
fetchlink = 'https://www.rijksoverheid.nl/documenten?trefwoord=Rutte+&periode-van=01-11-2015&onderdeel=Ministerie+van+Algemene+Zaken&type=Toespraak&pagina='
author="M. Rutte"
location="Netherlands"
lang="NLEN" # we have to figure out the actual language here somehow
xpathmp='//*[@id="content"]/div[2]//h2/span/text()'
regexmp=".*'([0-9]+)'.*"
xpathlink='//*[@class="common results"]/a/@href'
xpathdate='//*[@class="meta"]/text()'
strtodate="\n              Toespraak | %d-%m-%Y"
xpathtitle='//*[@class="publication"]/h3/text()'
linkbase="https://www.rijksoverheid.nl"
i = 0

for attempt in range(3):
    try:
        req=request.Request(url = fetchlink, headers = headers)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        maxpage=str(tree.xpath(xpathmp))
    except request.HTTPError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 2:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except request.URLError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 2:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    else:
        break

try:
    maxno=math.ceil(int(re.match(regexmp,maxpage).group(1))/10)
except AttributeError:
    maxno=1
    print("Only 1 result page found/Error occured ("+ author + lang +")")
numbers=list(range(0,int(maxno)))


with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    for number in numbers:
        for attempt in range(3):
            try:
                req=request.Request(fetchlink + str(number+1))
                tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
                templinks = tree.xpath(xpathlink)
                tempdate = (tree.xpath(xpathdate))
                temptitle=(tree.xpath(xpathtitle))    
                for dt,tt,lk in zip(tempdate,temptitle, templinks):
                    row = []
                    tmpdt=time.strptime(dt, strtodate)
                    row.append(time.strftime("%d-%m-%Y",tmpdt))
                    row.append(location)
                    row.append(author)
                    row.append(lang)
                    ttf = re.sub("\r|\n|\t","",tt.lstrip())
                    row.append(ttf)
                    row.append(linkbase+lk)
                    writer.writerow(row)
                    i += 1
                time.sleep(randint(1,3))
            except request.HTTPError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 2:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink + str(number+1))
                time.sleep(10)
            except request.URLError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 2:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink + str(number+1))
                time.sleep(10)
            else:
                break


print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")

#%% Britain: May (EN) 
# speeches need to be restricted to pages where the following xpath
# ('//*[@id="content"]/div[3]/div[1]/div[1]/div[1]/dl/dd/text()')
# matches the expression '(Transcript of the speech, exactly as it was delivered)'


fetchlink = 'https://www.gov.uk/search/all?order=updated-newest&organisations%5B%5D=prime-ministers-office-10-downing-street&page={}&parent=prime-ministers-office-10-downing-street&people%5B%5D=theresa-may&public_timestamp%5Bfrom%5D=13%2F07%2F2016&public_timestamp%5Bto%5D='
xpathmp = '//*[@id="js-pagination"]/nav/ul/li/a/span[3]/text()'
regexmp = '.*\d* of (\d*)'
author="T. May"
location="Great Britain"
lang="EN"
xpathlink='//*[@id="js-results"]//a/@href'
xpathdate='//*[@id="js-results"]//time/@datetime'
strtodate="%Y-%m-%d"
xpathtitle='//*[@id="js-results"]//a/text()'
linkbase="https://www.gov.uk"

for attempt in range(3):
    try:
        req=request.Request(fetchlink.format(1), headers = headers)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        maxpage=str(tree.xpath(xpathmp))
    except request.HTTPError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 2:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except request.URLError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 2:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    else:
        break

try:
    maxno=(re.match(regexmp,maxpage).group(1))
except AttributeError:
    maxno=1
    print("Only 1 result page found/Error occured ("+ author + lang +")")
numbers=list(range(0,int(maxno)))

i = 0
with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    for number in numbers:
        for attempt in range(3):
            try:
                req=request.Request(fetchlink.format(number+1), headers = headers)
                tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
                templinks = tree.xpath(xpathlink)
                tempdate=(tree.xpath(xpathdate))
                temptitle=(tree.xpath(xpathtitle))    
                for dt,tt,lk in zip(tempdate,temptitle,templinks):    
                    row = []
                    tmpdt=time.strptime(dt, strtodate)
                    row.append(time.strftime("%d-%m-%Y",tmpdt))
                    row.append(location)
                    row.append(author)
                    row.append(lang)
                    ttf = re.sub("\r|\n|\t","",tt.lstrip())
                    try:
                        row.append(re.match('(.*): \d+ .* \d\d\d\d', ttf).group(1))
                    except AttributeError:
                        row.append(ttf)
                    row.append(linkbase+lk)
                    writer.writerow(row)
                    i += 1
                time.sleep(1)
            except request.HTTPError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 2:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink.format(number+1))
                time.sleep(10)
            except request.URLError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 2:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink.format(number+1))
                time.sleep(10)
            else:
                break



print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")

#%% Britain: Cameron (EN)
# speeches need to be restricted to pages where the following xpath
# ('//*[@id="content"]/div[3]/div[1]/div[1]/div[1]/dl/dd/text()')
# matches the expression '(Transcript of the speech, exactly as it was delivered)'

fetchlink = 'https://www.gov.uk/search/all?order=updated-newest&organisations%5B%5D=prime-ministers-office-10-downing-street&page={}&parent=prime-ministers-office-10-downing-street&people%5B%5D=david-cameron&public_timestamp%5Bfrom%5D=01%2F11%2F2015&public_timestamp%5Bto%5D=13%2F07%2F2016'
xpathmp = '//*[@id="js-pagination"]/nav/ul/li/a/span[3]/text()'
regexmp = '.*[0-9] of ([1-9]+)*'
author="D. Cameron"
location="Great Britain"
lang="EN"
xpathlink='//*[@id="js-results"]//a/@href'
xpathdate='//*[@id="js-results"]//time/@datetime'
strtodate="%Y-%m-%d"
xpathtitle='//*[@id="js-results"]//a/text()'
linkbase="https://www.gov.uk"

for attempt in range(3):
    try:
        req=request.Request(fetchlink.format(1), headers = headers)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        maxpage=str(tree.xpath(xpathmp))
    except request.HTTPError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 2:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except request.URLError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 2:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    else:
        break

try:
    maxno=(re.match(regexmp,maxpage).group(1))
except AttributeError:
    maxno=1
    print("Only 1 result page found/Error occured ("+ author + lang +")")
numbers=list(range(0,int(maxno)))

i = 0
with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    for number in numbers:
        for attempt in range(3):
            try:
                req=request.Request(fetchlink.format(number+1), headers = headers)
                tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
                templinks = tree.xpath(xpathlink)
                tempdate=(tree.xpath(xpathdate))
                temptitle=(tree.xpath(xpathtitle))    
                for dt,tt,lk in zip(tempdate,temptitle,templinks):    
                    row = []
                    tmpdt=time.strptime(dt, strtodate)
                    row.append(time.strftime("%d-%m-%Y",tmpdt))
                    row.append(location)
                    row.append(author)
                    row.append(lang)
                    ttf = re.sub("\r|\n|\t","",tt.lstrip())
                    try:
                        row.append(re.match('(.*): \d+ .* \d\d\d\d', ttf).group(1))
                    except AttributeError:
                        row.append(ttf)
                    row.append(linkbase+lk)
                    writer.writerow(row)
                    i += 1
                time.sleep(1)
            except request.HTTPError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 2:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink.format(number+1))
                time.sleep(10)
            except request.URLError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 2:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink.format(number+1))
                time.sleep(10)
            else:
                break



print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")


#%% Sweden (EN)
fetchlink = 'https://www.government.se/speeches/'
author="S.Loefven"
location="Sweden"
lang="EN"
xpathmp='//*[@id="tabs--primo--alpha-fragment-1-result"]/div[2]/div/h2/span[2]/strong[1]'
regexmp="[0-9]+"
strtodate="%d %B %Y"
num = 0
i = 0

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
                    row.append(time.strftime("%d-%m-%Y", tmpdt))
                    row.append(location)
                    row.append(author)
                    row.append(lang)
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
            print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink.format(number+1))
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink.format(number+1))
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
                    row = []
                    row.append(time.strftime("%d-%m-%Y", tmpdt))
                    row.append(location)
                    row.append(author)
                    row.append(lang)
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
            print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink.format(number+1))
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink.format(number+1))
            time.sleep(10)
        except NoSuchElementException:
            break

driver.close()

print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")


#%% Denmark (EN)
fetchlink = 'http://www.stm.dk/index.dsp?page=11004&action=page_overview_search&l1_valg=-1&l2_valg=-1'

author1 = 'L. Rasmussen'
author2 = 'H. Thorning-Schmidt'
author3 = 'L. Rasmussen'
author4 = 'A. Rasmussen'
author5 = 'P. Rasmussen'

change1 = '28-06-2015'
change2 = '03-10-2011'
change3 = '05-04-2009'
change4 = '27-11-2001'

location="Denmark"
lang="EN"
xpathlink='//*[@class="page-overview-search-result-items"]/div[*]/div/div[1]/a/@href'
xpathdate='//*[@class="page-overview-search-result-items"]/div[*]/div/div[1]/span/text()'
xpathtitle='//*[@class="page-overview-search-result-items"]/div[*]/div/div[1]/a/text()'
strtodate="%d.%m.%y"
linkbase="http://www.stm.dk/"
i = 0

with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    for attempt in range(3):
        try:
            req=request.Request(url = fetchlink, headers = headers)
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            templinks = tree.xpath(xpathlink)
            tempdate = (tree.xpath(xpathdate))
            temptitle = (tree.xpath(xpathtitle))    
            for dt,tt,lk in zip(tempdate,temptitle,templinks):    
                tmpdt=time.strptime(dt, strtodate)
                row = []
                row.append(time.strftime("%d-%m-%Y",tmpdt))
                row.append(location)
                if time.strptime(dt, strtodate) > time.strptime(change1, "%d-%m-%Y"):
                    row.append(author1)
                elif time.strptime(dt, strtodate) < time.strptime(change1, "%d-%m-%Y") and time.strptime(dt, strtodate) > time.strptime(change2, "%d-%m-%Y"):
                    row.append(author2)
                elif time.strptime(dt, strtodate) < time.strptime(change2, "%d-%m-%Y") and time.strptime(dt, strtodate) > time.strptime(change3, "%d-%m-%Y"):
                    row.append(author3)
                elif time.strptime(dt, strtodate) < time.strptime(change3, "%d-%m-%Y") and time.strptime(dt, strtodate) > time.strptime(change4, "%d-%m-%Y"):
                    row.append(author4)
                elif time.strptime(dt, strtodate) < time.strptime(change4, "%d-%m-%Y"):
                    row.append(author5)
                else:
                    print("Faulty date error: " + dt)
                row.append(lang)
                ttf = re.sub("\r|\n|\t","",tt.lstrip())
                try:
                    row.append(re.match('.*:', ttf).group(0))
                except AttributeError:
                    row.append(ttf)
                row.append(linkbase+lk)
                writer.writerow(row)
                i += 1
            time.sleep(randint(1,3))
        except request.HTTPError:
            print("Whoops, that went wrong, retrying page for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink)
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink)
            time.sleep(10)
        else:
            break


print("Finished fetching " + str(i) + " Denmark " + lang + " speech links\n\n")


#%% Denmark (DK)
fetchlink = 'http://www.stm.dk/index.dsp?page=7990&action=page_overview_search&l1_valg=-1&l2_valg=-1'
lang="DK"
xpathlink='//*[@class="page-overview-search-result-items"]/div[*]/div/div[1]/a/@href'
xpathdate='//*[@class="page-overview-search-result-items"]/div[*]/div/div[1]/span/text()'
xpathtitle='//*[@class="page-overview-search-result-items"]/div[*]/div/div[1]/a/text()'
strtodate="%d.%m.%y"
linkbase="http://www.stm.dk/"
i = 0

with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    for attempt in range(3):
        try:
            req=request.Request(url = fetchlink, headers = headers)
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            templinks = tree.xpath(xpathlink)
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt,lk in zip(tempdate,temptitle,templinks):    
                tmpdt=time.strptime(dt, strtodate)
                row = []
                row.append(time.strftime("%d-%m-%Y",tmpdt))
                row.append(location)
                if time.strptime(dt, strtodate) > time.strptime(change1, "%d-%m-%Y"):
                    row.append(author1)
                elif time.strptime(dt, strtodate) < time.strptime(change1, "%d-%m-%Y") and time.strptime(dt, strtodate) > time.strptime(change2, "%d-%m-%Y"):
                    row.append(author2)
                elif time.strptime(dt, strtodate) < time.strptime(change2, "%d-%m-%Y") and time.strptime(dt, strtodate) > time.strptime(change3, "%d-%m-%Y"):
                    row.append(author3)
                elif time.strptime(dt, strtodate) < time.strptime(change3, "%d-%m-%Y") and time.strptime(dt, strtodate) > time.strptime(change4, "%d-%m-%Y"):
                    row.append(author4)
                elif time.strptime(dt, strtodate) < time.strptime(change4, "%d-%m-%Y"):
                    row.append(author5)
                else:
                    print("Faulty date error: " + dt)
                row.append(lang)
                ttf = re.sub("\r|\n|\t","",tt.lstrip())
                try:
                    row.append(re.match('.*:', ttf).group(0))
                except AttributeError:
                    row.append(ttf)
                row.append(linkbase+lk)
                writer.writerow(row)
                i += 1
            time.sleep(randint(1,5))
        except request.HTTPError:
            print("Whoops, that went wrong, retrying page for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink)
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink)
            time.sleep(10)
        else:
            break

print("Finished fetching " + str(i) + " Denmark " + lang + " speech links\n\n")


#%% Norway (EN)
fetchlink = 'https://www.regjeringen.no/en/whatsnew/speeches_articles/id1334/?ownerid=875&page='
linkbase = 'https://www.regjeringen.no'
xpathmp = '//*[@id="mainContent"]/div[2]/div/div/p[1]/text()'
regexmp = '.*(Showing [0-9]*-[0-9]* of )([0-9]*)( results.).*'
xpathlink = '//*[@id="searchResultsListing"]/li[*]/h2/a/@href'
xpathdate = '//*[@id="searchResultsListing"]/li[*]/div/span[1]/text()'
xpathtitle = '//*[@id="searchResultsListing"]/li[*]/h2/a/text()'
author = 'E. Solberg'
location = 'Norway'
lang = 'EN'
strtodate = '%d/%m/%Y'
i = 0


for attempt in range(5):
    try:
        req=request.Request(fetchlink)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        maxpage=str(tree.xpath(xpathmp))
    except request.HTTPError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except request.URLError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except ConnectionResetError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)    
    else:
        break

maxno=int((int(re.match(regexmp,maxpage).group(2))-1)/20)+1

with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    for page in range(maxno):
        for attempt in range(3):
            try:
                req=request.Request(url = str(fetchlink + str(page + 1)), headers = headers)
                tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
                templinks = tree.xpath(xpathlink)
                tempdate=(tree.xpath(xpathdate))
                temptitle=(tree.xpath(xpathtitle))
                for dt,tt,lk in zip(tempdate,temptitle,templinks):
                    row = []
                    tmpdt=time.strptime(dt, strtodate)
                    row.append(time.strftime("%d-%m-%Y",tmpdt))
                    row.append(location)
                    row.append(author)
                    row.append(lang)
                    ttf = re.sub("\r|\n|\t","",tt.lstrip())
                    row.append(re.match("[^\s*].*[^\s*]", ttf).group(0))
                    row.append(linkbase+lk)
                    writer.writerow(row)
                    i += 1
                time.sleep(randint(1,5))
            except request.HTTPError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 2:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink + str(number+1))
                time.sleep(10)
            except request.URLError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 2:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink + str(number+1))
                time.sleep(10)
            else:
                break


print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")

#%% Norway (NO)
fetchlink = 'https://www.regjeringen.no/no/aktuelt/taler_artikler/id1334/?ownerid=875&page='
linkbase = 'https://www.regjeringen.no'
xpathmp = '//*[@id="mainContent"]/div[2]/div/div/p[1]/text()'
regexmp = '.*(Viser [0-9]*-[0-9]* av )([0-9]*)( treff.).*'
xpathlink = '//*[@id="searchResultsListing"]/li[*]/h2/a/@href'
xpathdate = '//*[@id="searchResultsListing"]/li[*]/div/span[1]/text()'
xpathtitle = '//*[@id="searchResultsListing"]/li[*]/h2/a/text()'
author = 'E. Solberg'
location = 'Norway'
lang = 'NO'
strtodate = '%d.%m.%Y'
i = 0


for attempt in range(5):
    try:
        req=request.Request(fetchlink)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        maxpage=str(tree.xpath(xpathmp))
    except request.HTTPError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except request.URLError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except ConnectionResetError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)    
    else:
        break

maxno=int((int(re.match(regexmp,maxpage).group(2))-1)/20)+1


with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    for page in range(maxno):
        for attempt in range(3):
            try:
                req=request.Request(url = str(fetchlink + str(page + 1)), headers = headers)
                tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
                templinks = tree.xpath(xpathlink)
                tempdate=(tree.xpath(xpathdate))
                temptitle=(tree.xpath(xpathtitle))
                for dt,tt,lk in zip(tempdate,temptitle,templinks):
                    row = []
                    tmpdt=time.strptime(dt, strtodate)
                    row.append(time.strftime("%d-%m-%Y",tmpdt))
                    row.append(location)
                    row.append(author)
                    row.append(lang)
                    ttf = re.sub("\r|\n|\t","",tt.lstrip())
                    row.append(re.match("[^\s*].*[^\s*]", ttf).group(0))
                    row.append(linkbase+lk)
                    writer.writerow(row)
                    i += 1
                time.sleep(randint(1,5))
            except request.HTTPError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 2:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink + str(number+1))
                time.sleep(10)
            except request.URLError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 2:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink + str(number+1))
                time.sleep(10)
            else:
                break

print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")

#%% Estonia (EN)
fetchlink = 'https://www.valitsus.ee/en/news?title=&title_op=allwords&source=23&date=All&date_custom%5Bmin%5D=&date_custom%5Bmax%5D=&field_news_subject_tid_i18n=139&page='
xpathmp = '//*[@id="block-system-main"]/div/div/div/div[2]/ul/li[*]/a/text()'
regexmp = '.*(\d)'
xpathlink = '//*[@id="block-system-main"]/div/div/div/div[1]/div[*]/div[2]/h2/a/@href'
xpathdate = '//*[@id="block-system-main"]/div/div/div/div[1]/div[*]/div[2]/div[1]/text()[1]'
xpathtitle = '//*[@id="block-system-main"]/div/div/div/div[1]/div[*]/div[2]/h2/a/text()'
author = 'J. Ratas'
location = 'Estonia'
lang = 'EN'
linkbase="https://www.valitsus.ee"
strtodate = '%d.%m.%Y'
i = 0


for attempt in range(5):
    try:
        req=request.Request(fetchlink)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        maxpage=str(tree.xpath(xpathmp))
    except request.HTTPError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except request.URLError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except ConnectionResetError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)    
    else:
        break

maxno=int(re.match(regexmp,maxpage).group(1))

with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')

    for page in range(maxno):
        for attempt in range(3):
            try:
                req=request.Request(url = str(fetchlink + str(page)))
                tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
                templinks = tree.xpath(xpathlink)
                tempdate=(tree.xpath(xpathdate))
                temptitle=(tree.xpath(xpathtitle))
                for dt,tt,lk in zip(tempdate,temptitle, templinks):
                    tmpdt=time.strptime(dt, strtodate)
                    row = []
                    row.append(time.strftime("%d-%m-%Y",tmpdt))
                    row.append(location)
                    row.append(author)
                    row.append(lang)
                    ttf = re.sub("\r|\n|\t","",tt.lstrip())
                    row.append(ttf)
                    row.append(linkbase+lk)
                    writer.writerow(row)
                    i += 1
                time.sleep(randint(1,5))
            except request.HTTPError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 2:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink + str(number+1))
                time.sleep(10)
            except request.URLError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 2:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink + str(number+1))
                time.sleep(10)
            else:
                break
    
print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")

#%% Estonia (EE)
fetchlink = 'https://www.valitsus.ee/et/uudised?title=&title_op=allwords&source=23&date=All&date_custom%5Bmin%5D=&date_custom%5Bmax%5D=&field_news_subject_tid_i18n=139&page='
xpathmp = '//*[@id="block-system-main"]/div/div/div/div[2]/ul/li[*]/a/text()'
regexmp = '.*(\d)'
xpathlink = '//*[@id="block-system-main"]/div/div/div/div[1]/div[*]/div[2]/h2/a/@href'
xpathdate = '//*[@id="block-system-main"]/div/div/div/div[1]/div[*]/div[2]/div[1]/text()[1]'
xpathtitle = '//*[@id="block-system-main"]/div/div/div/div[1]/div[*]/div[2]/h2/a/text()'
author = 'J. Ratas'
location = 'Estonia'
lang = 'EE'
linkbase="https://www.valitsus.ee"
strtodate = '%d.%m.%Y'


for attempt in range(5):
    try:
        req=request.Request(fetchlink)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        maxpage=str(tree.xpath(xpathmp))
    except request.HTTPError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except request.URLError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except ConnectionResetError:
        print("Whoops, that went wrong, retrying first page for "+author+ " "+ lang)
        if attempt == 4:
            print("Fetching first page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)    
    else:
        break

maxno=int(re.match(regexmp,maxpage).group(1))

i = 0
with open(linkpath, mode="a", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')

    for page in range(maxno):
        for attempt in range(3):
            try:
                req=request.Request(url = str(fetchlink + str(page)))
                tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
                templinks = tree.xpath(xpathlink)
                tempdate=(tree.xpath(xpathdate))
                temptitle=(tree.xpath(xpathtitle))
                for dt,tt,lk in zip(tempdate,temptitle, templinks):
                    tmpdt=time.strptime(dt, strtodate)
                    row = []
                    row.append(time.strftime("%d-%m-%Y",tmpdt))
                    row.append(location)
                    row.append(author)
                    row.append(lang)
                    ttf = re.sub("\r|\n|\t","",tt.lstrip())
                    row.append(ttf)
                    row.append(linkbase+lk)
                    writer.writerow(row)
                    i += 1
                time.sleep(randint(1,5))
            except request.HTTPError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 2:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink + str(number+1))
                time.sleep(10)
            except request.URLError:
                print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author+ " "+ lang)
                if attempt == 2:
                    print("Fetching result page " + str(number+1) + author + lang + " failed due to HTTPError")
                    deadlinks.append(fetchlink + str(number+1))
                time.sleep(10)
            else:
                break
    

print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")


# =============================================================================
# #%% Spain - unstable website, not scrapable

# fetchlink="http://www.lamoncloa.gob.es/presidente/intervenciones/Paginas/index.aspx?mts="
# author1="M.Rajoy"
# author2="P.Sanchez"
# dateswitch = time.strptime("02/06/2018","%d/%m/%Y")
# datestart = time.strptime("31/10/2015","%d/%m/%Y")
# datestop =  time.strptime("13/05/2019","%d/%m/%Y")
# location="Spain"
# lang="ES"
# xpathmp='//*[@id="ctl00_PlaceHolderMain_DisplayMode_ctl00_Summary_EditModePanel_ctl01_hdnLastPage"]'
# xpathlink='//*[@id="columnContentContainer"]/ul/li[*]/div/p[1]/a'
# xpathdate='//*[@id="columnContentContainer"]/ul/li[*]/div/p[1]/a' #date in title
# strtodate="%d/%m/%Y"
# xpathtitle='//*[@id="columnContentContainer"]/ul/li[*]/div/p[1]/a'
# linkbase="http://www.lamoncloa.gob.es"
# xpathsel = '//*[@id="ctl00_PlaceHolderMain_DisplayMode_ctl00_Summary_EditModePanel_ctl01_btnPage{}"]'
# xpathelmt = '//*[@id="columnContentContainer"]/ul/li[*]/div/p[1]/a'
# opts = Options()
# opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36")
# 
# driver = webdriver.Chrome(options=opts)
# driver.set_page_load_timeout(5)
# 
# #Generating yearmonth url postfixes for scraping results
# speechlinks=[]
# maxno = 0
# num=list(range(1,13)) 
# years=list(range(2015,2020))
# numbers=[]
# for year in years:
#     for n in num:
#         no=str(year)+str(format(n,'02'))
#         numbers.append(no)
# 
# 
# with open(linkpath, mode="a", encoding="utf-8") as fo:
#     writer=csv.writer(fo, lineterminator = '\n')
# 
#     for number in numbers:
#         i = 0
#         for attempt in range(3):
#             try:
#                 if time.strptime(number, '%Y%m') > datestart and time.strptime(number, '%Y%m') < datestop:
#                     print('Starting with: ' + str(number) + '...')
#                     fetchurl = fetchlink + str(number)
#                     time.sleep(3)
#                     driver.get(fetchurl)
#                     maxpage = driver.find_element_by_xpath(xpathmp).get_attribute('value')
#                     try:
#                         maxno=int(maxpage)
#                     except IndexError:
#                         maxno=1
#                     for attempt2 in range(3):
#                         try:
#                             templinks = driver.find_elements_by_xpath(xpathlink)
#                             temptitle = driver.find_elements_by_xpath(xpathtitle)
#                             for tt, lk in zip(temptitle, templinks):
#                                 row = []
#                                 tmpdt=time.strptime(tt.get_attribute('title').split(".")[0], strtodate)
#                                 row.append(time.strftime("%d-%m-%Y",tmpdt))
#                                 row.append(location)
#                                 if tmpdt < dateswitch:                  
#                                     row.append(author1)
#                                 else:
#                                     row.append(author2)
#                                 row.append(lang)
#                                 row.append(tt.get_attribute('title').split(".")[1])
#                                 row.append(lk.get_attribute('href'))
#                                 writer.writerow(row)
#                                 i += 1
#                             if int(maxno) >= 2:
#                                 for no in range(2, (int(maxno)+1)):
#                                     button = driver.find_element_by_xpath(xpathsel.format(3))
#                                     button.click()
#                                     time.sleep(3)
#                                     templinks2 = driver.find_elements_by_xpath(xpathlink)
#                                     temptitle2 = driver.find_elements_by_xpath(xpathtitle)
#                                     for tt, lk in zip(temptitle2, templinks2):
#                                         row = []
#                                         tmpdt=time.strptime(tt.get_attribute('title').split(".")[0], strtodate)
#                                         row.append(time.strftime("%d-%m-%Y",tmpdt))
#                                         row.append(location)
#                                         if tmpdt < dateswitch:                  
#                                             row.append(author1)
#                                         else:
#                                             row.append(author2)
#                                         row.append(lang)
#                                         row.append(tt.get_attribute('title').split(".")[1])
#                                         row.append(lk.get_attribute('href'))
#                                         writer.writerow(row)
#                                         i += 1
#                         except request.HTTPError:
#                             print("Whoops, that went wrong, retrying page "+str(number) +" for "+author1+ " "+ lang)
#                             time.sleep(5)
#                             if attempt2 == 2:
#                                 print("Fetching result page " + str(number) +  author1 + lang + " failed due to HTTPError")
#                                 deadlinks.append(fetchlink +str(number))
#                         except request.URLError:
#                             print("Whoops, that went wrong, retrying page "+str(number) + " for " + author1 + " " + lang)
#                             time.sleep(5)
#                             if attempt2 == 2:
#                                 print("Fetching result page " + str(number) + author1 + lang + " failed due to HTTPError")
#                                 deadlinks.append(fetchlink +str(number))
#                         except TimeoutException:
#                             if attempt == 2:
#                                 print("Fetching result page " + str(number) + author1 + lang + " failed due to TimeOut")
#                                 deadlinks.append(fetchlink)
#                             print('TimeOut, trying again...')
#                             driver.set_page_load_timeout(30)
#                         except NoSuchElementException:
#                             if attempt == 2:
#                                 print("Fetching result page " + str(number) + author1 + lang + " failed due to NoSuchElementException")
#                                 deadlinks.append(fetchlink)
#                             print('NoSuchElement, trying again...')
#                             driver.set_page_load_timeout(30)
#                         except ConnectionError:
#                             if attempt == 2:
#                                 print("Fetching result page " + str(number) + author1 + lang + " failed due to ConnectionError")
#                                 deadlinks.append(fetchlink)
#                             print('ConnectionError, trying again...')      
#                         except WebDriverException:
#                             continue
#                         else:
#                             break
#                     print(str(number) + ": fetched " + str(i) + " links from " + str(maxno) + " page(s)")
#                     driver.set_page_load_timeout(5)
#             except request.HTTPError:
#                 print("Whoops, that went wrong, retrying first page for "+author1+ " "+ lang)
#                 if attempt == 2:
#                     print("Fetching first page Spain " + number + lang + " failed due to HTTPError")
#                     deadlinks.append(fetchlink)
#             except request.URLError:
#                 print("Whoops, that went wrong, retrying first page for "+author1+ " "+ lang)
#                 if attempt == 2:
#                    print("Fetching first page " + author1 + lang + " failed due to HTTPError")
#                    deadlinks.append(fetchlink)
#             except TimeoutException:
#                 if attempt == 2:
#                     print("Fetching first page " + author1 + lang + " failed due to TimeOut")
#                     deadlinks.append(fetchlink)
#                 print('TimeOut, trying again...')
#                 driver.set_page_load_timeout(30)
#             except NoSuchElementException:
#                 if attempt == 2:
#                     print("Fetching first page " + author1 + lang + " failed due to NoSuchElementException") # if element is missing here, it's due to webpage not loading
#                     deadlinks.append(fetchlink)
#                 print('NoSuchElement, trying again...')
#                 driver.set_page_load_timeout(30)
#             except ConnectionError:
#                 if attempt == 2:
#                     print("Fetching first page " + author1 + lang + " failed due to ConnectionError") # if element is missing here, it's due to webpage not loading
#                     deadlinks.append(fetchlink)
#                 print('ConnectionError, trying again...')            
#             except WebDriverException:
#                 continue      
#             else:
#                 break
# 
# driver.quit()
# 
# for link in speechlinks:
#         completelinks.append(link)
# 
# print("Finished fetching " + fetchlink + " " + author1 + ' and ' + author2 + " " + lang + " speech links\n\n")
# 
# 
# =============================================================================


# =============================================================================
# #%% Fetching Tsipras speech links (GR) - website down for the last few weeks
# author="A. Tsipras"
# stoptime=time.strptime("01/11/2015","%d/%m/%Y")
# today = datetime.datetime.now().strftime("%Y-%m-%d")
# location="Greece"
# lang="GR"
# xpathlink='//*[@id="td-outer-wrap"]/div[2]/div/div[2]/div[1]/div/div[*]/div[2]/h3/a/@href'
# xpathdate='//*[@id="td-outer-wrap"]/div[2]/div/div[2]/div[1]/div/div[*]/div[2]/div[1]/span/time/@datetime'
# strtodate="%Y-%m-%d"
# linktodate=".*/([0-9]+/[0-9]+/[0-9]+)/.*"
# xpathtitle='//*[@id="td-outer-wrap"]/div[2]/div/div[2]/div[1]/div/div[*]/div[2]/h3/a/text()'
# linkbase = 'https://primeminister.gr/'
# 
# # this generates a link for every month between 11/2015 and today, then 
# # checks whether page is available. this is to circumvent the 'infinite 
# # scrolling page' with a 'load more'-button. 
# 
# # scraped sites to be verified through //*[@id="post-21336"]
# # this should contain a tag 'category-speeches'
# 
# # collect using selenium??
# 
# i = 0
# page = 0
# 
# with open(linkpath, mode="a", encoding="utf-8") as fo:
#     writer=csv.writer(fo, lineterminator = '\n')
#     for year in [2019, 2018, 2017, 2016, 2015]:
#         for month in range(13)[1:]:
#             for page in range(5)[1:]:
#                 if time.strptime((str(year)+'-'+str(month)), '%Y-%m') < time.strptime(today, strtodate) and time.strptime((str(year)+'-'+str(month)), '%Y-%m') > stoptime:
#                     fetchlink = linkbase+str(year)+"/"+str(month)+"/page/"+str(page)+"/"
#                     try:
#                         n = 0
#                         req=request.Request(url = fetchlink, headers = headers)
#                         tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
#                         templinks = tree.xpath(xpathlink)
#                         tempdate=(tree.xpath(xpathdate))
#                         temptitle=(tree.xpath(xpathtitle))
#                         for dt,tt,lk in zip(tempdate,temptitle,templinks):    
#                             try:            
#                                 row = []
#                                 tmpdt=time.strptime(dt[0:10], strtodate)
#                                 row.append(time.strftime("%d-%m-%Y", tmpdt))
#                                 row.append(location)
#                                 row.append(author)
#                                 row.append(lang)
#                                 ttf = re.sub("\r|\n|\t","",tt.lstrip())
#                                 row.append(ttf)
#                                 row.append(lk)
#                                 n += 1
#                                 i += 1
#                             except AttributeError:
#                                 tmpdt=time.strptime("2099-01-01", strtodate)
#                                 print("Date not available")
#                                 deadlinks.append("Date not available")
#                             except ValueError:
#                                 tmpdt=time.strptime("2099-01-01", strtodate)
#                                 print("Date not available")
#                                 deadlinks.append("Date not available")
#                         print(str(n)+" links fetched: "+str(year)+"/"+str(month)+"/page/"+str(page)+" for " + author)
#                         if n < 10:
#                             break
#                         time.sleep(5)
#                     except request.HTTPError:
#                         print("Whoops, that went wrong, HTTPError page "+str(year)+"/"+str(month)+"/page/"+str(page)+" for " + author)
#                         break
#                     except request.URLError:
#                         print("Whoops, that went wrong, URLError page "+str(year)+"/"+str(month)+"/page/"+str(page)+" for " + author)
#                         deadlinks.append(fetchlink)
#                         break
#                 else:
#                     pass
# 
# 
# print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")
# 
# #%% Greece (EN)
# author="A. Tsipras"
# stoptime=time.strptime("01/03/2017","%d/%m/%Y")
# today = datetime.datetime.now().strftime("%Y-%m-%d")
# location="Greece"
# lang="EN"
# xpathlink='//*[@id="td-outer-wrap"]/div[2]/div/div[2]/div[1]/div/div[*]/div[2]/h3/a/@href'
# xpathdate='//*[@id="td-outer-wrap"]/div[2]/div/div[2]/div[1]/div/div[*]/div[2]/div[1]/span/time/@datetime'
# strtodate="%Y-%m-%d"
# linktodate=".*/([0-9]+/[0-9]+/[0-9]+)/.*"
# xpathtitle='//*[@id="td-outer-wrap"]/div[2]/div/div[2]/div[1]/div/div[*]/div[2]/h3/a/text()'
# linkbase = 'https://primeminister.gr/'
# 
# 
# # scraped sites to be verified through //*[@id="post-XXXXX"]
# # this should contain a tag 'category-speeches'
# 
# i = 0
# page = 0
# 
# with open(linkpath, mode="a", encoding="utf-8") as fo:
#     writer=csv.writer(fo, lineterminator = '\n')
#     for year in [2019, 2018, 2017, 2016, 2015]:
#         for month in range(13)[1:]:
#             for page in range(5)[1:]:
#                 if time.strptime((str(year)+'-'+str(month)), '%Y-%m') < time.strptime(today, strtodate) and time.strptime((str(year)+'-'+str(month)), '%Y-%m') > stoptime:
#                     fetchlink = linkbase+'en/'+str(year)+"/"+str(month)+"/page/"+str(page)+"/"
#                     try:
#                         n = 0
#                         req=request.Request(url = fetchlink, headers = headers)
#                         tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
#                         templinks = tree.xpath(xpathlink)
#                         tempdate=(tree.xpath(xpathdate))
#                         temptitle=(tree.xpath(xpathtitle))
#                         for dt,tt,lk in zip(tempdate,temptitle,templinks):    
#                             try:            
#                                 row = []
#                                 tmpdt=time.strptime(dt[0:10], strtodate)
#                                 row.append(time.strftime("%d-%m-%Y", tmpdt))
#                                 row.append(location)
#                                 row.append(author)
#                                 row.append(lang)
#                                 ttf = re.sub("\r|\n|\t","",tt.lstrip())
#                                 row.append(ttf)
#                                 row.append(lk)
#                                 writer.writerow(row)
#                                 n += 1
#                                 i += 1
#                             except AttributeError:
#                                 tmpdt=time.strptime("2099-01-01", strtodate)
#                                 print("Date not available")
#                                 deadlinks.append("Date not available")
#                             except ValueError:
#                                 tmpdt=time.strptime("2099-01-01", strtodate)
#                                 print("Date not available")
#                                 deadlinks.append("Date not available")
#                         print(str(n)+" links fetched: "+str(year)+"/"+str(month)+"/page/"+str(page)+" for " + author)
#                         if n < 10:
#                             break
#                         time.sleep(5)
#                     except request.HTTPError:
#                         print("Whoops, that went wrong, HTTPError page "+str(year)+"/"+str(month)+"/page/"+str(page)+" for " + author)
#                         break
#                     except request.URLError:
#                         print("Whoops, that went wrong, URLError page "+str(year)+"/"+str(month)+"/page/"+str(page)+" for " + author)
#                         deadlinks.append(fetchlink)
#                         break
#                 else:
#                     pass
# 
# 
# 
# print("Finished fetching " + str(i) + " " + author + " " + lang + " speech links\n\n")
# 
# =============================================================================


#%% write deadlinks into csv
deadlinkpath =  "C:/Users/samunico/OneDrive/Dokumente/Studium/"+\
                "Amsterdam/Gijs/Speeches/Scraping/I - Linkscraping/"+\
                "LinksCombinedDeadlinks/"+now+".csv"

output= zip(deadlinks)
with open(deadlinkpath,mode="w",encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    writer.writerows(output)

print('Finished link collection, with {} dead fetchlinks.\n'.format(len(deadlinks)))

if len(deadlinks) > 0:
    print('Printing dead links:')
    print(deadlinks)  
    