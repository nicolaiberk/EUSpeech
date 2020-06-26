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

basedir="/media/home/Temp/EUEngage"
#%% Importing the LinksCombined dataset
with open (basedir+"/MergedDEF.csv") as fi: # Change to correct directory before importing
    reader=csv.reader(fi,delimiter=",")
    for row in reader:
        date.append(row[0])
        country.append(row[1])
        speaker.append(row[2])
        language.append(row[3])
        title.append(row[4])
        completelinks.append(row[5])
print("Importing done, starting scraping")

##%% Scraping Dutch speeches
#xpathspeech='//*[@id="content"]/child::p/descendant-or-self::*/text()'
#for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):
#    if s == "J.P. Balkenende":
#        for attempt in range(5):
#            try:    
#                req=request.Request(l)
#                tree=html.fromstring(request.urlopen(req).read())
#                tmpspeech.append("<p>"+ "</p><p>".join(tree.xpath(xpathspeech))+"</p>")
#                tmpdate.append(d)
#                tmpcountry.append(c)
#                tmpspeaker.append(s)
#                tmplanguage.append(lang)
#                tmptitle.append(t)
#                tmplink.append(l)
#                deadlink.append("0")
#                time.sleep(randint(1,5))
#            except request.HTTPError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            except request.URLError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            except ConnectionResetError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            else:
#                break
#    
#    elif s == "M. Rutte":
#        for attempt in range(5):
#            try:    
#                req=request.Request(l)
#                tree=html.fromstring(request.urlopen(req).read())
#                tmpspeech.append("<p>"+ "</p><p>".join(tree.xpath(xpathspeech))+"</p>")
#                tmpdate.append(d)
#                tmpcountry.append(c)
#                tmpspeaker.append(s)
#                tmplanguage.append(lang)
#                tmptitle.append(t)
#                tmplink.append(l)
#                deadlink.append("0")
#                time.sleep(randint(1,5))
#            except request.HTTPError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            except request.URLError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            except ConnectionResetError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            else:
#                break
#
#output=zip(tmpdate,tmpcountry,tmpspeaker,tmplanguage,tmptitle,tmplink,tmpspeech,deadlink)
#dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
#with open(basedir+"/Speeches"+c+dt+".csv",mode="w",encoding="utf-8") as fo:
#    writer=csv.writer(fo)
#    writer.writerows(output)
#
#tmpdate=[]
#tmpcountry=[]
#tmpspeaker=[]
#tmplanguage=[]
#tmptitle=[]
#tmplink=[]
#tmpspeech=[]
#deadlink=[]
#print("Done scraping Dutch speeches")        
##%% Scraping UK speeches
#xpathspeech='//*[@class="govspeak"]/p/descendant-or-self::*/text()'
##Adopted:
#################
##comment Martijn:
## //*[@class="govspeak"]/p/text()
##leaves out link at the end of text that follows speech - may add up with enough speeches
#################
#for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):
#    if l.startswith("https://www.gov.uk/government/speeches"):
#        for attempt in range(5):
#            try:    
#                req=request.Request(l)
#                tree=html.fromstring(request.urlopen(req).read())
#                tmpspeech.append("<p>"+ "</p><p>".join(tree.xpath(xpathspeech))+"</p>")
#                tmpdate.append(d)
#                tmpcountry.append(c)
#                tmpspeaker.append(s)
#                tmplanguage.append(lang)
#                tmptitle.append(t)
#                tmplink.append(l)
#                deadlink.append("0")
#                time.sleep(randint(1,5))
#            except request.HTTPError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            except request.URLError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            except ConnectionResetError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            else:
#                break
#
#output=zip(tmpdate,tmpcountry,tmpspeaker,tmplanguage,tmptitle,tmplink,tmpspeech,deadlink)
#dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
#with open(basedir+"/Speeches"+c+dt+".csv",mode="w",encoding="utf-8") as fo:
#    writer=csv.writer(fo)
#    writer.writerows(output)
#
#tmpdate=[]
#tmpcountry=[]
#tmpspeaker=[]
#tmplanguage=[]
#tmptitle=[]
#tmplink=[]
#tmpspeech=[]
#deadlink=[]
#print("Done scraping UK speeches")        
##%% Scraping French speeches
#xpathspeech='//*[@class="col1"]/p/descendant-or-self::*/text()'
#for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):
#    if l.startswith("http://discours.vie-publique.fr"):
#        for attempt in range(5):
#            try:    
#                req=request.Request(l)
#                tree=html.fromstring(request.urlopen(req).read())
#                tmpspeech.append("<p>"+ "</p><p>".join(tree.xpath(xpathspeech))+"</p>")
#                tmpdate.append(d)
#                tmpcountry.append(c)
#                tmpspeaker.append(s)
#                tmplanguage.append(lang)
#                tmptitle.append(t)
#                tmplink.append(l)
#                deadlink.append("0")
#                time.sleep(randint(1,5))
#            except request.HTTPError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            except request.URLError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            except ConnectionResetError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            else:
#                break
##%%
#output=zip(tmpdate,tmpcountry,tmpspeaker,tmplanguage,tmptitle,tmplink,tmpspeech,deadlink)
#dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
#with open(basedir+"/Speeches"+c+dt+".csv",mode="w",encoding="utf-8") as fo:
#    writer=csv.writer(fo)
#    writer.writerows(output)
#
#tmpdate=[]
#tmpcountry=[]
#tmpspeaker=[]
#tmplanguage=[]
#tmptitle=[]
#tmplink=[]
#tmpspeech=[]
#deadlink=[]
#print("Done scraping French speeches")        
##%% Scraping German speeches (inludes some speeches in English)
#xpathspeech='//*[@class="basepage_pages"]/p/descendant-or-self::*/text()'
#################
##comment Martijn:
## //*[@class="basepage_pages"]/p/text()
##leaves out bold location
#################
#for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):
#    if l.startswith("http://www.bundeskanzlerin.de/"):
#        for attempt in range(5):
#            try:    
#                req=request.Request(l)
#                tree=html.fromstring(request.urlopen(req).read())
#                tmpspeech.append("<p>"+ "</p><p>".join(tree.xpath(xpathspeech))+"</p>")
#                tmpdate.append(d)
#                tmpcountry.append(c)
#                tmpspeaker.append(s)
#                tmplanguage.append(lang)
#                tmptitle.append(t)
#                tmplink.append(l)
#                deadlink.append("0")
#                time.sleep(randint(1,5))
#            except request.HTTPError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            except request.URLError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            except ConnectionResetError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            else:
#                break
#
#output=zip(tmpdate,tmpcountry,tmpspeaker,tmplanguage,tmptitle,tmplink,tmpspeech,deadlink)
#dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
#with open(basedir+"/Speeches"+c+dt+".csv",mode="w",encoding="utf-8") as fo:
#    writer=csv.writer(fo)
#    writer.writerows(output)
#
#tmpdate=[]
#tmpcountry=[]
#tmpspeaker=[]
#tmplanguage=[]
#tmptitle=[]
#tmplink=[]
#tmpspeech=[]
#deadlink=[]
#print("Done scraping German speeches")        
##%% Scraping Czech speeches (also contains statements)
#xpathspeech='//*[@class="detail"]/p/descendant-or-self::*/text()'
#################
##comment Martijn:
## //*[@class="detail"]/p/text()
##leaves out last line denoting speech giver
#################
#################
##comment Erik:
## Not necessary, speech giver can be filtered out
## by removing everything after last sentence
#################
#for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):
#    if "vlada.cz/" in l:
#        if l.startswith("http://www.vlada.cz"):
#            for attempt in range(5):
#                try:    
#                    req=request.Request(l)
#                    tree=html.fromstring(request.urlopen(req).read())
#                    tmpspeech.append("<p>"+ "</p><p>".join(tree.xpath(xpathspeech))+"</p>")
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    deadlink.append("0")
#                    time.sleep(randint(1,5))
#                except request.HTTPError:
#                    print("Whoops, that went wrong, retrying page "+str(l))
#                    if attempt == 4:
#                        deadlink.append(l)
#                        tmpdate.append(d)
#                        tmpcountry.append(c)
#                        tmpspeaker.append(s)
#                        tmplanguage.append(lang)
#                        tmptitle.append(t)
#                        tmplink.append(l)
#                        tmpspeech.append("404")
#                        print("Fetching speech " + str(l) + " failed due to HTTPError")
#                    time.sleep(10)
#                except request.URLError:
#                    print("Whoops, that went wrong, retrying page "+str(l))
#                    if attempt == 4:
#                        deadlink.append(l)
#                        tmpdate.append(d)
#                        tmpcountry.append(c)
#                        tmpspeaker.append(s)
#                        tmplanguage.append(lang)
#                        tmptitle.append(t)
#                        tmplink.append(l)
#                        tmpspeech.append("404")
#                        print("Fetching speech " + str(l) + " failed due to HTTPError")
#                    time.sleep(10)
#                except ConnectionResetError:
#                    print("Whoops, that went wrong, retrying page "+str(l))
#                    if attempt == 4:
#                        deadlink.append(l)
#                        tmpdate.append(d)
#                        tmpcountry.append(c)
#                        tmpspeaker.append(s)
#                        tmplanguage.append(lang)
#                        tmptitle.append(t)
#                        tmplink.append(l)
#                        tmpspeech.append("404")
#                        print("Fetching speech " + str(l) + " failed due to HTTPError")
#                    time.sleep(10)
#                else:
#                    break
#        elif l.startswith("https://web.archive.org/web"):
#            for attempt in range(5):
#                try:    
#                    req=request.Request(re.sub("https://web.archive.org/web/[0-9]+?/http://","http://",l))
#                    tree=html.fromstring(request.urlopen(req).read())
#                    tmpspeech.append("<p>"+ "</p><p>".join(tree.xpath(xpathspeech))+"</p>")
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    deadlink.append("0")
#                    time.sleep(randint(1,5))
#                except request.HTTPError:
#                    print("Whoops, that went wrong, retrying page "+str(l))
#                    if attempt == 4:
#                        deadlink.append(l)
#                        tmpdate.append(d)
#                        tmpcountry.append(c)
#                        tmpspeaker.append(s)
#                        tmplanguage.append(lang)
#                        tmptitle.append(t)
#                        tmplink.append(l)
#                        tmpspeech.append("404")
#                        print("Fetching speech " + str(l) + " failed due to HTTPError")
#                    time.sleep(10)
#                except request.URLError:
#                    print("Whoops, that went wrong, retrying page "+str(l))
#                    if attempt == 4:
#                        deadlink.append(l)
#                        tmpdate.append(d)
#                        tmpcountry.append(c)
#                        tmpspeaker.append(s)
#                        tmplanguage.append(lang)
#                        tmptitle.append(t)
#                        tmplink.append(l)
#                        tmpspeech.append("404")
#                        print("Fetching speech " + str(l) + " failed due to HTTPError")
#                    time.sleep(10)
#                except ConnectionResetError:
#                    print("Whoops, that went wrong, retrying page "+str(l))
#                    if attempt == 4:
#                        deadlink.append(l)
#                        tmpdate.append(d)
#                        tmpcountry.append(c)
#                        tmpspeaker.append(s)
#                        tmplanguage.append(lang)
#                        tmptitle.append(t)
#                        tmplink.append(l)
#                        tmpspeech.append("404")
#                        print("Fetching speech " + str(l) + " failed due to HTTPError")
#                    time.sleep(10)
#                else:
#                    break
#
#output=zip(tmpdate,tmpcountry,tmpspeaker,tmplanguage,tmptitle,tmplink,tmpspeech,deadlink)
#dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
#with open(basedir+"/Speeches"+c+dt+".csv",mode="w",encoding="utf-8") as fo:
#    writer=csv.writer(fo)
#    writer.writerows(output)
#
#tmpdate=[]
#tmpcountry=[]
#tmpspeaker=[]
#tmplanguage=[]
#tmptitle=[]
#tmplink=[]
#tmpspeech=[]
#deadlink=[]
#print("Done scraping Czech speeches")        
##%% Scraping Greek speeches (http://www.primeminister.gov.gr/2012/06/21/9501 is not scraped because of strange structure, might be others)
#xpathspeech='//*[@class="articleitem"]/p/descendant-or-self::*/text()'
#for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):
#    if l.startswith("http://www.primeminister.gov.gr/"):
#        for attempt in range(5):
#            try:    
#                req=request.Request(l)
#                tree=html.fromstring(request.urlopen(req).read())
#                tmpspeech.append("<p>"+ "</p><p>".join(tree.xpath(xpathspeech))+"</p>")
#                tmpdate.append(d)
#                tmpcountry.append(c)
#                tmpspeaker.append(s)
#                tmplanguage.append(lang)
#                tmptitle.append(t)
#                tmplink.append(l)
#                deadlink.append("0")
#                time.sleep(randint(1,5))
#            except request.HTTPError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            except request.URLError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            except ConnectionResetError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            else:
#                break
#
#output=zip(tmpdate,tmpcountry,tmpspeaker,tmplanguage,tmptitle,tmplink,tmpspeech,deadlink)
#dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
#with open(basedir+"/Speeches"+c+dt+".csv",mode="w",encoding="utf-8") as fo:
#    writer=csv.writer(fo)
#    writer.writerows(output)
#
#tmpdate=[]
#tmpcountry=[]
#tmpspeaker=[]
#tmplanguage=[]
#tmptitle=[]
#tmplink=[]
#tmpspeech=[]
#deadlink=[]
#print("Done scraping Greek speeches")        
##%% Scraping Spanish speeches (http://www.lamoncloa.gob.es/lang/en/paginas/archivo/2008/31012008XXIHispAle.aspx is not a speech)
#xpathspeech='//*[@class="contenidoTexto"]/descendant-or-self::*/text()'
#for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):
#    if l.startswith("http://www.lamoncloa.gob.es/"):
#        for attempt in range(5):
#            try:    
#                req=request.Request(l)
#                tree=html.fromstring(request.urlopen(req).read())
#                tmpspeech.append("<p>"+ "</p><p>".join(tree.xpath(xpathspeech))+"</p>")
#                tmpdate.append(d)
#                tmpcountry.append(c)
#                tmpspeaker.append(s)
#                tmplanguage.append(lang)
#                tmptitle.append(t)
#                tmplink.append(l)
#                deadlink.append("0")
#                time.sleep(randint(1,5))
#            except request.HTTPError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            except request.URLError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            except ConnectionResetError:
#                print("Whoops, that went wrong, retrying page "+str(l))
#                if attempt == 4:
#                    deadlink.append(l)
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    tmpspeech.append("404")
#                    print("Fetching speech " + str(l) + " failed due to HTTPError")
#                time.sleep(10)
#            else:
#                break
#
#output=zip(tmpdate,tmpcountry,tmpspeaker,tmplanguage,tmptitle,tmplink,tmpspeech,deadlink)
#dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
#with open(basedir+"/Speeches"+c+dt+".csv",mode="w",encoding="utf-8") as fo:
#    writer=csv.writer(fo)
#    writer.writerows(output)
#
#tmpdate=[]
#tmpcountry=[]
#tmpspeaker=[]
#tmplanguage=[]
#tmptitle=[]
#tmplink=[]
#tmpspeech=[]
#deadlink=[]
#print("Done scraping Spanish speeches")        
##%% Scraping Greece Wayback speeches
#from lxml import etree
#xpathspeech='//*[@class="articleitem"]/p/descendant-or-self::*/text()'
#for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):
#
#    if l.startswith("https://web.archive.org/web/"):
#        if "http://www.primeminister.gov.gr/" in l:        
#            for attempt in range(5):
#                try:    
#                    req=request.Request(l)
#                    tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
#                    tmpspeech.append("<p>"+ "</p><p>".join(tree.xpath(xpathspeech))+"</p>")
#                    tmpdate.append(d)
#                    tmpcountry.append(c)
#                    tmpspeaker.append(s)
#                    tmplanguage.append(lang)
#                    tmptitle.append(t)
#                    tmplink.append(l)
#                    deadlink.append("0")
#                    time.sleep(randint(1,5))
#                except request.HTTPError:
#                    print("Whoops, that went wrong, retrying page "+str(l))
#                    if attempt == 4:
#                        deadlink.append(l)
#                        tmpdate.append(d)
#                        tmpcountry.append(c)
#                        tmpspeaker.append(s)
#                        tmplanguage.append(lang)
#                        tmptitle.append(t)
#                        tmplink.append(l)
#                        tmpspeech.append("404")
#                        print("Fetching speech " + str(l) + " failed due to HTTPError")
#                    time.sleep(10)
#                except request.URLError:
#                    print("Whoops, that went wrong, retrying page "+str(l))
#                    if attempt == 4:
#                        deadlink.append(l)
#                        tmpdate.append(d)
#                        tmpcountry.append(c)
#                        tmpspeaker.append(s)
#                        tmplanguage.append(lang)
#                        tmptitle.append(t)
#                        tmplink.append(l)
#                        tmpspeech.append("404")
#                        print("Fetching speech " + str(l) + " failed due to HTTPError")
#                    time.sleep(10)
#                except ConnectionResetError:
#                    print("Whoops, that went wrong, retrying page "+str(l))
#                    if attempt == 4:
#                        deadlink.append(l)
#                        tmpdate.append(d)
#                        tmpcountry.append(c)
#                        tmpspeaker.append(s)
#                        tmplanguage.append(lang)
#                        tmptitle.append(t)
#                        tmplink.append(l)
#                        tmpspeech.append("404")
#                        print("Fetching speech " + str(l) + " failed due to HTTPError")
#                    time.sleep(10)
#                except etree.ParserError:
#                    print("Whoops, ParserError, retrying page "+str(l))
#                    if attempt == 4:
#                        deadlink.append(l)
#                        tmpdate.append(d)
#                        tmpcountry.append(c)
#                        tmpspeaker.append(s)
#                        tmplanguage.append(lang)
#                        tmptitle.append(t)
#                        tmplink.append(l)
#                        tmpspeech.append("404")
#                        print("Fetching speech " + str(l) + " failed due to ParserError")
#                    time.sleep(10)
#                else:
#                    break
#
#output=zip(tmpdate,tmpcountry,tmpspeaker,tmplanguage,tmptitle,tmplink,tmpspeech,deadlink)
#dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
#with open(basedir+"/SpeechesWB"+c+dt+".csv",mode="w",encoding="utf-8") as fo:
#    writer=csv.writer(fo)
#    writer.writerows(output)
#
#tmpdate=[]
#tmpcountry=[]
#tmpspeaker=[]
#tmplanguage=[]
#tmptitle=[]
#tmplink=[]
#tmpspeech=[]
#deadlink=[]
#print("Done scraping Greek Wayback speeches")        
#%% Scraping UK Wayback speeches (scrapes both speech and introduction/additional info, tags text needs to be cleaned afterwards)
xpathspeech='//*[@class="entry"]/p/descendant-or-self::*/text()'
for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):

    if l.startswith("http://webarchive.nationalarchives.gov.uk/"):
        for attempt in range(5):
            try:    
                req=request.Request(l)
                tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
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
print("Done scraping UK Wayback speeches")        
#%% Scraping IMF speeches
xpathspeech='//*[@class="content"]/p/descendant-or-self::*/text()'
################
#comment Martijn:
# //*[@class="content"]/p/text()
#leaves out some meta data
################
################
#comment Erik:
# Doing this also leaves out any bold or italic text
################
for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):

    if l.startswith("http://www.imf.org/"):
        for attempt in range(5):
            try:    
                req=request.Request(l)
                tree=html.fromstring(request.urlopen(req).read())
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
print("Done scraping IMF speeches")
print("Start scraping European Commission speeches. Scraping ca. 7000 speeches takes a long time")       
#%% Scraping European Commission speeches (scrapes all text from page, including titles and introductions)
xpathspeech='//*[@id="contentPressRelease"]/descendant::*/text()'
for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):

    if l.startswith("http://europa.eu/rapid/"):
        for attempt in range(5):
            try:    
                req=request.Request(l)
                tree=html.fromstring(request.urlopen(req).read())
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
print("Done scraping European Commission speeches")        
#%% Scraping ECB speeches (multi-language) introductions are included: https://www.ecb.europa.eu/press/key/date/2007/html/sp071219.en.html
xpathspeech='//*[@class="ecb-pressContent"]/descendant::p/descendant-or-self::*/text()'
for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):

    if l.startswith("https://www.ecb.europa.eu/"):
        for attempt in range(5):
            try:    
                req=request.Request(l)
                tree=html.fromstring(request.urlopen(req).read())
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
print("Done scraping ECB speeches")        
#%% Scraping ALDE Group speeches
xpathspeech='//*[@class="news-single-content"]/descendant::p/descendant-or-self::*/text()'
for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):

    if l.startswith("http://www.alde.eu/"):
        for attempt in range(5):
            try:    
                req=request.Request(l)
                tree=html.fromstring(request.urlopen(req).read())
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
print("Done scraping ALDE speeches")        
#%% Scraping ECR Group speeches
xpathspeech='//*[@class="entry-content"]/descendant-or-self::*/text()'
for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):

    if l.startswith("http://ecrgroup.eu/"):
        for attempt in range(5):
            try:    
                req=request.Request(l)
                tree=html.fromstring(request.urlopen(req).read())
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
print("Done scraping ECR speeches")        
#%%
xpathspeech='//p[@class="contents"]/descendant-or-self::*/text()'
for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):

    if l.startswith("http://www.europarl.europa.eu/"):
        for attempt in range(5):
            try:    
                req=request.Request(l)
                tree=html.fromstring(request.urlopen(req).read())
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
print("Done scraping European Parliament speeches")        
#%% Scraping European Council html speeches
xpathspeech='//*[@class="free-text none "]/descendant::p/descendant-or-self::*/text()'
for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):

    if l.startswith("http://www.consilium.europa.eu/en/press/"):
        for attempt in range(5):
            try:    
                req=request.Request(l)
                tree=html.fromstring(request.urlopen(req).read())
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
print("Done scraping European Council HTML speeches")        
#%% Scraping European Council pdf speeches (note that these speeches contain all text from the pdf, including any headers/footers)
xpathspeech='//div/descendant::*/text()'
for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):

    if l.startswith("http://www.consilium.europa.eu/en/workarea/"):
        tmpspeech.append("404")
        deadlink.append(l)
        tmpdate.append(d)
        tmpcountry.append(c)
        tmpspeaker.append(s)
        tmplanguage.append(lang)
        tmptitle.append(t)
        tmplink.append(l)
#        try:    
#            request.urlretrieve(l, "/media/home/Temp/temp.pdf")
#            subprocess.Popen("abiword -t /media/home/Temp/temp.html /media/home/Temp/temp.pdf", shell=True)
#            tree=html.fromstring(request.urlopen("file:///media/home/Temp/temp.html").read())
#            tempspeeches.append(tree.xpath(xpathspeech))
#            time.sleep(randint(1,5))
#        except request.HTTPError:
#            deadlinks.append(l)
#            tempspeeches.append("404")
#            print("Fetching speech " + str(l) + " failed due to HTTPError")
#            time.sleep(randint(1,5))
#        except request.URLError:
#            deadlinks.append(l)
#            tempspeeches.append("404")
#            print("Fetching speech " + str(l) + " failed due to HTTPError")
#            time.sleep(randint(1,5))
output=zip(tmpdate,tmpcountry,tmpspeaker,tmplanguage,tmptitle,tmplink,tmpspeech,deadlink)
dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
with open(basedir+"/Speeches"+c+dt+"HTML.csv",mode="w",encoding="utf-8") as fo:
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
print("Done scraping European Council PDF speeches")        
#%% Scraping Italy speeches
xpathspeech='//*[@class="dvTesto" or @class="dvtesto"]/descendant-or-self::*/text()'
for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):

    if "sitiarcheologici.palazzochigi.it" in l:
        for attempt in range(5):
            try:    
                req=request.Request(l)
                tree=html.fromstring(request.urlopen(req).read())
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

print("Done scraping Italian speeches")
#%%
xpathspeech='//*[@class="dvTesto" or @class="dvtesto"]/descendant-or-self::*/text()'
for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):

    if l.startswith("http://www.governo.it/"):
        for attempt in range(5):
            try:    
                req=request.Request(re.sub("http://www.governo.it/web","https://web.archive.org/web",l))
                tree=html.fromstring(request.urlopen(req).read())
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
print("Done scraping Italian speeches")
#%% Scraping Portugal speeches
xpathspeech='//*[@class="margin20 font_increase"]/descendant::p/descendant-or-self::*/text()'
for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):
    if s == "Passos Coelho":
        tempspeeches.append("404")
        deadlink.append(l)
        tmpdate.append(d)
        tmpcountry.append(c)
        tmpspeaker.append(s)
        tmplanguage.append(lang)
        tmptitle.append(t)
        tmplink.append(l)
        tmpspeech.append("404")
output=zip(tmpdate,tmpcountry,tmpspeaker,tmplanguage,tmptitle,tmplink,tmpspeech,deadlink)
dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
with open(basedir+"/SpeechesPDF1"+c+dt+".csv",mode="w",encoding="utf-8") as fo:
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
for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):
    if s == "Jose Socrates":
        for attempt in range(5):
            try:    
                req=request.Request(l)
                tree=html.fromstring(request.urlopen(req).read())
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
for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):
    if s == "Antonia Costa":
        deadlink.append(l)
        tmpdate.append(d)
        tmpcountry.append(c)
        tmpspeaker.append(s)
        tmplanguage.append(lang)
        tmptitle.append(t)
        tmplink.append(l)
        tmpspeech.append("404")
output=zip(tmpdate,tmpcountry,tmpspeaker,tmplanguage,tmptitle,tmplink,tmpspeech,deadlink)
dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
with open(basedir+"/SpeechesPDF2"+c+dt+".csv",mode="w",encoding="utf-8") as fo:
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
print("Done scraping Portugese speeches")
#%% Scraping Poland speeches
xpathspeech='//*[@class="richText text-resize"]/descendant::p/descendant-or-self::*/text()'
for d,c,s,lang,t,l in zip(date,country,speaker,language,title,completelinks):

    if "premier.gov.pl" in l:
        for attempt in range(5):
            try:    
                req=request.Request(l)
                tree=html.fromstring(request.urlopen(req).read())
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
print("Done scraping Polish speeches")      
##%% Use length of tempspeeches lists to determine empty speeches
#for l,s in zip(completelinks,tempspeeches):
#    if len(s) < 2:
#        emptyspeeches.append(l)
#for speech in tempspeeches:
#    speeches.append("<p>"+ "</p><p>".join(speech)+"</p>")
##%%
#output=zip(date,country,speaker,language,title,completelinks,speeches)
##raw data output, without header rows, can be used for further data processing, but is by no means a final product
#dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
#with open("/media/home/Temp/EUEngage/SpeechesCombinedDEF"+dt+".csv",mode="w",encoding="utf-8") as fo:
#    writer=csv.writer(fo)
#    writer.writerows(output)
#
#output=zip(deadlinks,emptyspeeches)
##raw data output, without header rows, can be used for further data processing, but is by no means a final product
#dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
#with open("/media/home/Temp/EUEngage/SpeechesCombinedDeadlinks"+dt+".csv",mode="w",encoding="utf-8") as fo:
#    writer=csv.writer(fo)
#    writer.writerows(output)
print("Done")
