# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 18:05:34 2015

@author: EdV
"""

#Notes:
# 1. For the data to stay aligned properly (metadata matching actual speeches), scraping must be done in the order in which the links are listed.
# This is done by scraping the speeches in the same (website) order as when the links were scraped
from lxml import html
from urllib import request
from random import randint
import time
import re
import csv
import datetime #for naming the output file, so that the script can be run multiple times without overwriting
completelinks=[]
date=[]
speaker=[]
country=[]
language=[]
title=[]
deadlinks=[]
speeches=[]
tempspeeches=[]
emptyspeeches=[]
tmpdate=[]
tmpcountry=[]
tmpspeaker=[]
tmplanguage=[]
tmptitle=[]
tmplink=[]
tmpspeech=[]
deadlink=[]

basedir="C:/Users/gschuma1/Dropbox/Papers/Leader Speeches Project/Erik/"
#%% Importing the LinksCombined dataset
with open (basedir+"/MergedDEF.csv",encoding="utf-8") as fi: # Change to correct directory before importing
    reader=csv.reader(fi,delimiter=",")
    for row in reader:
        date.append(row[0])
        country.append(row[1])
        speaker.append(row[2])
        language.append(row[3])
        title.append(row[4])
        completelinks.append(row[5])
print("Importing done, starting scraping")

#%% Scraping Spanish speeches (http://www.lamoncloa.gob.es/lang/en/paginas/archivo/2008/31012008XXIHispAle.aspx is not a speech)
xpathspeech='//*[@class="contenidoTexto"]/descendant-or-self::*/text()'
for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):
    if l.startswith("http://www.lamoncloa.gob.es/"):
        for attempt in range(5):
            try:    
                req=request.Request(l)
                tree=html.fromstring(request.urlopen(req).read()) #.decode(encoding="utf-8",errors="ignore") 
                tmpspeech.append("<p>"+ "</p><p>".join(tree.xpath(xpathspeech))+"</p>")
                tmpdate.append(d)
                tmpcountry.append(c)
                tmpspeaker.append(s)
                tmplanguage.append(lang)
                tmptitle.append(t)
                tmplink.append(l)
                deadlink.append("0")
                time.sleep(randint(1,5))
            except request.HTTPError:
                print("Whoops, that went wrong, retrying page "+str(l))
                if attempt == 4:
                    deadlink.append(l)
                    tmpdate.append(d)
                    tmpcountry.append(c)
                    tmpspeaker.append(s)
                    tmplanguage.append(lang)
                    tmptitle.append(t)
                    tmplink.append(l)
                    tmpspeech.append("404")
                    print("Fetching speech " + str(l) + " failed due to HTTPError")
                time.sleep(10)
            except request.URLError:
                print("Whoops, that went wrong, retrying page "+str(l))
                if attempt == 4:
                    deadlink.append(l)
                    tmpdate.append(d)
                    tmpcountry.append(c)
                    tmpspeaker.append(s)
                    tmplanguage.append(lang)
                    tmptitle.append(t)
                    tmplink.append(l)
                    tmpspeech.append("404")
                    print("Fetching speech " + str(l) + " failed due to HTTPError")
                time.sleep(10)
            except ConnectionResetError:
                print("Whoops, that went wrong, retrying page "+str(l))
                if attempt == 4:
                    deadlink.append(l)
                    tmpdate.append(d)
                    tmpcountry.append(c)
                    tmpspeaker.append(s)
                    tmplanguage.append(lang)
                    tmptitle.append(t)
                    tmplink.append(l)
                    tmpspeech.append("404")
                    print("Fetching speech " + str(l) + " failed due to HTTPError")
                time.sleep(10)
            else:
                break

output=zip(tmpdate,tmpcountry,tmpspeaker,tmplanguage,tmptitle,tmplink,tmpspeech,deadlink)
dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
with open(basedir+"/Speeches"+c+dt+".csv",mode="w",encoding="utf-8") as fo:
    writer=csv.writer(fo)
    writer.writerows(output)

tmpdate=[]
tmpcountry=[]
tmpspeaker=[]
tmplanguage=[]
tmptitle=[]
tmplink=[]
tmpspeech=[]
deadlink=[]
print("Done scraping Spanish speeches")
print("Done")
