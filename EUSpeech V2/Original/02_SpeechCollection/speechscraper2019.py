# -*- coding: utf-8 -*-
"""
Created on Wed May 22 10:22:31 2019

Speech Scraper EUSpeech 2019

@author: NB
"""
#%% import and vars
import csv
from urllib import request
from lxml import html
import re
import time
from random import randint
import datetime

linkdir = 'C:/Users/samunico/OneDrive/Dokumente/Studium/Amsterdam/Gijs/Speeches/Scraping/I - Linkscraping'
speechdir = 'C:/Users/samunico/OneDrive/Dokumente/Studium/Amsterdam/Gijs/Speeches/Scraping/II - Speechscraping'
deadlinks = []
unwanted = []
i = 0
mis = 0
unw = 0

headers = {'User-Agent': 'Chrome/41.0.2228.0'}


#%% speech collection

print('Start fetching speeches...\n')

dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

with open(linkdir+"/CompleteLinks/linkset_20190722-150637.csv", mode="r",encoding="utf-8") as fi: # Change to correct directory before importing
    with open(speechdir+"/Speeches/speeches_"+dt+".csv", mode="w",encoding="utf-8") as fo: # Change to correct directory before importing
        reader = csv.reader(fi,delimiter=",")
        next(reader)
        writer = csv.writer(fo, lineterminator = '\n')
        firstrow = ['Date', 'Country', 'Speaker', 'Language', 'Title', 'URL']
        writer.writerow(firstrow)
        for row in reader:
            print("\tFetching speech #", str(i+1), '...' , end = "\r")
            for attempt in range(3):
                try:
                    fetchlink = row[5]
                    country = row[1]
                    req = request.Request(url = str(fetchlink), headers = headers)
                    tree = html.fromstring(request.urlopen(req).read().decode(encoding="utf-8"))
                except request.HTTPError:
                    print("Whoops, that went wrong, retrying page "+ fetchlink +" for "+ row[2] + " "+ row[3])
                    if attempt == 2:
                        print("Fetching page " + fetchlink +" for "+ row[2] + " "+ row[3] + " failed due to HTTPError")
                        deadlinks.append(fetchlink)
                        mis += 1
                        continue
                    time.sleep(10)
                except request.URLError:
                    print("Whoops, that went wrong, retrying page "+ fetchlink +" for "+ row[2] + " "+ row[3])
                    if attempt == 2:
                        print("Fetching page " + fetchlink +" for "+ row[2] + " "+ row[3] + " failed due to URLError")
                        deadlinks.append(fetchlink)
                        mis += 1
                        continue
                    time.sleep(10)
                except:
                    print("Whoops, that went wrong, retrying page "+ fetchlink +" for "+ row[2] + " "+ row[3])
                    if attempt == 2:
                        print("Fetching page " + fetchlink +" for "+ row[2] + " "+ row[3] + " failed due to Unknown Error")
                        deadlinks.append(fetchlink)
                        mis += 1
                        continue
                    time.sleep(10)
                    
                
            # define xpath dependent on page
            if country == 'Czech Republic':
                xpath = '//*[@id="content"]/div[1]/div/div[1]/div/p/text()'
                regex = 0
            
            elif country == 'France':
                
                if re.match('.*[Dd]éclaration.*', row[4]):
                    
                    regex = '.*ti :(.*)'
                    # add if statement for newest macron speeches (other xpath and sort out non-speeches)
                    if fetchlink.startswith('https://www.elysee.fr'):
                        temp = tree.xpath('//*[@id="main"]/section[*]/div/div/div[1]/p/span/text()')
                        test = ''
                        for t in temp:
                            test += t + ' '
                        
                        if re.match('.* - Seul le prononcé fait foi.*', test):
                            xpath = '//*[@id="main"]/section/div/div/div[2]/p/text()'
                            if tree.xpath(xpath) == []:
                                xpath = '//*[@id="transcript-1"]/div[2]/div/div/div/div[2]//text()'
                        else:
                            unwanted.append(fetchlink)    
                            unw += 1
                            continue
                    else:             
                        xpath = '//*[@id="content"]/div[1]//text()'
                else:
                    unwanted.append(fetchlink)    
                    unw += 1
                    continue
                
            elif country == 'Germany':
                xpath = '//*[@id="main"]/div/div[2]/p/text()'
                if tree.xpath(xpath) == []:
                    xpath = '//*[@id="main"]/div/div[1]//text()'    
                regex = 0
                
# =============================================================================
#             elif country == 'Greece':    
#                 # sort out non-speeches
#                 cats = str(tree.xpath('//article/@class'))
#                 if re.match('.*(category-speeches).*', cats):
#                     xpath = '//article/div[2]//text()'
#                     regex = 0
#                 else:
#                     continue
# =============================================================================
                
            elif country == 'Netherlands':
                xpath = '//*[@id="content"]//text()'
                regex = '.*Toespraak +\| \d{2}-\d{2}-\d{4}(.*)'
                re_en = '.*toespraak is alleen beschikbaar in het Engels\. *(.*)|.*toespraak is alleen in het Engels beschikbaar\. *(.*)|.*toespraak is in het Engels uitgesproken\. *(.*)'
                re_de = '.*toespraak is alleen beschikbaar in het Duits\. *(.*)|.*toespraak is alleen in het Duits beschikbaar\. *(.*)'
                if re.match(re_en, str(tree.xpath('//*[@id="content"]/div/p/text()'))):
                    row[3] = 'EN'
                    regex  = re_en
                if re.match(re_de, str(tree.xpath('//*[@id="content"]/div/p/text()'))):
                    row[3] = 'DE'
                    regex  = re_de
                else:
                    row[3] = 'NL'
                
            # PDFs for Portugal have to be read in a separate process
            elif country == 'Portugal':
                continue 
            
            # Spain not scraped at the moment (website too slow)
            
            elif country == 'Great Britain':
                # sort out non-speeches
                cats = str(tree.xpath('//*[@id="content"]/div[3]/div[1]/div[1]/div[1]/dl/dd/text()'))
                if re.match('.*(Transcript of the speech, exactly as it was delivered).*', cats):
                    xpath = '//*[@id="content"]/div[3]/div[1]/div[1]/div[2]/div//text()'
                    regex = 0
                else:
                    unwanted.append(fetchlink)    
                    unw += 1
                    continue
            
            elif country == 'Sweden':
                xpath = '//*[@id="content"]/section/div[1]/div/p/text()'
                regex = '.*Check against delivery\.(.*)|.*Det talade ordet gäller\.(.*)'
            
            elif country == 'Denmark':
                xpath = '//*[@id="main"]/div[2]//text()'
                regex = '.*[Cc][Hh][Ee][Cc][Kk] [Aa][Gg][Aa][Ii][Nn][Ss][Tt] [Dd][Ee][Ll][Ii][Vv][Ee][Rr][Yy](.*)|.*Det talte ord gælder(.*)'
            
            elif country == 'Norway':
                xpath = '//*[@id="mainContent"]/div[1]/div/div[3]//text()'
                regex = '.*Check against delivery(.*)|.*Sjekkes mot fremføring(.*)|.*Sjekkes mot framføring(.*)'
                if tree.xpath(xpath) == []:
                    xpath = '//*[@id="mainContent"]/div[1]/div/div[2]//p/text()'
                # replace language with actual speech language:
                if re.match('https://www.regjeringen.no/en/.*', fetchlink):
                    row[3] = 'EN'
                
            elif country == 'Estonia':
                xpath = '//*[@id="block-system-main"]/div/div//text()'
                regex = '.*\d\d\d\d - \d+:\d\d(.*)KÕIK UUDISED.*|.*\d\d\d\d - \d+:\d\d(.*)Kõik uudised.*|.*\d\d\d\d - \d+:\d\d(.*)[Aa][Ll][Ll] [Nn][Ee][Ww][Ss].*|.*\d\d\d\d - \d\d:\d\d(.*)'
            else:
                print('Unknown country')
                break                        
                                                            
            txt = tree.xpath(xpath)
            if txt == []:
                print('No speech found for\n\t', fetchlink, '\n\t using xpath: ', xpath)
                deadlinks.append(fetchlink)
                mis += 1
                continue
                
            txtstr = ''
            
            for t in txt:
                txtstr += t + ' '
            cleantxt = re.sub("\r|\n|\t|\\xa0|\* \* \*"," ",txtstr.lstrip())
            
            if regex != 0:
                try:
                    # see regex norway and sweden
                    if str(re.match(regex, cleantxt).group(1)) == 'None':
                        if str(re.match(regex, cleantxt).group(2)) == 'None':
                            if str(re.match(regex, cleantxt).group(3)) == 'None':
                                cleantxt = re.sub("\r|\n|\t|\* \* \*"," ",txtstr.lstrip())
                            else:
                                cleantxt = re.match(regex, cleantxt).group(3)
                        else:
                            cleantxt = re.match(regex, cleantxt).group(2)
                    else:
                        cleantxt = re.match(regex, cleantxt).group(1)
                except AttributeError:
                    pass
            
            cleantxt = re.sub(' +', ' ', cleantxt)
            
            if len(cleantxt)<200:
                print('\tVery short speech: ', str(row), '\n\tSKIPPING SPEECH')
                deadlinks.append(fetchlink)
                mis += 1
                continue
            
            row.append(cleantxt)
            writer.writerow(row)
            i += 1
            time.sleep(randint(1,3))


with open(speechdir+"/Speeches/deadlinks_"+dt+".csv", mode="w",encoding="utf-8") as fo: # Change to correct directory before importing
    writer = csv.writer(fo, lineterminator = '\n')
    for dl in deadlinks:
        writer.writerow(dl)  

with open(speechdir+"/Speeches/outsorted_"+dt+".csv", mode="w",encoding="utf-8") as fo: # Change to correct directory before importing
    writer = csv.writer(fo, lineterminator = '\n')
    for uw in unwanted:
        writer.writerow(uw)  

print('Finished fetching {} speeches'.format(str(i)))
print('Collection of {} links failed'.format(str(mis)))
print('{} links sorted out.'.format(str(unw)))

