# Automated Collection for EUSpeech
# Author: Nicolai Berk
# 18-07-2020 
#
# Mail me via nicolai.berk@gmail.com

# import
import os
import pandas as pd
from functions import *

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
CollectLinks = pd.read_csv('CollectLinks.csv')

## replace NaN
CollectLinks = CollectLinks.where(pd.notnull(CollectLinks), None)


## delete old links
if os.path.exists(linkdir+"links.csv"):
  os.remove(linkdir+"links.csv")

## subset
standardLinks = CollectLinks[CollectLinks['selenium'] == 0]
seleniumLinks = CollectLinks[CollectLinks['selenium'] == 1]

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
                mode        = 'a')


    
## scrape links with selenium, add to other links
for index, row in seleniumLinks.iterrows():
    seleniumScraper(file        = 'links', 
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
                    xpbutton    = row['xpbutton'],
                    xpcookie    = row['xpcookie'],
                    process     = row['process'],
                    mode        = 'a')


# run collection of speeches



# run language recognition

# append to existing data

## write mindate for next collection

# send report via mail (from https://realpython.com/python-send-email/)