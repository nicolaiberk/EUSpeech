# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 19:09:33 2016

@author: tykes
"""

from lxml import html
from urllib import request
from random import randint
import time
import re
import csv
import datetime #for naming the output file, so that the script can be run multiple times without overwriting
import subprocess
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
#%%
with open (basedir+"/SpeechesEUCouncilPDF.csv") as fi: # Change to correct directory before importing
    reader=csv.reader(fi,delimiter=",")
    for row in reader:
        tmpdate.append(row[0])
        tmpcountry.append(row[1])
        tmpspeaker.append(row[2])
        tmplanguage.append(row[3])
        tmptitle.append(row[4])
        tmplink.append(row[5])
        tmpspeech.append(row[6])
        deadlink.append(row[7])
with open (basedir+"/SpeechesPOPDF1.csv") as fi: # Change to correct directory before importing
    reader=csv.reader(fi,delimiter=",")
    for row in reader:
        tmpdate.append(row[0])
        tmpcountry.append(row[1])
        tmpspeaker.append(row[2])
        tmplanguage.append(row[3])
        tmptitle.append(row[4])
        tmplink.append(row[5])
        tmpspeech.append(row[6])
        deadlink.append(row[7])
with open (basedir+"/SpeechesPOPDF2.csv") as fi: # Change to correct directory before importing
    reader=csv.reader(fi,delimiter=",")
    for row in reader:
        tmpdate.append(row[0])
        tmpcountry.append(row[1])
        tmpspeaker.append(row[2])
        tmplanguage.append(row[3])
        tmptitle.append(row[4])
        tmplink.append(row[5])
        tmpspeech.append(row[6])
        deadlink.append(row[7])

print("Importing done, starting scraping")
numbers=list(range(0,len(tmplink)))
#%%
for n,l in zip(numbers,tmplink):
    for attempt in range(3):
    
        try:    
            request.urlretrieve(l, basedir+"/pdf/temp"+str(n)+".pdf")
        except request.HTTPError:
            print("Whoops, that went wrong, retrying first page for")
            if attempt == 2:
                print("Fetching first page failed due to HTTPError")
        except request.URLError:
            print("Whoops, that went wrong, retrying first page for")
            if attempt == 2:
                print("Fetching first page failed due to HTTPError")
        else:
            break
#%%
abiword=subprocess.Popen("abiword -t html "+basedir+"/pdf/*.pdf", shell=True)
#%% Importing relevant speeches, nonrelevant ones (newspaper articles, presentations etc. have been manually removed)
# Selecting relevant items means everything without pictures on the cover
xpathspeech='//div/descendant::*/text()'
tmpspeech=[]
for n in numbers:
    tree=html.fromstring(request.urlopen("file://"+basedir+"/pdf/temp"+str(n)+".html").read())
    tmpspeech.append("".join(tree.xpath(xpathspeech)))     
#%%
outdate=[]
outcountry=[]
outspeaker=[]
outlanguage=[]
outtitle=[]
outlink=[]
outspeech=[]
outdeadlink=[]
for d,c,s,lang,t,l,speech in zip(tmpdate,tmpcountry,tmpspeaker,tmplanguage,tmptitle,tmplink,tmpspeech):
    if c == "European Council":
        outspeech.append(speech)
        outdate.append(d)
        outcountry.append(c)
        outspeaker.append(s)
        outlanguage.append(lang)
        outtitle.append(t)
        outlink.append(l)
        outdeadlink.append("0")
output=zip(outdate,outcountry,outspeaker,outlanguage,outtitle,outlink,outspeech,outdeadlink)
dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
with open(basedir+"/SpeechesEUCouncilPDF"+dt+".csv",mode="w",encoding="utf-8") as fo:
    writer=csv.writer(fo)
    writer.writerows(output)
outdate=[]
outcountry=[]
outspeaker=[]
outlanguage=[]
outtitle=[]
outlink=[]
outspeech=[]
outdeadlink=[]
for d,c,s,lang,t,l,speech in zip(tmpdate,tmpcountry,tmpspeaker,tmplanguage,tmptitle,tmplink,tmpspeech):
    if c == "Portugal":
        outspeech.append(speech)
        outdate.append(d)
        outcountry.append(c)
        outspeaker.append(s)
        outlanguage.append(lang)
        outtitle.append(t)
        outlink.append(l)
        outdeadlink.append("0")
output=zip(outdate,outcountry,outspeaker,outlanguage,outtitle,outlink,outspeech,outdeadlink)
dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
with open(basedir+"/SpeechesPOPDF"+dt+".csv",mode="w",encoding="utf-8") as fo:
    writer=csv.writer(fo)
    writer.writerows(output)