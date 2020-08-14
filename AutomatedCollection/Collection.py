# Automated Collection for EUSpeech
# Author: Nicolai Berk
# 18-07-2020 
#
# Mail me via nicolai.berk@gmail.com

# import
import os
import pandas as pd
from functions import *
import time

# define folders global vars
linkdir=os.getcwd()+'/Links/'
speechdir=os.getcwd()+'/Speeches/'
finaldir=os.getcwd()+'/FinalSpeeches/'

countries_collected = 0
countries_failed = 0
speeches_collected = 0
speeches_faied = 0
report = ''



# collect new links for each country (starting from last collection date, which needs to be loaded)

## get mindate from last collection
prev_col = open('datestamp.txt', 'r').read()

## load csv with general links and definitions
CollectLinks = pd.read_csv('CollectLinks.csv', sep = ',')

## replace NaN
CollectLinks = CollectLinks.where(pd.notnull(CollectLinks), None)


## subset
standardLinks = CollectLinks[CollectLinks['selenium'] == 0]
seleniumLinks = CollectLinks[CollectLinks['selenium'] == 1]

## delete old file and write header for linkfile
header = ['speaker', 'url', 'linkbase', 'xpathLink', 'xpathTitle', 'xpathDate', 'regexDate', 'strToDate', 
          'country', 'language', 'selenium', 'xpbutton', 'xpcookie', 'process', 'xpathSpeech', 
          'regexSpeech', 'regexControl', 'start', 'fmt_url', 'dt_obj', 'date', 'title', 'urlSpeech']
with open(linkdir+'links.csv', mode = 'w') as fi:
    writer = csv.writer(fi, lineterminator = '\n')
    writer.writerow(header)


## scrape links of normal websites (make this nicer with zip(cols))
for index, row  in standardLinks.iterrows(): 
    linkScraper(file        = 'links', 
                path        = linkdir, 
                sender      = row['speaker'], 
                url         = row['url'], 
                linkbase    = row['linkbase'], 
                xpathLinks  = row['xpathLinks'], 
                xpathTitles = row['xpathTitles'], 
                xpathDates  = row['xpathDates'], 
                regexDates  = row['regexDates'], 
                strToDates  = row['strToDates'],
                mindate     = prev_col,
                country     = row['country'],
                language    = row['language'],
                xpathSpeech = row['xpathSpeech'],
                regexSpeech  = row['regexSpeech'], 
                regexControl = row['regexControl'], 
#                 mode        = 'a',
                start       = row['start'],
                fmt_url     = row['fmt_url'])


    
# as Greek website prevents scraping with incapsula, it could be scraped with selenium, but this is probably better done by hand than in a function
    
## scrape links with selenium, add to other links
# for index, row in seleniumLinks.iterrows():
#     seleniumScraper(file         = 'links', 
#                     path         = linkdir, 
#                     sender       = row['speaker'], 
#                     url          = row['url'], 
#                     linkbase     = row['linkbase'], 
#                     xpathLinks   = row['xpathLinks'], 
#                     xpathTitles  = row['xpathTitles'], 
#                     xpathDates   = row['xpathDates'], 
#                     regexDates   = row['regexDates'], 
#                     strToDates   = row['strToDates'],
#                     mindate      = prev_col,
#                     country      = row['country'],
#                     language     = row['language'],
#                     xpbutton     = row['xpbutton'],
#                     xpcookie     = row['xpcookie'],
#                     process      = row['process'],
#                     xpathSpeech  = row['xpathSpeech'],
#                     regexSpeech  = row['regexSpeech'], 
#                     regexControl = row['regexControl'], 
#                     mode         = 'a',
#                     dt_obj       = row['dt_obj'])
    
# run collection of speeches
speechScraper('links.csv', linkdir, speechdir, mode = 'w', min_len = 200)

# run language recognition
langdetectspeeches('Speeches/speeches','FinalSpeeches/speeches_final', readHeader = False, mode = 'a', timestamp = False)

# write mindate for next collection
now  = time.strftime('%d/%m/%Y', time.gmtime(time.time()))
open('datestamp.txt', 'w').write(now)
