# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 13:19:42 2015

@author: tykes
"""
import csv
import datetime
completelinks=[]
date=[]
speaker=[]
country=[]
language=[]
title=[]
deadlinks=[]

with open ("//home/tykes/Documenten/EU Engage/Final/LinksCombinedDEF.csv") as fi: # Change to correct directory before importing
    reader=csv.reader(fi,delimiter=",")
    for row in reader:
        date.append(row[0])
        country.append(row[1])
        speaker.append(row[2])
        language.append(row[3])
        title.append(row[4])
        completelinks.append(row[5])
print("Importing done, starting scraping")
with open ("//home/tykes/Documenten/EU Engage/Final/PortugalDEF.csv") as fi: # Change to correct directory before importing
    reader=csv.reader(fi,delimiter=",")
    for row in reader:
        date.append(row[0])
        country.append(row[1])
        speaker.append(row[2])
        language.append(row[3])
        title.append(row[4])
        completelinks.append(row[5])
print("Importing done, starting scraping")
##%%
#import time
#strtodate="%d/%m/%Y"
#for index, d in enumerate(date):
#    if "/" in d:
#        date[index]="European Council"
#        tmpdt=time.strptime(d, strtodate)
#        date[index]=(time.strftime("%d-%m-%Y",tmpdt))

#%%
output=zip(date,country,speaker,language,title,completelinks)
#raw data output, without header rows, can be used for further data processing, but is by no means a final product
dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
with open("/home/tykes/MergedDEF"+dt+".csv",mode="w",encoding="utf-8") as fo:
    writer=csv.writer(fo)
    writer.writerows(output)