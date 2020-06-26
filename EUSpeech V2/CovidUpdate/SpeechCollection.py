#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 13:01:09 2020

Speechcollection for Covid update

@author: Nicolai Berk
"""

import os
os.chdir('ADD/PATH/HERE')
import datetime
from functions import SpeechScraper


linkdir = 'ADD/INPUT/PATH/HERE'
dt=str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

#%% CZ
SpeechScraper(file='CZ_cz20200506-162929.csv', 
              linkdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/CompleteLinks/"), 
              speechdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/Speeches/"), 
              xpath='/html/body//div[@class="detail"]/p',
              dt=dt)

SpeechScraper(file='CZ_en20200506-162929.csv', 
              linkdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/CompleteLinks/"), 
              speechdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/Speeches/"), 
              xpath='/html/body//div[@class="detail"]/p',
              dt=dt)

#%% DE
SpeechScraper(file='DE_de20200506-162929.csv', 
              linkdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/CompleteLinks/"), 
              speechdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/Speeches/"), 
              xpath='/html/body//div[@class="basepage_pages"]/p/text()',
              dt=dt)

SpeechScraper(file='DE_en20200506-162929.csv', 
              linkdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/CompleteLinks/"), 
              speechdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/Speeches/"), 
              xpath='/html/body//div[@class="basepage_pages"]/p/text()',
              dt=dt)

#%% DK
SpeechScraper(file='DK_dk20200506-162929.csv', 
              linkdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/CompleteLinks/"), 
              speechdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/Speeches/"), 
              xpath='/html/body//div[@class="maininner maininner-page"]/p[not(@class)]',
              dt=dt)

SpeechScraper(file='DK_en20200506-162929.csv', 
              linkdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/CompleteLinks/"), 
              speechdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/Speeches/"), 
              xpath='/html/body//div[@class="maininner maininner-page"]/p',
              dt=dt,
              regex='.*Check against delivery(.*)')

#%% EE
SpeechScraper(file='EE_ee20200506-162929.csv', 
              linkdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/CompleteLinks/"), 
              speechdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/Speeches/"), 
              xpath='/html/body//div[@class="field-item even"]/p/text()',
              dt=dt)

SpeechScraper(file='EE_en20200506-162929.csv', 
              linkdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/CompleteLinks/"), 
              speechdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/Speeches/"), 
              xpath='/html/body//div[@class="field-item even"]/p[1]/text()',
              dt=dt)

#%% FR
SpeechScraper(file='FR_fr20200506-162929.csv', 
              linkdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/CompleteLinks/"), 
              speechdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/Speeches/"), 
              xpath='/html/body//div[@class="discour--desc"]/span/p/text()',
              dt=dt,
              fr=True)

#%% IT (contains speeches in the senate and chamber)
SpeechScraper(file='IT_it20200506-162929.csv', 
              linkdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/CompleteLinks/"), 
              speechdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/Speeches/"), 
              xpath='/html/body//div[@class="body_intervista"]/p/text()',
              dt=dt)

#%% NL
SpeechScraper(file='NL_nl20200506-162929.csv', 
              linkdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/CompleteLinks/"), 
              speechdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/Speeches/"), 
              xpath='//div[@id="content"]/p[not(@class)]//text()',
              dt=dt)

SpeechScraper(file='NL_en20200506-162929.csv', 
              linkdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/CompleteLinks/"), 
              speechdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/Speeches/"), 
              xpath='//div[@id="content"]/p[not(@class)]//text()',
              dt=dt)

#%% NO
SpeechScraper(file='NO_en20200506-162929.csv', 
              linkdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/CompleteLinks/"), 
              speechdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/Speeches/"), 
              xpath='//div[@class="article-body"]/p[not(@style)]',
              dt=dt)

SpeechScraper(file='NO_no20200506-162929.csv', 
              linkdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/CompleteLinks/"), 
              speechdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/Speeches/"), 
              xpath='//div[@class="article-body"]/p[not(@style)]',
              dt=dt)

#%% SE
SpeechScraper(file='sweden06052020.csv', 
              linkdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/CompleteLinks/"), 
              speechdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/Speeches/"), 
              xpath='//div[@class="has-wordExplanation"]/p//text()',
              dt='20200506-172749')

#%% Britan
xpath = '//*[@id="content"]/div[3]/div[1]/div[1]/div[2]/div//text()'
i=0
mis=0
deadlinks=[]
country='Great Britain'


print('Fetching speeches...\n')

with open(str(path+'CompleteLinks/GB20200514.csv'), mode='r', encoding='utf-8') as fi:
    reader=csv.reader(fi)
    with open(str(path+'Speeches/GB'+dt+'.csv'), mode='w', encoding='utf-8') as fo:
        writer=csv.writer(fo)
        writer.writerow(['date', 'country', 'speaker', 'title', 'url', 'text'])
        # sort out non-speeches
        for row in reader:
            for attempt in range(3):
                try:
                    fetchlink = row[3]
                    req = request.Request(url = str(fetchlink), headers = headers)
                    tree = html.fromstring(request.urlopen(req).read().decode(encoding="utf-8"))
                except request.HTTPError:
                    print("Whoops, that went wrong, retrying page "+ fetchlink +" for "+ row[2] + " "+ row[3])
                    if attempt == 2:
                        print("Fetching page " + fetchlink +" for "+ row[2] + " "+ row[3] + " failed due to HTTPError")
                        deadlinks.append(fetchlink)
                        mis += 1
                        continue
                    time.sleep(5)
                except request.URLError:
                    print("Whoops, that went wrong, retrying page "+ fetchlink +" for "+ row[2] + " "+ row[3])
                    if attempt == 2:
                        print("Fetching page " + fetchlink +" for "+ row[2] + " "+ row[3] + " failed due to URLError")
                        deadlinks.append(fetchlink)
                        mis += 1
                        continue
                    time.sleep(5)
                except:
                    print("Whoops, that went wrong, retrying page "+ fetchlink +" for "+ row[2] + " "+ row[3])
                    if attempt == 2:
                        print("Fetching page " + fetchlink +" for "+ row[2] + " "+ row[3] + " failed due to Unknown Error")
                        deadlinks.append(fetchlink)
                        mis += 1
                        continue
                    time.sleep(5)
            cats = str(tree.xpath('//*[@id="content"]/div[3]/div[1]/div[1]/div[1]/dl/dd/text()'))
            if re.match('.*(Transcript of the speech, exactly as it was delivered).*', cats):
                txt = tree.xpath(xpath)
                txtstr = ''
                for t in txt:
                    txtstr += t + ' '
                cleantxt = re.sub("\r|\n|\t|\\xa0|\* \* \*"," ",txtstr.lstrip())
                writer.writerow([row[0],country,row[1],row[2],row[3],cleantxt])
                i+=1
                print('\tCollected {} speech(es)...\r'.format(i))
print('Finished collecting {} speeches.'.format(i))


