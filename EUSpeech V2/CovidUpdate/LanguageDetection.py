"""
Nicolai Berk
"""


import os
import csv
import re

path=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/")
os.chdir(path)

from functions import langdetectspeeches




#%% run language detection

inputcsv="Speeches/speeches_20200506-172749"
outputcsv="Speeches/speechesCovidUpdate_LangDet"
output= ["date",
         "speaker",
         "title",
         "completelinks",
         "text",
         "lang",
         "lang_prob",
         "nooflanguages",
         "lenspeech",
         "lenspeech2",
         "checkspeech"]

langdetectspeeches(path,
                   inputcsv,
                   outputcsv,
                   n_tot=1500,
                   writeHeader=output,
                   readHeader=False)



#%% add countrynames
output= ["date",
         "country",
         "speaker",
         "title",
         "completelinks",
         "text",
         "lang",
         "lang_prob",
         "nooflanguages",
         "lenspeech",
         "lenspeech2",
         "checkspeech"]

inputcsv="Speeches/speechesCovidUpdate_LangDet"
outputcsv="Speeches/speechesCovidUpdate_20200511"
with open(path+inputcsv+'.csv', mode='r', encoding = 'utf-8') as fi:
    reader=csv.reader(fi)
    next(reader)
    with open(path+outputcsv+'.csv', mode='w', encoding ='utf-8') as fo:
        writer=csv.writer(fo)
        writer.writerow(output) # Header
        for row in reader:
            date = row[0]
            speaker = row[1]
            title = row[2]
            url = row[3]
            text=row[4]
            row[1]=re.sub('A. Babis',      'Czech Republic', row[1])
            row[1]=re.sub('A. Merkel',     'Germany' , row[1])
            row[1]=re.sub('M. Frederiksen','Denmark' , row[1])
            row[1]=re.sub('L. Rasmussen',  'Denmark' , row[1])
            row[1]=re.sub('J.Ratas',       'Estonia' , row[1])
            row[1]=re.sub('E. Macron',     'France'  , row[1])
            row[1]=re.sub('G. Conte',      'Italy'   , row[1])
            row[1]=re.sub('M. Rutte',      'The Netherlands', row[1])
            row[1]=re.sub('E. Solberg',    'Norway', row[1])
            row[1]=re.sub('S.Loefven',     'Sweden', row[1])
            row[1]=re.sub('A. Duda',       'Poland', row[1])
            country = row[1]
            writer.writerow([date, country, speaker, title, url, text,row[5], row[6], row[7], row[8], row[9], row[10]])



## additional language detection for Britain
inputcsv='Speeches/GB'+dt
outputcsv="Speeches/GB"+dt+"_LangDet_new"
output= ["date",
         "country",
         "speaker",
         "title",
         "completelinks",
         "text",
         "lang",
         "lang_prob",
         "nooflanguages",
         "lenspeech",
         "lenspeech2",
         "checkspeech"]

langdetectspeeches(path,
                   inputcsv,
                   outputcsv,
                   n_tot=43,
                   writeHeader=output,
                   readHeader=True)
