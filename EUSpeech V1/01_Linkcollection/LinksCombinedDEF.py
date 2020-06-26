# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 14:33:14 2015

@author: EdV
"""
# Notes:
# 1. Elysee.fr script not included because it uses selenium, and is only used to scrape Hollande speeches. Using vie-publique.fr instead
# 2. Merkel links are scraped, but only have date info in url. This sometimes does not work, so for some links the date is missing (7 on 13-10-15)
# 3. UK Archive and Spain links are scraped all at once, which means the author of the speech is determined based on the date of publication
#** 4. Spain links contain (on a first look) more than just speeches, needs to be checked
#** 5. UK Archive website provides more than just speeches, need to be filtered after scraping, as search function cannot be used, and URL's are not consistent
#** 6. Greek and UK Wayback/Archive links have some duplicates, which still have to be filtered out
# 7. IMF is scraping speeches from all representatives, not just Christine Lagarde.
# 8. EPP script not added because not yielding results, after investigating page also seems that it redirects to the official ep site for speeches, thus it is not an additional resource
# 9. EP_plenary script not added because it does not actually fetch plenary links, but is an unfinished version of the Brown script
# 10. The EP scripts currently write different language metadata for different authors, but it seems like most speeches are in English anyway, so not sure why this is so.
from lxml import html, etree
from urllib import request
from random import randint
import requests
import itertools
import time
import re
import math
completelinks=[]
date=[]
speaker=[]
country=[]
language=[]
title=[]
deadlinks=[]
#%% Fetching Balkenende English speech links
fetchlink="https://www.government.nl/ministries/ministry-of-general-affairs/documents?keyword=Balkenende&period-from=01-01-2007&period-to=14-11-2010&issue=All+issues&type=Speech&page="
author="J.P. Balkenende"
location="Netherlands"
lang="EN"
xpathmp='//*[@id="content"]/div[1]/h2/span/text()'
regexmp=".*'([0-9]+)'.*"
xpathlink='//*[@class="common results"]/a/@href'
xpathdate='//*[@class="meta"]/text()'
strtodate="\n              Speech | %d-%m-%Y"
xpathtitle='//*[@class="publication"]/h3/text()'
linkbase="https://www.government.nl"

for attempt in range(3):
    try:
        req=request.Request(fetchlink)
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
speechlinks=[]
for number in numbers:
    for attempt in range(3):
        try:
            req=request.Request(fetchlink + str(number+1))
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            speechlinks.append(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt in zip(tempdate,temptitle):    
                tmpdt=time.strptime(dt, strtodate)
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                deadlinks.append("0")
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
flatlinks=list(itertools.chain(*speechlinks))
## Adding url prefix to href tags to make them usable
for link in flatlinks:
    completelink=linkbase + link
    completelinks.append(completelink)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%% Fetching Balkenende Dutch speech links
fetchlink="https://www.rijksoverheid.nl/ministeries/ministerie-van-algemene-zaken/documenten?trefwoord=Balkenende&periode-van=01-01-2007&periode-tot=14-11-2010&type=Toespraak&pagina="
author="J.P. Balkenende"
location="Netherlands"
lang="NL"
xpathmp='//*[@id="content"]/div[1]/h2/span/text()'
regexmp=".*'([0-9]+)'.*"
xpathlink='//*[@class="common results"]/a/@href'
xpathdate='//*[@class="meta"]/text()'
strtodate="\n              Toespraak | %d-%m-%Y"
xpathtitle='//*[@class="publication"]/h3/text()'
linkbase="https://www.rijksoverheid.nl"

for attempt in range(3):
    try:
        req=request.Request(fetchlink)
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
speechlinks=[]
for number in numbers:
    for attempt in range(3):
        try:
            req=request.Request(fetchlink + str(number+1))
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            speechlinks.append(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt in zip(tempdate,temptitle):    
                tmpdt=time.strptime(dt, strtodate)
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                deadlinks.append("0")
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
flatlinks=list(itertools.chain(*speechlinks))
## Adding url prefix to href tags to make them usable
for link in flatlinks:
    completelink=linkbase + link
    completelinks.append(completelink)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")

#%% Fetching Rutte English speech links
fetchlink="https://www.government.nl/government/contents/members-of-cabinet/mark-rutte/documents?type=Speech&page="
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

for attempt in range(3):
    try:
        req=request.Request(fetchlink)
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
speechlinks=[]
for number in numbers:
    for attempt in range(3):
        try:
            req=request.Request(fetchlink + str(number+1))
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            speechlinks.append(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt in zip(tempdate,temptitle):    
                tmpdt=time.strptime(dt, strtodate)
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                deadlinks.append("0")
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

flatlinks=list(itertools.chain(*speechlinks))
## Adding url prefix to href tags to make them usable
for link in flatlinks:
    completelink=linkbase + link
    completelinks.append(completelink)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%% Fetching Rutte Dutch speech links
fetchlink="https://www.rijksoverheid.nl/regering/inhoud/bewindspersonen/mark-rutte/documenten?trefwoord=&periode-van=&periode-tot=&type=Toespraak&pagina="
author="M. Rutte"
location="Netherlands"
lang="NL"
xpathmp='//*[@id="content"]/div[1]/h2/span/text()'
regexmp=".*'([0-9]+)'.*"
xpathlink='//*[@class="common results"]/a/@href'
xpathdate='//*[@class="meta"]/text()'
strtodate="\n              Toespraak | %d-%m-%Y"
xpathtitle='//*[@class="publication"]/h3/text()'
linkbase="https://www.rijksoverheid.nl"

for attempt in range(3):
    try:
        req=request.Request(fetchlink)
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

speechlinks=[]
for number in numbers:
    for attempt in range(3):
        try:
            req=request.Request(fetchlink + str(number+1))
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            speechlinks.append(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt in zip(tempdate,temptitle):    
                tmpdt=time.strptime(dt, strtodate)
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                deadlinks.append("0")
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

flatlinks=list(itertools.chain(*speechlinks))
## Adding url prefix to href tags to make them usable
for link in flatlinks:
    completelink=linkbase + link
    completelinks.append(completelink)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%% Fetching Cameron English speech links
fetchlink="https://www.gov.uk/government/announcements?announcement_type_option=speeches&departments%5B%5D=prime-ministers-office-10-downing-street&keywords=&topics%5B%5D=all&page="
author="D. Cameron"
location="Great Britain"
lang="EN"
xpathmp='//*[@class="next"]/a/span[@class="page-numbers"]/text()'
regexmp=".*[0-9] of ([0-9]+).*"
xpathlink='//*[@class="document-row"]/h3/a/@href'
xpathdate='//*[@class="public_timestamp"]/@datetime'
strtodate="%Y-%m-%d"
xpathtitle='//*[@class="document-row"]/h3/a/text()'
linkbase="https://www.gov.uk"

for attempt in range(3):
    try:
        req=request.Request(fetchlink)
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

speechlinks=[]
for number in numbers:
    for attempt in range(3):
        try:
            req=request.Request(fetchlink + str(number+1))
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            speechlinks.append(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt in zip(tempdate,temptitle):    
                tmpdt=time.strptime(dt[:10], strtodate)
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                deadlinks.append("0")
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

flatlinks=list(itertools.chain(*speechlinks))

for link in flatlinks:
    completelink=linkbase + link
    completelinks.append(completelink)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%% Fetching Chirac French speech links
fetchlink="http://www.vie-publique.fr/rechercher/recherche.php?query=%22D%C3%A9claration%20de%20M.%20Jacques%20Chirac%22&date=&dateDebut=2007/01/01&dateFin=2007/05/16&skin=cdp&replies=100&filter=&typeloi=&auteur=f/vp_auteurphysique/chirac%20jacques&typeDoc=f/vp_type_discours/declaration&source=&sort=document_date_publication&q="
author="J. Chirac"
location="France"
lang="FR"
xpathlink='//*[@class="titre"]/a/@href'
xpathdate='//*[@class="date"]/text()'
strtodate="%d/%m/%Y"
xpathtitle='//*[@class="titre"]/a//text()[last()]'

speechlinks=[]
for attempt in range(3):
    try:
        req=request.Request(fetchlink)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        speechlinks.append(tree.xpath(xpathlink))
        tempdate=(tree.xpath(xpathdate))
        temptitle=(tree.xpath(xpathtitle))    
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime("%d-%m-%Y",tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append("Déclaration de M. Jacques Chirac" + tt)
            deadlinks.append("0")
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

flatlinks=list(itertools.chain(*speechlinks))

for link in flatlinks:
    completelink=re.sub(" |\n","",link)
    completelinks.append(completelink)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%% Fetching Hollande French speech links
fetchlink="http://www.vie-publique.fr/rechercher/recherche.php?query=%22D%C3%A9claration%20de%20M.%20Fran%C3%A7ois%20Hollande%22&skin=cdp&b=0&replies=1000&sort=document_date_publication&filter=&dateDebut=2012/05/15&dateFin=&auteur=&typeDoc=&source=&date=&filtreAuteurLibre=&typeloi=&q="
author="F. Hollande"
location="France"
lang="FR"
xpathlink='//*[@class="titre"]/a/@href'
xpathdate='//*[@class="date"]/text()'
strtodate="%d/%m/%Y"
xpathtitle='//*[@class="titre"]/a//text()[last()]'

speechlinks=[]
for attempt in range(3):
    try:
        req=request.Request(fetchlink)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        speechlinks.append(tree.xpath(xpathlink))
        tempdate=(tree.xpath(xpathdate))
        temptitle=(tree.xpath(xpathtitle))    
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime("%d-%m-%Y",tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append("Déclaration de M. Francois Hollande" + tt)
            deadlinks.append("0")
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

flatlinks=list(itertools.chain(*speechlinks))

for link in flatlinks:
    completelink=re.sub(" |\n","",link)
    completelinks.append(completelink)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%% Fetching Sarkozy French speech links
fetchlink="http://www.vie-publique.fr/rechercher/recherche.php?query=%22D%C3%A9claration%20de%20M.%20Nicolas%20Sarkozy%22&date=&dateDebut=2007/05/16&dateFin=2012/05/15&skin=cdp&replies=1000&filter=&typeloi=&auteur=f/vp_auteurphysique/sarkozy%20nicolas&filtreAuteurLibre=&typeDoc=f/vp_type_discours/declaration&source=&sort=document_date_publication&q="
author="N. Sarkozy"
location="France"
lang="FR"
xpathlink='//*[@class="titre"]/a/@href'
xpathdate='//*[@class="date"]/text()'
strtodate="%d/%m/%Y"
xpathtitle='//*[@class="titre"]/a//text()[last()]'

speechlinks=[]
for attempt in range(3):
    try:
        req=request.Request(fetchlink)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        speechlinks.append(tree.xpath(xpathlink))
        tempdate=(tree.xpath(xpathdate))
        temptitle=(tree.xpath(xpathtitle))    
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime("%d-%m-%Y",tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append("Déclaration de M. Nicolas Sarkozy" + tt)
            deadlinks.append("0")
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

flatlinks=list(itertools.chain(*speechlinks))

for link in flatlinks:
    completelink=re.sub(" |\n","",link)
    completelinks.append(completelink)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%% Fetching Merkel German speech links
fetchlink="http://www.bundeskanzlerin.de/SiteGlobals/Forms/Webs/BKin/Suche/DE/Solr_aktuelles_formular.html?nn=619050&doctype=speech&gtp=619002_list%253D"
author="A. Merkel"
location="Germany"
lang="DE"
xpathmp='//*[@class="navIndex"]/li[5]/a/@title'
regexmp=".*'Seite ([0-9]+)'.*"
xpathlink='//*[@id="searchResult"]/div/ol/li/h3/a/@href'
strtodate="%Y-%m-%d"
linktodate=".*/([0-9]+-[0-9]+-[0-9]+)-.*"
xpathtitle='//*[@id="searchResult"]/div/ol/li/h3/a/text()'
linkbase="http://www.bundeskanzlerin.de/"

for attempt in range(3):
    try:
        req=request.Request(fetchlink)
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
flatlinks=[]
for number in numbers:
    for attempt in range(3):
        try:
            req=request.Request(fetchlink + str(number+1))
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            templinks=tree.xpath(xpathlink)
            # Removing ;jsessionid="" from links, because those will be invalid when used later for scraping. Regex found online.    
            for templink in templinks:
                link=re.sub(";jsessionid=.*?(?=\\?|$)", "",templink)
                flatlinks.append(link)
                try:            
                    tmpdt=time.strptime(re.match(linktodate,link).group(1), strtodate)
                    deadlinks.append("0")
                except AttributeError:
                    tmpdt=time.strptime("2099-01-01", strtodate)
                    print("Date not available")
                    deadlinks.append("Date not available")
                except ValueError:
                    tmpdt=time.strptime("2099-01-01", strtodate)
                    print("Date not available")
                    deadlinks.append("Date not available")
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
            temptitle=(tree.xpath(xpathtitle))    
            for tt in temptitle:    
                title.append(tt)
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

## Adding url prefix to href tags to make them usable
for link in flatlinks:
    completelink=linkbase + link
    completelinks.append(completelink)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%% Fetching Sobotka CZ speech links
fetchlink="http://www.vlada.cz/scripts/detail.php?pgid=1013&conn=10155&pg="
author="B. Sobotka"
location="Czech Republic"
lang="CZ"
xpathmp='//*[@class="pager offset-before-double"]/p/text()'
regexmp=".*xa0([0-9]+).*"
xpathlink='//*[@class="record"]/h2/a/@href'
xpathdate='//*[@class="info"]/text()'
strtodate="%d. %m. %Y"
xpathtitle='//*[@class="record"]/h2/a/text()'
linkbase="http://www.vlada.cz"
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

try:
    maxno=math.ceil(int(re.match(regexmp,maxpage).group(1))/10)
except AttributeError:
    maxno=1
    print("Only 1 result page found/Error occured ("+ author + lang +")")
numbers=list(range(0,int(maxno)))

speechlinks=[]
for number in numbers:
    for attempt in range(5):
        try:
            req=request.Request(fetchlink + str(number+1))
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            speechlinks.append(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt in zip(tempdate,temptitle):    
                tmpdt=time.strptime(dt, strtodate)
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                deadlinks.append("0")
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

flatlinks=list(itertools.chain(*speechlinks))
## Adding url prefix to href tags to make them usable
for link in flatlinks:
    completelink=linkbase + link
    completelinks.append(completelink)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%% Fetching Sobotka EN speech links
fetchlink="http://www.vlada.cz/scripts/detail.php?pgid=1016&conn=10175&pg="
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

try:
    maxno=math.ceil(int(re.match(regexmp,maxpage).group(1))/10)
except AttributeError:
    maxno=1
    print("Only 1 result page found/Error occured ("+ author + lang +")")
numbers=list(range(0,int(maxno)))

speechlinks=[]
for number in numbers:
    for attempt in range(5):
        try:
            req=request.Request(fetchlink + str(number+1))
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            speechlinks.append(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt in zip(tempdate,temptitle):    
                tmpdt=time.strptime(dt, strtodate)
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                deadlinks.append("0")
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

flatlinks=list(itertools.chain(*speechlinks))
## Adding url prefix to href tags to make them usable
for link in flatlinks:
    completelink=linkbase + link
    completelinks.append(completelink)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%% Fetching Wayback CZ speech links
fetchlink="https://web.archive.org/web/20120628035120/http://vlada.cz/scripts/detail.php?pgid=338&conn=2035&pg="
author1="P. Nečas"
switch1=time.strptime("13/07/2010","%d/%m/%Y")
author2="J. Fischer"
switch2=time.strptime("08/05/2009","%d/%m/%Y")
author3="M. Topolánek"
location="Czech Republic"
lang="CZ"
xpathlink='//*[@class="record"]/h2/a/@href'
xpathdate='//*[@class="info"]/text()'
strtodate="%d. %m. %Y"
xpathtitle='//*[@class="record"]/h2/a/text()'
linkbase="https://web.archive.org"
numbers=list(range(1,8))

speechlinks=[]
for number in numbers:
    for attempt in range(3):
        try:
            req=request.Request(fetchlink + str(number))
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            speechlinks.append(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt in zip(tempdate,temptitle):    
                tmpdt=time.strptime(dt, strtodate)
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                if tmpdt < switch2:                  
                    speaker.append(author3)
                elif tmpdt < switch1:
                    speaker.append(author2)
                else:
                    speaker.append(author1)
                country.append(location)
                language.append(lang)
                title.append(tt)
                deadlinks.append("0")
            time.sleep(randint(1,5))
        except request.HTTPError:
            print("Whoops, that went wrong, retrying page "+str(number)+" for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number) + author1 + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink + str(number))
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page "+str(number)+" for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number) + author1 + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink + str(number))
            time.sleep(10)
        else:
            break

flatlinks=list(itertools.chain(*speechlinks))
## Adding url prefix to href tags to make them usable
for link in flatlinks:
    completelink=linkbase + link
    completelinks.append(completelink)
print("Finished fetching " + fetchlink + " " + author1 + " " + lang + " speech links")
#%% Fetching Tsipras EN speech links
fetchlink="http://www.primeminister.gov.gr/english/category/news/speeches/"
author1="A. Tsipras"
switch1=time.strptime("26/01/2015","%d/%m/%Y")
author2="A. Samaras"
switch2=time.strptime("20/06/2012","%d/%m/%Y")
author3="L. Papademos"
switch3=time.strptime("11/11/2011","%d/%m/%Y")
author4="G.A. Papandreou"
location="Greece"
lang="EN"
xpathmp='//*[@class="last"]/@href'
regexmp=".*http://www.primeminister.gov.gr/english/category/news/speeches/page/([0-9]+)/.*"
xpathlink='//*[@class="archive"]/div/h3/a/@href'
xpathdate='//*[@class="archive"]/div/h3/a/@href'
strtodate="%Y/%m/%d"
linktodate=".*/([0-9]+/[0-9]+/[0-9]+)/.*"
xpathtitle='//*[@class="archive"]/div/h3/a/text()'
for attempt in range(3):
    try:
        req=request.Request(fetchlink)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        maxpage=str(tree.xpath(xpathmp))
    except request.HTTPError:
        print("Whoops, that went wrong, retrying first page for "+author4+ " "+ lang)
        if attempt == 2:
            print("Fetching first page " + author4 + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except request.URLError:
        print("Whoops, that went wrong, retrying first page for "+author4+ " "+ lang)
        if attempt == 2:
            print("Fetching first page " + author4 + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    else:
        break

try:
    maxno=re.match(regexmp,maxpage).group(1)
except AttributeError:
    maxno=1
    print("Only 1 result page found/Error occured ("+ author1 + lang +")")
numbers=list(range(0,int(maxno)))

speechlinks=[]
for number in numbers:
    for attempt in range(3):
        try:
            req=request.Request(fetchlink + "page/"+ str(number+1) + "/")
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            speechlinks.append(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt in zip(tempdate,temptitle):    
                try:            
                    tmpdt=time.strptime(re.match(linktodate,dt).group(1), strtodate)
                    deadlinks.append("0")
                except AttributeError:
                    tmpdt=time.strptime("2099/01/01", strtodate)
                    print("Date not available")
                    deadlinks.append("Date not available")
                except ValueError:
                    tmpdt=time.strptime("2099/01/01", strtodate)
                    print("Date not available")
                    deadlinks.append("Date not available")
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                if tmpdt < switch3:                  
                    speaker.append(author4)
                elif tmpdt < switch2:
                    speaker.append(author3)
                elif tmpdt < switch1:
                    speaker.append(author2)
                else:
                    speaker.append(author1)
                country.append(location)
                language.append(lang)
                title.append(tt)
            time.sleep(randint(1,5))
        except request.HTTPError:
            print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author4+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number+1) + author4 + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink + str(number+1))
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author4+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number+1) + author4 + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink + str(number+1))
            time.sleep(10)
        else:
            break

flatlinks=list(itertools.chain(*speechlinks))
for link in flatlinks:
    completelinks.append(link)

print("Finished fetching " + fetchlink + " " + author1 + " " + lang + " speech links")
#%% Fetching Tsipras GR speech links
fetchlink="http://www.primeminister.gov.gr/category/news/omilia/"
author1="A. Samaras"
author2="A. Tsipras"
dateswitch=time.strptime("26/01/2015","%d/%m/%Y")
location="Greece"
lang="GR"
xpathmp='//*[@id="page_bar"]/div/a[12]/text()'
regexmp=".*'([0-9]+)'.*"
xpathlink='//*[@class="archiveitem"]/h3/a/@href'
xpathdate='//*[@class="archiveitem"]/h3/a/@href'
strtodate="%Y/%m/%d"
linktodate=".*/([0-9]+/[0-9]+/[0-9]+)/.*"
xpathtitle='//*[@class="archiveitem"]/h3/a/text()'
for attempt in range(3):
    try:
        req=request.Request(fetchlink)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        maxpage=str(tree.xpath(xpathmp))
    except request.HTTPError:
        print("Whoops, that went wrong, retrying first page for "+author1+ " "+ lang)
        if attempt == 2:
            print("Fetching first page " + author1 + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except request.URLError:
        print("Whoops, that went wrong, retrying first page for "+author1+ " "+ lang)
        if attempt == 2:
            print("Fetching first page " + author1 + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    else:
        break

try:
    maxno=re.match(regexmp,maxpage).group(1)
except AttributeError:
    maxno=1
    print("Only 1 result page found/Error occured ("+ author1 + lang +")")
numbers=list(range(0,int(maxno)))

speechlinks=[]
for number in numbers:
    for attempt in range(3):
        try:
            req=request.Request(fetchlink + "page/"+ str(number+1) + "/")
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            speechlinks.append(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt in zip(tempdate,temptitle):    
                try:            
                    tmpdt=time.strptime(re.match(linktodate,dt).group(1), strtodate)
                    deadlinks.append("0")
                except AttributeError:
                    tmpdt=time.strptime("2099/01/01", strtodate)
                    print("Date not available")
                    deadlinks.append("Date not available")
                except ValueError:
                    tmpdt=time.strptime("2099/01/01", strtodate)
                    print("Date not available")
                    deadlinks.append("Date not available")
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                if tmpdt < dateswitch:                  
                    speaker.append(author1)
                else:
                    speaker.append(author2)
                country.append(location)
                language.append(lang)
                title.append(tt)
            time.sleep(randint(1,5))
        except request.HTTPError:
            print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author1+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number+1) + author1 + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink + str(number+1))
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author1+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number+1) + author1 + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink + str(number+1))
            time.sleep(10)
        else:
            break

flatlinks=list(itertools.chain(*speechlinks))
for link in flatlinks:
    completelinks.append(link)

print("Finished fetching " + fetchlink + " " + author1 + " " + lang + " speech links")
#%% Fetching Spain EN speech links
fetchlink="http://www.lamoncloa.gob.es/lang/en/presidente/intervenciones/Paginas/index.aspx?mts="
author1="J.L.R. Zapatero"
author2="M. Rajoy"
dateswitch=time.strptime("20/12/2011","%d/%m/%Y")
location="Spain"
lang="EN"
xpathmp='//*[@id="SelectorUltimaPagina"]/a/@href'
xpathlink='//*[@class="intervencionesSumarioDerecha"]/p/a/@href'
xpathdate='//*[@class="sumarioFecha"]/text()'
strtodate="%d/%m/%Y"
xpathtitle='//*[@class="intervencionesSumarioDerecha"]/p/a/text()'
linkbase="http://www.lamoncloa.gob.es"

# Generating yearmonth url postfixes for scraping results
speechlinks=[]
num=list(range(1,13)) 
years=list(range(2007,2016))
numbers=[]
for year in years:
    for n in num:
        no=str(year)+str(format(n,'02'))
        numbers.append(no)

for attempt in range(3):
    try:
    # Fetching maximum number of pages
        for number in numbers:
            req=request.Request(fetchlink + str(number))
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            maxpage=str(tree.xpath(xpathmp))
            try:
                maxno=re.match(".*?mts="+ str(number)+"&p=([0-9]).*",maxpage).group(1)
            except AttributeError:
                maxno=1
            pageno=list(range(0,int(maxno)))
            #Fetching actual links    
            for page in pageno:
                for attempt2 in range(3):
                    try:
                        req=request.Request(fetchlink + str(number) + "&p=" + str(page+1))
                        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
                        speechlinks.append(tree.xpath(xpathlink))
                        tempdate=(tree.xpath(xpathdate))
                        temptitle=(tree.xpath(xpathtitle))    
                        for dt,tt in zip(tempdate,temptitle):    
                            tmpdt=time.strptime(dt, strtodate)
                            date.append(time.strftime("%d-%m-%Y",tmpdt))
                            if tmpdt < dateswitch:                  
                                speaker.append(author1)
                            else:
                                speaker.append(author2)
                            country.append(location)
                            language.append(lang)
                            title.append(tt)
                            deadlinks.append("0")
                        time.sleep(randint(1,5))
                    except request.HTTPError:
                        print("Whoops, that went wrong, retrying page "+str(number) + "&p=" + str(page+1)+" for "+author1+ " "+ lang)
                        if attempt2 == 2:
                            print("Fetching result page " + str(number) + "&p=" + str(page+1) + author1 + lang + " failed due to HTTPError")
                            deadlinks.append(fetchlink +str(number) + "&p=" + str(page+1))
                        time.sleep(10)
                    except request.URLError:
                        print("Whoops, that went wrong, retrying page "+str(number) + "&p=" + str(page+1)+" for "+author1+ " "+ lang)
                        if attempt2 == 2:
                            print("Fetching result page " +str(number) + "&p=" + str(page+1) + author1 + lang + " failed due to HTTPError")
                            deadlinks.append(fetchlink +str(number) + "&p=" + str(page+1))
                        time.sleep(10)
                    else:
                        break
    
    except request.HTTPError:
        print("Whoops, that went wrong, retrying first page for "+author1+ " "+ lang)
        if attempt == 2:
            print("Fetching first page " + author1 + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except request.URLError:
        print("Whoops, that went wrong, retrying first page for "+author1+ " "+ lang)
        if attempt == 2:
            print("Fetching first page " + author1 + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    else:
        break
flatlinks=list(itertools.chain(*speechlinks))
## Adding url prefix to href tags to make them usable
for link in flatlinks:
    completelink=linkbase + link
    completelinks.append(completelink)
print("Finished fetching " + fetchlink + " " + author1 + " " + lang + " speech links")
#%% Fetching Spain ES speech links
fetchlink="http://www.lamoncloa.gob.es/presidente/intervenciones/Paginas/index.aspx?mts="
author1="J.L.R. Zapatero"
author2="M. Rajoy"
dateswitch=time.strptime("20/12/2011","%d/%m/%Y")
location="Spain"
lang="ES"
xpathmp='//*[@id="SelectorUltimaPagina"]/a/@href'
xpathlink='//*[@class="intervencionesSumarioDerecha"]/p/a/@href'
xpathdate='//*[@class="sumarioFecha"]/text()'
strtodate="%d/%m/%Y"
xpathtitle='//*[@class="intervencionesSumarioDerecha"]/p/a/text()'
linkbase="http://www.lamoncloa.gob.es"

# Generating yearmonth url postfixes for scraping results
speechlinks=[]
num=list(range(1,13)) 
years=list(range(2007,2016))
numbers=[]
for year in years:
    for n in num:
        no=str(year)+str(format(n,'02'))
        numbers.append(no)

for attempt in range(3):
    try:
    # Fetching maximum number of pages
        for number in numbers:
            req=request.Request(fetchlink + str(number))
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            maxpage=str(tree.xpath(xpathmp))
            try:
                maxno=re.match(".*?mts="+ str(number)+"&p=([0-9]).*",maxpage).group(1)
            except AttributeError:
                maxno=1
            pageno=list(range(0,int(maxno)))
            #Fetching actual links    
            for page in pageno:
                for attempt2 in range(3):
                    try:
                        req=request.Request(fetchlink + str(number) + "&p=" + str(page+1))
                        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
                        speechlinks.append(tree.xpath(xpathlink))
                        tempdate=(tree.xpath(xpathdate))
                        temptitle=(tree.xpath(xpathtitle))    
                        for dt,tt in zip(tempdate,temptitle):    
                            tmpdt=time.strptime(dt, strtodate)
                            date.append(time.strftime("%d-%m-%Y",tmpdt))
                            if tmpdt < dateswitch:                  
                                speaker.append(author1)
                            else:
                                speaker.append(author2)
                            country.append(location)
                            language.append(lang)
                            title.append(tt)
                            deadlinks.append("0")
                        time.sleep(randint(1,5))
                    except request.HTTPError:
                        print("Whoops, that went wrong, retrying page "+str(number) + "&p=" + str(page+1)+" for "+author1+ " "+ lang)
                        if attempt2 == 2:
                            print("Fetching result page " + str(number) + "&p=" + str(page+1) + author1 + lang + " failed due to HTTPError")
                            deadlinks.append(fetchlink +str(number) + "&p=" + str(page+1))
                        time.sleep(10)
                    except request.URLError:
                        print("Whoops, that went wrong, retrying page "+str(number) + "&p=" + str(page+1)+" for "+author1+ " "+ lang)
                        if attempt2 == 2:
                            print("Fetching result page " +str(number) + "&p=" + str(page+1) + author1 + lang + " failed due to HTTPError")
                            deadlinks.append(fetchlink +str(number) + "&p=" + str(page+1))
                        time.sleep(10)
                    else:
                        break
    
    except request.HTTPError:
        print("Whoops, that went wrong, retrying first page for "+author1+ " "+ lang)
        if attempt == 2:
            print("Fetching first page " + author1 + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    except request.URLError:
        print("Whoops, that went wrong, retrying first page for "+author1+ " "+ lang)
        if attempt == 2:
            print("Fetching first page " + author1 + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
    else:
        break
flatlinks=list(itertools.chain(*speechlinks))
## Adding url prefix to href tags to make them usable
for link in flatlinks:
    completelink=linkbase + link
    completelinks.append(completelink)
print("Finished fetching " + fetchlink + " " + author1 + " " + lang + " speech links")
    #%% Fetching Tsipras GR speech links
fetchlink="https://web.archive.org/web/20121015121813/http://www.primeminister.gov.gr/category/news/omilia/page/"
author1="A. Tsipras"
switch1=time.strptime("26/01/2015","%d/%m/%Y")
author2="A.Samaras"
switch2=time.strptime("20/06/2012","%d/%m/%Y")
author3="L. Papademos"
switch3=time.strptime("11/11/2011","%d/%m/%Y")
author4="G.A. Papandreou"
location="Greece"
lang="GR"
xpathmp='//*[@id="page_bar"]/div/a[12]/text()'
regexmp=".*'([0-9]+)'.*"
xpathlink='//*[@class="archiveitem"]/h3/a/@href'
xpathdate='//*[@class="archiveitem"]/h3/a/@href'
strtodate="%Y/%m/%d"
linktodate=".*/([0-9]+/[0-9]+/[0-9]+)/.*"
xpathtitle='//*[@class="archiveitem"]/h3/a/text()'
linkbase="https://web.archive.org"
# Hardcoded numbers list, due to static pages of wayback machine (past snapshots don't change)
numbers=list(range(2,8))
speechlinks=[]
for number in numbers:
    for attempt in range(3):
        try:
            req=request.Request(fetchlink + str(number))
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            speechlinks.append(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt in zip(tempdate,temptitle):    
                try:            
                    tmpdt=time.strptime(re.match(linktodate,dt).group(1), strtodate)
                    deadlinks.append("0")
                except AttributeError:
                    tmpdt=time.strptime("2099/01/01", strtodate)
                    print("Date not available")
                    deadlinks.append("Date not available")
                except ValueError:
                    tmpdt=time.strptime("2099/01/01", strtodate)
                    print("Date not available")
                    deadlinks.append("Date not available")
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                if tmpdt < switch3:                  
                    speaker.append(author4)
                elif tmpdt < switch2:
                    speaker.append(author3)
                elif tmpdt < switch1:
                    speaker.append(author2)
                else:
                    speaker.append(author1)
                country.append(location)
                language.append(lang)
                title.append(tt)
            time.sleep(randint(1,5))
        except request.HTTPError:
            print("Whoops, that went wrong, retrying page "+str(number)+" for "+author4+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number) + author4 + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink + str(number))
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page "+str(number)+" for "+author4+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number) + author4 + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink + str(number))
            time.sleep(10)
        else:
            break
#Fetching part 2, from June 2011 and before
fetchlink="https://web.archive.org/web/20110606112636/http://www.primeminister.gov.gr/category/news/omilia/page/"
numbers=list(range(2,21))
# Hardcoded downloading of first page, as this has a different URL
for attempt in range(3):
    try:
        req=request.Request("https://web.archive.org/web/20110606112636/http://www.primeminister.gov.gr/category/news/omilia/")
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        speechlinks.append(tree.xpath(xpathlink))
        tempdate=(tree.xpath(xpathdate))
        temptitle=(tree.xpath(xpathtitle))    
        for dt,tt in zip(tempdate,temptitle):    
            try:            
                tmpdt=time.strptime(re.match(linktodate,dt).group(1), strtodate)
                deadlinks.append("0")
            except AttributeError:
                tmpdt=time.strptime("2099/01/01", strtodate)
                print("Date not available")
                deadlinks.append("Date not available")
            except ValueError:
                tmpdt=time.strptime("2099/01/01", strtodate)
                print("Date not available")
                deadlinks.append("Date not available")
            date.append(time.strftime("%d-%m-%Y",tmpdt))
            if tmpdt < switch3:                  
                speaker.append(author4)
            elif tmpdt < switch2:
                speaker.append(author3)
            elif tmpdt < switch1:
                speaker.append(author2)
            else:
                speaker.append(author1)
            country.append(location)
            language.append(lang)
            title.append(tt)
        time.sleep(randint(1,5))
    except request.HTTPError:
        print("Whoops, that went wrong, retrying page for "+author4+ " "+ lang)
        if attempt == 2:
            print("Fetching result page " + author4 + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
        time.sleep(10)
    except request.URLError:
        print("Whoops, that went wrong, retrying page for "+author4+ " "+ lang)
        if attempt == 2:
            print("Fetching result page "  + author4 + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
        time.sleep(10)
    else:
        break

for number in numbers:
    for attempt in range(3):
        try:
            req=request.Request(fetchlink + str(number))
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            speechlinks.append(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt in zip(tempdate,temptitle):    
                try:            
                    tmpdt=time.strptime(re.match(linktodate,dt).group(1), strtodate)
                    deadlinks.append("0")
                except AttributeError:
                    tmpdt=time.strptime("2099/01/01", strtodate)
                    print("Date not available")
                    deadlinks.append("Date not available")
                except ValueError:
                    tmpdt=time.strptime("2099/01/01", strtodate)
                    print("Date not available")
                    deadlinks.append("Date not available")
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                if tmpdt < switch3:                  
                    speaker.append(author4)
                elif tmpdt < switch2:
                    speaker.append(author3)
                elif tmpdt < switch1:
                    speaker.append(author2)
                else:
                    speaker.append(author1)
                country.append(location)
                language.append(lang)
                title.append(tt)
            time.sleep(randint(1,5))
        except request.HTTPError:
            print("Whoops, that went wrong, retrying page "+str(number)+" for "+author4+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number) + author4 + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink + str(number))
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page "+str(number)+" for "+author4+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number) + author4 + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink + str(number))
            time.sleep(10)
        else:
            break

flatlinks=list(itertools.chain(*speechlinks))
for link in flatlinks:
    completelink=linkbase + link
    completelinks.append(completelink)
print("Finished fetching " + fetchlink + " " + author4 + " " + lang + " speech links")
#%% Fetching Brown and Blair speech links from UK Archive
fetchlink="http://webarchive.nationalarchives.gov.uk/20100511073116/http://www.number10.gov.uk/news/speeches-and-transcripts"
author2="G. Brown"
author1="T. Blair"
location="Great Britain"
lang="EN"
xpathlink='//*[@class="post_latestnews rightfloat"]//h3/a/@href'
xpathdate='//*[@class="timestamp"]/text()'
strtodate="%A %d %B %Y"
dateswitch=time.strptime("27/06/2007","%d/%m/%Y")
xpathtitle='//*[@class="post_latestnews rightfloat"]//h3/a/@title'
#linkbase=""
# Scraping 2010 back till March 2009
numbers=range(2,21)
speechlinks=[]
for attempt in range(3):
    try:
        req=request.Request(fetchlink)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        speechlinks.append(tree.xpath(xpathlink))
        tempdate=(tree.xpath(xpathdate))
        tempdate = [x.strip() for x in tempdate]
        temptitle=(tree.xpath(xpathtitle))  
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime("%d-%m-%Y",tmpdt))
            if tmpdt < dateswitch:                  
                speaker.append(author1)
            else:
                speaker.append(author2)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
    except request.HTTPError:
        print("Whoops, that went wrong, retrying page for "+author1+ " "+ lang)
        if attempt == 2:
            print("Fetching result page " + author1 + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
        time.sleep(10)
    except request.URLError:
        print("Whoops, that went wrong, retrying page for "+author1+ " "+ lang)
        if attempt == 2:
            print("Fetching result page " + author1 + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
        time.sleep(10)
    else:
        break

for number in numbers:
    for attempt in range(3):
        try:
            req=request.Request(fetchlink + '/page/' + str(number))
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            speechlinks.append(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            tempdate = [x.strip() for x in tempdate]
            temptitle=(tree.xpath(xpathtitle))  
            for dt,tt in zip(tempdate,temptitle):    
                tmpdt=time.strptime(dt, strtodate)
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                if tmpdt < dateswitch:                  
                    speaker.append(author1)
                else:
                    speaker.append(author2)
                country.append(location)
                language.append(lang)
                title.append(tt)
                deadlinks.append("0")
            time.sleep(randint(1,5))
        except request.HTTPError:
            print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author1+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number+1) + author1 + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink + str(number+1))
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author1+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number+1) + author1 + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink + str(number+1))
            time.sleep(10)
        else:
            break
# Fetching links from 2007 until March 2009
fetchlink="http://webarchive.nationalarchives.gov.uk/20090330121547/http://www.number10.gov.uk/topics/news/speeches-and-transcripts"
numbers=range(2,19)
for attempt in range(3):
    try:
        req=request.Request(fetchlink)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        speechlinks.append(tree.xpath(xpathlink))
        tempdate=(tree.xpath(xpathdate))
        tempdate = [x.strip() for x in tempdate]
        temptitle=(tree.xpath(xpathtitle))  
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime("%d-%m-%Y",tmpdt))
            if tmpdt < dateswitch:                  
                speaker.append(author1)
            else:
                speaker.append(author2)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
    except request.HTTPError:
        print("Whoops, that went wrong, retrying page for "+author1+ " "+ lang)
        if attempt == 2:
            print("Fetching result page " + author1 + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
        time.sleep(10)
    except request.URLError:
        print("Whoops, that went wrong, retrying page for "+author1+ " "+ lang)
        if attempt == 2:
            print("Fetching result page " + author1 + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
        time.sleep(10)
    else:
        break

for number in numbers:
    for attempt in range(3):
        try:
            req=request.Request(fetchlink + '/page/' + str(number))
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            speechlinks.append(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            tempdate = [x.strip() for x in tempdate]
            temptitle=(tree.xpath(xpathtitle))  
            for dt,tt in zip(tempdate,temptitle):    
                tmpdt=time.strptime(dt, strtodate)
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                if tmpdt < dateswitch:                  
                    speaker.append(author1)
                else:
                    speaker.append(author2)
                country.append(location)
                language.append(lang)
                title.append(tt)
                deadlinks.append("0")
            time.sleep(randint(1,5))
        except request.HTTPError:
            print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author1+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number+1) + author1 + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink + str(number+1))
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page "+str(number+1)+" for "+author1+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number+1) + author1 + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink + str(number+1))
            time.sleep(10)
        else:
            break

flatlinks=list(itertools.chain(*speechlinks))
# This cannot be done with the current script, as filtering links would mean that the final links are no longer aligned with other info, such as date and author
# For now, all links are scraped, and need to be filtered later
for link in flatlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author1 + " " + lang + " speech links")
#%% Fetching IMF EN speech links
fetchlink="http://www.imf.org/external/news/default.aspx?gType=News&DType=Speeches&selCountry=Select+Country&selSpeaker=Select+Speaker&selMonth=01&selDay=01&selYear=2007&selMonth1=Month&selDay1=Day&selYear1=Year&sBy=date%20desc&cp="
author="IMF"
location="International Monetary Fund"
lang="EN"
xpathmp='//*[@class="formTableFooter boxPadding10"]/text()'
regexmp=".*Page 1 of ([0-9]+).*"
xpathlink='//*[@height="60"]/a/@href'
xpathdate='//*[@height="60"]/a/@href'
strtodate="%m%d%y"
xpathtitle='//*[@height="60"]/a/text()'
linktodate=".*/([0-9]+)[a-z]*.htm"
for attempt in range(3):
    try:
        req=request.Request(fetchlink +"1")
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

speechlinks=[]
for number in numbers:
    for attempt in range(3):
        try:
            req=request.Request(fetchlink + str(number+1))
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            speechlinks.append(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt in zip(tempdate,temptitle):    
                try:            
                    tmpdt=time.strptime(re.match(linktodate,dt).group(1), strtodate)
                    deadlinks.append("0")
                except AttributeError:
                    tmpdt=time.strptime("2099/01/01", strtodate)
                    print("Date not available")
                    deadlinks.append("Date not available")
                except ValueError:
                    tmpdt=time.strptime("2099/01/01", strtodate)
                    print("Date not available")
                    deadlinks.append("Date not available")
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
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

flatlinks=list(itertools.chain(*speechlinks))
## Adding url prefix to href tags to make them usable
for link in flatlinks:
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%% Fetching European Commission EN speech links
fetchlink="http://europa.eu/rapid/search-result.htm?dateRange=period&fromDate=01%2F01%2F2007&type=SPEECH&size=100&locale=EN&page=1"
xmlfeed="http://europa.eu/rapid/search-result.htm?dateRange=period&fromDate=01%2F01%2F2007&type=SPEECH&size=100&locale=EN&format=XML&page="
author="European Commission"
location="European Commission"
lang="EN"
xpathmp='//*[@title="Last page"]/@href'
regexmp=".*&page=([0-9]+).*"
xpathlink='//language[code="EN"]/url/text()'
xpathdate='//PressRelease[contains(language/code,"EN")]/date/text()'
strtodate="%a, %d %b %Y %H:%M:%S %z"
xpathtitle='//language[code="EN"]/title/text()'
for attempt in range(3):
    try:
        req=request.Request(fetchlink+"1")
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

speechlinks=[]
for number in numbers:
    for attempt in range(3):
        try:
            req=request.Request(xmlfeed + str(number+1))
            tree=etree.fromstring(request.urlopen(req).read())
            speechlinks.append(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt in zip(tempdate,temptitle):    
                tmpdt=time.strptime(dt, strtodate)
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                deadlinks.append("0")
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

flatlinks=list(itertools.chain(*speechlinks))
## Adding url prefix to href tags to make them usable
for link in flatlinks:
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%% Fetching ECB EN speech links
fetchlink="https://www.ecb.europa.eu/press/key/date/"
author="ECB"
location="European Central Bank"
lang="EN"
xpathlink='//a[@lang="en"]/@href'
xpathdate='//dd[contains(div/span/a/@lang,"en")]/preceding-sibling::*[1][self::dt]/text()' # Incredibly complex xpath to select dt tags preceding links to get correct dates
strtodate="%d/%m/%Y"
xpathtitle='//dd[contains(div/span/a/@lang,"en")]/span[@class="doc-title"]/text()'
linkbase="https://www.ecb.europa.eu"
numbers=list(range(2007,2016)) #Needs to be modified manually for additional years beyond 2015 or before 2007

speechlinks=[]
for number in numbers:
    for attempt in range(3):
        try:
            req=request.Request(fetchlink + str(number))
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            speechlinks.append(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt in zip(tempdate,temptitle):    
                tmpdt=time.strptime(dt, strtodate)
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                deadlinks.append("0")
            time.sleep(randint(1,5))
        except request.HTTPError:
            print("Whoops, that went wrong, retrying page "+str(number)+" for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink + str(number))
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page "+str(number)+" for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
                deadlinks.append(fetchlink + str(number))
            time.sleep(10)
        else:
            break

flatlinks=list(itertools.chain(*speechlinks))
## Adding url prefix to href tags to make them usable
for link in flatlinks:
    completelink=linkbase + link
    completelinks.append(completelink)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%% Fetching ALDE Guy Verhofstadt EN speech links
fetchlink="http://www.alde.eu/press/speeches-speech-guy-verhofstadt/"
author="Guy Verhofstadt"
location="European Parliament"
lang="EN"
xpathlink='//*[@class="news-list-container"]//h2/a/@href'
xpathdate= '//*[@class="news-list-date"]/h2/text()'
strtodate="%d/%m/%Y"
xpathtitle='//*[@class="news-list-container"]//h2/a/@title'
linkbase="http://www.alde.eu/"

numbers=range(0,5) #Hardcoded page numbers!
speechlinks=[]

for number in numbers:
    for attempt in range(3):
        try:
            if number == 0:
                req=request.Request(fetchlink)
            else: 
                req=request.Request(fetchlink + 'p/' + str(number))
            
            tree=html.fromstring(request.urlopen(req).read())
            speechlinks.append(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))  
            for dt,tt in zip(tempdate,temptitle):    
                tmpdt=time.strptime(dt, strtodate)
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                deadlinks.append("0")
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
flatlinks=list(itertools.chain(*speechlinks))

for link in flatlinks:
    completelink=linkbase + link
    completelinks.append(completelink)
    
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%% Fetching ECR Martin Callanan EN speech links
fetchlink="http://ecrgroup.eu/speeches/"
author="Martin Callanan"
location="European Parliament"
lang="EN"
xpathlink='//*[@class = "ecr2-list-title"]/a/@href'
xpathdate='//*[@class = "ecr2-list-publish-date"]/text()'
strtodate="%d/%B/%Y"
xpathtitle='//*[@class = "ecr2-list-title"]/a/text()'

numbers=range(0,8)
speechlinks=[]

for number in numbers:
    for attempt in range(3):
        try:
            if number == 0:
                req=request.Request(fetchlink)
            else: req=request.Request(fetchlink + 'page/' + str(number + 1))
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            speechlinks.append(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            
            regex = re.compile(r'\d{1}.*\d{4}')
            tempdate = [regex.findall(x) for x in tempdate]
            tempdate = list(itertools.chain(*tempdate))
            pattern = r'st|nd|rd|th|,'
            tempdate = [re.sub(pattern, ' ', x) for x in tempdate]
            pattern = r'- \d{2}'
            tempdate = [re.sub(pattern, ' ', x) for x in tempdate]
            pattern = re.compile(r'\s+')
            tempdate = [re.sub(pattern, '/', x) for x in tempdate]
            temptitle=(tree.xpath(xpathtitle)) 
            
            for dt,tt in zip(tempdate,temptitle):    
                tmpdt = time.strptime(dt, strtodate)
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                deadlinks.append("0")
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

flatlinks = list(itertools.chain(*speechlinks))

for link in flatlinks: 
    completelinks.append(link)
    
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%% Fetching EP group leaders speech links, see author info for specific info
fetchlink="http://www.europarl.europa.eu/meps/en/96650/see_more.html?type=CRE&leg=7&index="
author="Lothar Bisky"
location="European Parliament"
lang="EN"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/124796/see_more.html?type=CRE&leg=8&index="
author="David Borrelli"
location="European Parliament"
lang="IT"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/4536/see_more.html?type=CRE&leg=7&index="
author="Martin Callanan"
location="European Parliament"
lang="EN"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/1934/see_more.html?type=CRE&leg=6&index="
author="Daniel Cohn-Bendit"
location="European Parliament"
lang="FR"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
limitdate=time.strptime("31/12/2006","%d/%m/%Y")
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt,tl in zip(tempdate,temptitle,templinks):    
            tmpdt=time.strptime(dt, strtodate)
            if tmpdt > limitdate:
                date.append(time.strftime(strtodate,tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                completelinks.append(tl)            
                deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/1934/see_more.html?type=CRE&leg=7&index="
author="Daniel Cohn-Bendit"
location="European Parliament"
lang="FR"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/2109/see_more.html?type=CRE&leg=6&index="
author="Brian Crowley"
location="European Parliament"
lang="EN"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
limitdate=time.strptime("31/12/2006","%d/%m/%Y")
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt,tl in zip(tempdate,temptitle,templinks):    
            tmpdt=time.strptime(dt, strtodate)
            if tmpdt > limitdate:
                date.append(time.strftime(strtodate,tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                completelinks.append(tl)            
                deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/4342/see_more.html?type=CRE&leg=6&index="
author="Joseph Daul"
location="European Parliament"
lang="FR"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
limitdate=time.strptime("31/12/2006","%d/%m/%Y")
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt,tl in zip(tempdate,temptitle,templinks):    
            tmpdt=time.strptime(dt, strtodate)
            if tmpdt > limitdate:
                date.append(time.strftime(strtodate,tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                completelinks.append(tl)            
                deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/4342/see_more.html?type=CRE&leg=7&index="
author="Joseph Daul"
location="European Parliament"
lang="FR"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/125025/see_more.html?type=CRE&leg=8&index="
author="Marcel de Graaff"
location="European Parliament"
lang="NL"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/4525/see_more.html?type=CRE&leg=6&index="
author="Nigel Farage"
location="European Parliament"
lang="EN"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
limitdate=time.strptime("31/12/2006","%d/%m/%Y")
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt,tl in zip(tempdate,temptitle,templinks):    
            tmpdt=time.strptime(dt, strtodate)
            if tmpdt > limitdate:
                date.append(time.strftime(strtodate,tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                completelinks.append(tl)            
                deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/4525/see_more.html?type=CRE&leg=7&index="
author="Nigel Farage"
location="European Parliament"
lang="EN"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/4525/see_more.html?type=CRE&leg=8&index="
author="Nigel Farage"
location="European Parliament"
lang="EN"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/4254/see_more.html?type=CRE&leg=6&index="
author="Monica Frassoni"
location="European Parliament"
lang="EN"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
limitdate=time.strptime("31/12/2006","%d/%m/%Y")
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt,tl in zip(tempdate,temptitle,templinks):    
            tmpdt=time.strptime(dt, strtodate)
            if tmpdt > limitdate:
                date.append(time.strftime(strtodate,tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                completelinks.append(tl)            
                deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/28233/see_more.html?type=CRE&leg=7&index="
author="Rebecca Harms"
location="European Parliament"
lang="DE"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/28233/see_more.html?type=CRE&leg=8&index="
author="Rebecca Harms"
location="European Parliament"
lang="DE"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/33569/see_more.html?type=CRE&leg=8&index="
author="Syed Kamall"
location="European Parliament"
lang="EN"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/23792/see_more.html?type=CRE&leg=7&index="
author="Michal Kaminski"
location="European Parliament"
lang="PO"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/96648/see_more.html?type=CRE&leg=8&index="
author="Philippe Lamberts"
location="European Parliament"
lang="FR"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/28210/see_more.html?type=CRE&leg=8&index="
author="Marine Le Pen"
location="European Parliament"
lang="FR"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/1073/see_more.html?type=CRE&leg=6&index="
author="Cristiana Muscardini"
location="European Parliament"
lang="EN"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
limitdate=time.strptime("31/12/2006","%d/%m/%Y")
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt,tl in zip(tempdate,temptitle,templinks):    
            tmpdt=time.strptime(dt, strtodate)
            if tmpdt > limitdate:
                date.append(time.strftime(strtodate,tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                completelinks.append(tl)            
                deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/4436/see_more.html?type=CRE&leg=8&index="
author="Gianni Pittella"
location="European Parliament"
lang="IT"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/1911/see_more.html?type=CRE&leg=6&index="
author="Martin Schulz"
location="European Parliament"
lang="DE"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
limitdate=time.strptime("31/12/2006","%d/%m/%Y")
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt,tl in zip(tempdate,temptitle,templinks):    
            tmpdt=time.strptime(dt, strtodate)
            if tmpdt > limitdate:
                date.append(time.strftime(strtodate,tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                completelinks.append(tl)            
                deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/1911/see_more.html?type=CRE&leg=7&index="
author="Martin Schulz"
location="European Parliament"
lang="DE"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/28119/see_more.html?type=CRE&leg=6&index="
author="Kathy Sinnott"
location="European Parliament"
lang="EN"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
limitdate=time.strptime("31/12/2006","%d/%m/%Y")
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt,tl in zip(tempdate,temptitle,templinks):    
            tmpdt=time.strptime(dt, strtodate)
            if tmpdt > limitdate:
                date.append(time.strftime(strtodate,tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                completelinks.append(tl)            
                deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/4525/see_more.html?type=CRE&leg=7&index="
author="Francesco Speroni"
location="European Parliament"
lang="IT"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/2295/see_more.html?type=CRE&leg=7&index="
author="Hannes Swoboda"
location="European Parliament"
lang="DE"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/97058/see_more.html?type=CRE&leg=7&index="
author="Guy Verhofstadt"
location="European Parliament"
lang="EN"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/97058/see_more.html?type=CRE&leg=8&index="
author="Guy Verhofstadt"
location="European Parliament"
lang="EN"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/2155/see_more.html?type=CRE&leg=6&index="
author="Graham Watson"
location="European Parliament"
lang="EN"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
limitdate=time.strptime("31/12/2006","%d/%m/%Y")
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt,tl in zip(tempdate,temptitle,templinks):    
            tmpdt=time.strptime(dt, strtodate)
            if tmpdt > limitdate:
                date.append(time.strftime(strtodate,tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                completelinks.append(tl)            
                deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/28229/see_more.html?type=CRE&leg=8&index="
author="Manfred Weber"
location="European Parliament"
lang="EN"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/1018/see_more.html?type=CRE&leg=6&index="
author="Francis Wurtz"
location="European Parliament"
lang="EN"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
limitdate=time.strptime("31/12/2006","%d/%m/%Y")
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt,tl in zip(tempdate,temptitle,templinks):    
            tmpdt=time.strptime(dt, strtodate)
            if tmpdt > limitdate:
                date.append(time.strftime(strtodate,tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                completelinks.append(tl)            
                deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/23712/see_more.html?type=CRE&leg=7&index="
author="Jan Zahradil"
location="European Parliament"
lang="EN"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/28248/see_more.html?type=CRE&leg=7&index="
author="Gabriele Zimmer"
location="European Parliament"
lang="DE"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
      
for link in speechlinks: 
    completelinks.append(link)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%
fetchlink="http://www.europarl.europa.eu/meps/en/28248/see_more.html?type=CRE&leg=8&index="
author="Gabriele Zimmer"
location="European Parliament"
lang="DE"
strtodate="%d-%m-%Y"
numbers = range(0,1000, 100)
speechlinks = []
try:
    for number in numbers:
        response = requests.get(fetchlink + str(number))
        data = response.json()
        document_list = data['documentList']
        templinks = [x['titleUrl'] for x in document_list]
        tempdate = [x['date'] for x in document_list]
        temptitle = [x['title'] for x in document_list]
        speechlinks = speechlinks + templinks
        
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime(strtodate,tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
        time.sleep(randint(1,5))
 
        if data['nextIndex'] == -1:
            break
except request.HTTPError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
except request.URLError:
    deadlinks.append(fetchlink + str(number))
    print("Fetching result page " + str(number) + author + lang + " failed due to HTTPError")
    time.sleep(randint(1,5))
for link in speechlinks: 
    completelinks.append(link)

print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%% Fetching European Council EN speech links
fetchlink="http://www.consilium.europa.eu/en/press/press-releases/?ent%5b%5d=600&ent%5b%5d=553&typ%5b%5d=265&stDt=20150929&p="
author="European Council"
location="European Council"
lang="EN"
xpathmp='//a[@title="Last"]/@href'
regexmp=".*&p=([0-9]+).*"
xpathlink='//*[@class="label-title"]/a/@href'
xpathdate='//*[@class="calendar-title-date span12"]/h2/text()'
strtodate="%d %B %Y"
xpathtitle='//*[@class="label-title"]/a/span/text()'
linkbase="http://www.consilium.europa.eu/en"
author1="D. Tusk"
switch1=time.strptime("01/12/2014","%d/%m/%Y")
author2="H. van Rompuy"
#xpathtext='//*[@id="contentPressRelease"]/descendant::*/text()'

for attempt in range(3):
    try:
        req=request.Request(fetchlink+"1")
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

speechlinks=[]
for number in numbers:
    for attempt in range(3):
        try:
            req=request.Request(fetchlink + str(number+1))
            tree=html.fromstring(request.urlopen(req).read())
            speechlinks.append(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            templink=(tree.xpath(xpathlink))        
            for dt,tt,tl in zip(tempdate,temptitle,templink):    
                tmpdt=time.strptime(dt, strtodate)
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                if tmpdt < switch1:                  
                    speaker.append(author2)
                else:
                    speaker.append(author1)
                country.append(location)
                language.append(lang)
                title.append(tt)
                completelinks.append(linkbase+tl)
                deadlinks.append("0")
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
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")

#%% Wayback Italy
## Prodi
fetchlink="http://www.sitiarcheologici.palazzochigi.it/www.governo.it/maggio%202008/www.governo.it/Presidente/Interventi/index2bff.html?a=&m=&pg=1"
author="R. Prodi"
location="Italy"
lang="IT"
xpathlink='//*[@class="tdasinistra"]/a/@href'
xpathdate='//td[@class="tdasinistra"]/text()'
strtodate="%d/%m/%Y"
xpathtitle='//*[@class="tdasinistra"]/a/text()'
linkbase="http://www.sitiarcheologici.palazzochigi.it/www.governo.it/maggio%202008/www.governo.it/Presidente/Interventi/"
speechlinks=[]
limitdate=time.strptime("31/12/2006","%d/%m/%Y")
xpathpages='//*[@id="pagine"]/a/@href'
resultpages=[]
for attempt in range(3):
    try:
        req=request.Request(fetchlink)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        tempresults=(tree.xpath(xpathpages))
        resultpages.append(fetchlink)    
        for result in tempresults:
           resultpages.append(linkbase+result) 
    except request.HTTPError:
        deadlinks.append(fetchlink)
        print("Fetching result page index " + author + lang + " failed due to HTTPError")
        time.sleep(randint(1,5))
    except request.URLError:
        deadlinks.append(fetchlink)
        print("Fetching result page index " + author + lang + " failed due to HTTPError")
        time.sleep(randint(1,5))
for resultlink in resultpages[0:len(resultpages)-1]:
    for attempt in range(3):
        try:
            req=request.Request(resultlink)
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            templinks=(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt,tl in zip(tempdate,temptitle,templinks):    
                tmpdt=time.strptime(dt, strtodate)
                if tmpdt > limitdate:
                    date.append(time.strftime("%d-%m-%Y",tmpdt))
                    speaker.append(author)
                    country.append(location)
                    language.append(lang)
                    title.append(tt)
                    completelinks.append(linkbase+re.sub("dettaglio","testo_int",tl))            
                    deadlinks.append("0")
            time.sleep(randint(1,5))
        except request.HTTPError:
            print("Whoops, that went wrong, retrying page for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page" + author + lang + " failed due to HTTPError")
                deadlinks.append(resultlink)
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + author + lang + " failed due to HTTPError")
                deadlinks.append(resultlink)
            time.sleep(10)
        else:
            break
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")

#%% Berlusconi 

fetchlink="http://www.sitiarcheologici.palazzochigi.it/www.governo.it/novembre%202011/www.governo.it/Presidente/Interventi/index2bff.html?a=&m=&pg=1"
author="S. Berlusconi"
location="Italy"
lang="IT"
xpathlink='//*[@class="tdASinistra"]/a/@href'
xpathdate='//td[@class="tdASinistra"]/text()'
strtodate="%d/%m/%Y"
xpathtitle='//*[@class="tdASinistra"]/a/text()'
linkbase="http://www.sitiarcheologici.palazzochigi.it/www.governo.it/novembre%202011/www.governo.it/Presidente/Interventi/"

speechlinks=[]
xpathpages='//*[@id="pagine"]/a/@href'
resultpages=[]
for attempt in range(3):
    try:
        req=request.Request(fetchlink)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        tempresults=(tree.xpath(xpathpages))
        resultpages.append(fetchlink)    
        for result in tempresults:
           resultpages.append(linkbase+result) 
    except request.HTTPError:
        deadlinks.append(fetchlink)
        print("Fetching result page index " + author + lang + " failed due to HTTPError")
        time.sleep(randint(1,5))
    except request.URLError:
        deadlinks.append(fetchlink)
        print("Fetching result page index " + author + lang + " failed due to HTTPError")
        time.sleep(randint(1,5))
for resultlink in resultpages[0:len(resultpages)-1]:
    for attempt in range(3):
        try:
            req=request.Request(resultlink)
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            templinks=(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt,tl in zip(tempdate,temptitle,templinks):    
                tmpdt=time.strptime(dt, strtodate)
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                completelinks.append(linkbase+re.sub("dettaglio","testo_int",tl))            
                deadlinks.append("0")
            time.sleep(randint(1,5))
        except request.HTTPError:
            print("Whoops, that went wrong, retrying page for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page" + author + lang + " failed due to HTTPError")
                deadlinks.append(resultlink)
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + author + lang + " failed due to HTTPError")
                deadlinks.append(resultlink)
            time.sleep(10)
        else:
            break
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%% Monti

fetchlink="http://www.sitiarcheologici.palazzochigi.it/www.governo.it/aprile%202013/www.governo.it/Presidente/Interventi/index460c.html?a=&m=&pg=1&txtTesto="
author="M. Monti"
location="Italy"
lang="IT"
xpathlink='//*[@class="tdASinistra"]/a/@href'
xpathdate='//td[@class="tdASinistra"]/text()'
strtodate="%d/%m/%Y"
xpathtitle='//*[@class="tdASinistra"]/a/text()'
linkbase="http://www.sitiarcheologici.palazzochigi.it/www.governo.it/aprile%202013/www.governo.it/Presidente/Interventi/"

speechlinks=[]
xpathpages='//*[@id="pagine"]/a/@href'
resultpages=[]
for attempt in range(3):
    try:
        req=request.Request(fetchlink)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        tempresults=(tree.xpath(xpathpages))
        resultpages.append(fetchlink)    
        for result in tempresults:
           resultpages.append(linkbase+result) 
    except request.HTTPError:
        deadlinks.append(fetchlink)
        print("Fetching result page index " + author + lang + " failed due to HTTPError")
        time.sleep(randint(1,5))
    except request.URLError:
        deadlinks.append(fetchlink)
        print("Fetching result page index " + author + lang + " failed due to HTTPError")
        time.sleep(randint(1,5))
for resultlink in resultpages[0:len(resultpages)-1]:
    for attempt in range(3):
        try:
            req=request.Request(resultlink)
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            templinks=(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt,tl in zip(tempdate,temptitle,templinks):    
                tmpdt=time.strptime(dt, strtodate)
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                completelinks.append(linkbase+re.sub("dettaglio","testo_int",tl))            
                deadlinks.append("0")
            time.sleep(randint(1,5))
        except request.HTTPError:
            print("Whoops, that went wrong, retrying page for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page" + author + lang + " failed due to HTTPError")
                deadlinks.append(resultlink)
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + author + lang + " failed due to HTTPError")
                deadlinks.append(resultlink)
            time.sleep(10)
        else:
            break
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%% Letta

fetchlink="http://sitiarcheologici.palazzochigi.it/www.governo.it/febbraio%202014/www.governoletta.it/Presidente/Interventi/index460c.html?a=&m=&pg=1&txtTesto="
author="E. Letta"
location="Italy"
lang="IT"
xpathlink='//*[@class="tdASinistra"]/a/@href'
xpathdate='//td[@class="tdASinistra"]/text()'
strtodate="%d/%m/%Y"
xpathtitle='//*[@class="tdASinistra"]/a/text()'
linkbase="http://sitiarcheologici.palazzochigi.it/www.governo.it/febbraio%202014/www.governoletta.it/Presidente/Interventi/"

speechlinks=[]
xpathpages='//*[@id="pagine"]/a/@href'
resultpages=[]
for attempt in range(3):
    try:
        req=request.Request(fetchlink)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        tempresults=(tree.xpath(xpathpages))
        resultpages.append(fetchlink)    
        for result in tempresults:
           resultpages.append(linkbase+result) 
    except request.HTTPError:
        deadlinks.append(fetchlink)
        print("Fetching result page index " + author + lang + " failed due to HTTPError")
        time.sleep(randint(1,5))
    except request.URLError:
        deadlinks.append(fetchlink)
        print("Fetching result page index " + author + lang + " failed due to HTTPError")
        time.sleep(randint(1,5))
for resultlink in resultpages[0:len(resultpages)-1]:
    for attempt in range(3):
        try:
            req=request.Request(resultlink)
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            templinks=(tree.xpath(xpathlink))
            tempdate=(tree.xpath(xpathdate))
            temptitle=(tree.xpath(xpathtitle))    
            for dt,tt,tl in zip(tempdate,temptitle,templinks):    
                tmpdt=time.strptime(dt, strtodate)
                date.append(time.strftime("%d-%m-%Y",tmpdt))
                speaker.append(author)
                country.append(location)
                language.append(lang)
                title.append(tt)
                completelinks.append(linkbase+re.sub("dettaglio","testo_int",tl))            
                deadlinks.append("0")
            time.sleep(randint(1,5))
        except request.HTTPError:
            print("Whoops, that went wrong, retrying page for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page" + author + lang + " failed due to HTTPError")
                deadlinks.append(resultlink)
            time.sleep(10)
        except request.URLError:
            print("Whoops, that went wrong, retrying page for "+author+ " "+ lang)
            if attempt == 2:
                print("Fetching result page " + author + lang + " failed due to HTTPError")
                deadlinks.append(resultlink)
            time.sleep(10)
        else:
            break
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")

#%% Fetching M. Renzi IT speech links
fetchlink="https://web.archive.org/web/20150522094904/http://www.governo.it/Presidente/Interventi/index.asp"
author="M. Renzi"
location="Italy"
lang="IT"
xpathlink='//*[@class="tdASinistra"]/a/@href'
xpathdate='//td[@class="tdASinistra"]/text()'
strtodate="%d/%m/%Y"
xpathtitle='//*[@class="tdASinistra"]/a/text()'
linkbase="https://web.archive.org"

speechlinks=[]

for attempt in range(3):
    try:
        req=request.Request(fetchlink)
        tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
        speechlinks.append(tree.xpath(xpathlink))
        tempdate=(tree.xpath(xpathdate))
        temptitle=(tree.xpath(xpathtitle))    
        for dt,tt in zip(tempdate,temptitle):    
            tmpdt=time.strptime(dt, strtodate)
            date.append(time.strftime("%d-%m-%Y",tmpdt))
            speaker.append(author)
            country.append(location)
            language.append(lang)
            title.append(tt)
            deadlinks.append("0")
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
            print("Fetching result page " + author + lang + " failed due to HTTPError")
            deadlinks.append(fetchlink)
        time.sleep(10)
    else:
        break
flatlinks=list(itertools.chain(*speechlinks))
## Adding url prefix to href tags to make them usable
for link in flatlinks:
    completelink=linkbase + link
    completelinks.append(completelink)
print("Finished fetching " + fetchlink + " " + author + " " + lang + " speech links")
#%%  Saving the output
print("Printing errors/dead links")
for deadlink in deadlinks:
    if deadlink != "0":
        print(deadlink)

import datetime #for naming the output file, so that the script can be run multiple times without overwriting
import csv
cleantitle=[]
for t in title:
    cleantitle.append(re.sub("\r|\n|\t","",t.lstrip()))

output=zip(date,country,speaker,language,cleantitle,completelinks)
#raw data output, without header rows, can be used for further data processing, but is by no means a final product
dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
with open("/media/Games/Documenten/EU Engage/Final/LinksCombinedDEF"+dt+".csv",mode="w",encoding="utf-8") as fo:
    writer=csv.writer(fo)
    writer.writerows(output)

output=zip(deadlinks)
#raw data output, without header rows, can be used for further data processing, but is by no means a final product
dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
with open("/media/Games/Documenten/EU Engage/Final/LinksCombinedDeadlinks"+dt+".csv",mode="w",encoding="utf-8") as fo:
    writer=csv.writer(fo)
    writer.writerows(output)
