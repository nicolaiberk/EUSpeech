# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 13:32:29 2019

Portugal

@author: samunico
"""

#%% setup
from lxml import html
from urllib import request
import time
import re
import datetime
import csv
from random import randint
import PyPDF2

completelinks = []
date = []
speaker = []
country = []
language = []
title = []
deadlinks = []
now=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}



#%% link collection
basedir = "C:/Users/samunico/OneDrive/Dokumente/Studium/"+\
            "Amsterdam/Gijs/Speeches/Scraping/I - Linkscraping/"+\
            "CompleteLinks/portugal/"
linkpath =  basedir+"Portugal_"+now+".csv"

# generate csv and print header
with open(linkpath, mode="w", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    # write header:
    firstrow = ['Date', 'Country', 'Speaker', 'Language', 'Title', 'URL']
    writer.writerow(firstrow)
    
# only PDFs
# this could be solved using https://automatetheboringstuff.com/chapter13/ and
# https://pypi.org/project/pyPdf/

fetchlink="https://www.portugal.gov.pt/pt/gc21/comunicacao/intervencoes?f=primeiro+ministro&p="
author="A. Costa"
location="Portugal"
lang="PT"
numbers=list(range(0,int(9)))
xpathlink = '//*[@id="dvCentroCT"]/div[4]/div/div[1]/div[*]/div[1]/a/@href'
xpathdate = '//*[@id="dvCentroCT"]/div[4]/div/div[1]/div[*]/div[1]/div/text()'
xpathtitle = '//*[@id="dvCentroCT"]/div[4]/div/div[1]/div[*]/div[1]/a/text()'
xpathmp = '//*[@id="PageSelector__ctl0_SearchResultList_PaginationControl_container"]/div[1]/text()'
regexmp = ".*1 de (\d+)"
strtodate="%Y-%m-%d"

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
    maxno=int(re.match(regexmp,maxpage).group(1))
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
                req=request.Request(fetchlink + str(number+1), headers = headers)
                tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
                templinks = tree.xpath(xpathlink)
                tempdate=(tree.xpath(xpathdate))
                temptitle=(tree.xpath(xpathtitle))
                for dt,tt,lk in zip(tempdate,temptitle,templinks):
                    tmpdt=time.strptime(dt[35:45], strtodate)
                    row = []
                    row.append(time.strftime("%d-%m-%Y",tmpdt))
                    row.append(location)
                    row.append(author)
                    row.append(lang)
                    ttf = re.match('[^\s*].*[^\s*]', re.sub("\r|\n|\t","",tt.lstrip())).group(0)
                    row.append(ttf)
                    row.append(re.match(' *(.*)', lk).group(1))
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

#%% get links to pdfs from collected websites
xpathlink = '//div[5]/div[2]/div/a/@href'
xpath2 = '//*[@id="regText"]//text()'
pdflinks =  basedir+"PortugalPDFlinks_"+now+".csv"
i = 0
j = 0
x = 0
n = 0
deadlinks = []

with open(pdflinks, mode="w", encoding="utf-8") as fo:
    writer=csv.writer(fo, lineterminator = '\n')
    writer.writerow(firstrow)

with open(linkpath, mode="r", encoding="utf-8") as fi:
    reader=csv.reader(fi, lineterminator = '\n')
    next(reader)
    with open(pdflinks, mode = 'a', encoding = 'utf-8') as fo:
        writer = csv.writer(fo, lineterminator = '\n')
        for row in reader:
            print(n) # only works w extensive stoptime
            time.sleep(2)
            fetchlink = row[5]
            req=request.Request(fetchlink, headers = headers)
            time.sleep(2)
            tree=html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
            time.sleep(2)
            pdflink = tree.xpath(xpathlink)
            row_n = []
            for r in row:
                row_n.append(r)
            time.sleep(2)
            try:
                row_n[5] = pdflink[0]
                i += 1
                writer.writerow(row_n)
            #except IndexError:
            #    pdflink = tree.xpath(xpath2)
            #    row_n.append(fetchlink)
            #    speech = ''
            #    for s in pdflink:
            #        speech += s
            #    cleantxt = re.sub("\r|\n|\t"," ",speech.lstrip())
            #    row_n.append(cleantxt)
            #    with open(basedir+'portugal_speeches.csv', mode = 'a', encoding = 'utf-8') as fo2:
            #        writer2 = csv.writer(fo2, lineterminator = '\n')
            #        writer2.writerow(row_n)
            #    j += 1
            except:
                deadlinks.append(fetchlink)
                x += 1
            n += 1
            
                

print('Collected {} PDF links',\
      #'and {} html speech(es)',\
      '. {} link(s) failed.'.format(i,j,x))
if len(deadlinks) > 0:
    print('The following links failed:')
    for l in deadlinks:
        print(l)


#%% pdf download (see https://stackabuse.com/download-files-with-python/)


basedir = "C:/Users/samunico/OneDrive/Dokumente/Studium/"+\
            "Amsterdam/Gijs/Speeches/Scraping/II - Speechscraping/"+\
            "Speeches/pdfs_portugal/"
            
writer = csv.writer(fo)
with open(pdflinks, mode = 'r') as fi:
    reader = csv.reader(fi)
    next(reader)
    i = 0
    for row in reader:
        print('Fetching link {} of 72 ({}%)'.format(i, round((i/72)*100, 2)),\
              flush = True)
        fetchlink = row[5]
        filename = basedir + 'pdf' + str(i) + '.pdf'
        time.sleep(10) # only works w very extensive stoptime, else PDFs not downloaded
        request.urlretrieve(fetchlink, filename)
        i+=1

print('{} pdfs fetched'.format(i))

#%% read pdfs

basedir = "C:/Users/samunico/OneDrive/Dokumente/Studium/"+\
            "Amsterdam/Gijs/Speeches/Scraping/II - Speechscraping/"+\
            "Speeches/"
            
pdflinks = 'C:/Users/samunico/OneDrive/Dokumente/Studium/Amsterdam/Gijs/Speeches/Scraping/I - Linkscraping/CompleteLinks/portugal/PortugalPDFlinks_20190711-102139.csv'

i = 0
# directory should be changed to final speechfile
with open(basedir+'portugal_speeches_test.csv', mode = 'w', encoding = 'utf-8') as fo:
    writer = csv.writer(fo, lineterminator = '\n')
    with open(pdflinks, mode = 'r', encoding = 'utf-8') as fi:
        reader = csv.reader(fi, lineterminator = '\n')
        next(reader)
        for row in reader:
            pdf = basedir + 'pdfs_portugal/pdf' + str(i) + '.pdf'
            pdfReader = PyPDF2.PdfFileReader(pdf)
            txt = ''
            for p in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(p)
                txt += pageObj.extractText()[6:] #index removes page number
            cleantxt = re.sub(("\r|\n|\t|_+"), "", txt)
            row.append(cleantxt)
            writer.writerow(row)
            i += 1
            


            
