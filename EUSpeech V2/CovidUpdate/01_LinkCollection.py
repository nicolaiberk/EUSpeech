#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 12:08:27 2020

Updated Link Collection Leader Speeches III

@author: Nicolai Berk
"""

import os
os.chdir(os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate"))
from functions import linkScraper
import datetime

linkdir=os.path.expanduser("~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/CompleteLinks/")
dt=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

#%% NL (english)
linkScraper(file        = 'NL_en'+dt, 
            path        = linkdir,
            sender      = "M. Rutte", 
            url         = "https://www.government.nl/government/members-of-cabinet/mark-rutte/documents?type=Speech&page={}", 
            linkbase    = "https://www.government.nl", 
            maxpage     = 15, 
            npage       = 1,
            xpathLinks  = '//*[@class="common results"]/a', 
            xpathTitles = '//*[@class="publication"]/h3', 
            xpathDates  = '//*[@class="meta"]', 
            regexDates  = ' *Speech \| (.*)', 
            strToDates  = "%d-%m-%Y", 
            mindate     = "03/06/2019")

#%% NL (dutch)
linkScraper(file        = 'NL_nl'+dt, 
            path        = linkdir, 
            sender      = "M. Rutte", 
            url         = "https://www.rijksoverheid.nl/regering/bewindspersonen/mark-rutte/documenten?type=Toespraak&pagina={}", 
            linkbase    = "https://www.rijksoverheid.nl", 
            maxpage     = 8, 
            npage       = 1,
            xpathLinks  = '//*[@class="common results"]/a', 
            xpathTitles = '//*[@class="publication"]/h3', 
            xpathDates  = '//*[@class="meta"]', 
            regexDates  = ' *Toespraak \| (.*)', 
            strToDates  = "%d-%m-%Y", 
            mindate     = "03/06/2019")

#%% DE (english)
linkScraper(file        = 'DE_en'+dt, 
            path        = linkdir, 
            sender      = "A. Merkel", 
            url         = "https://www.bundeskanzlerin.de/bkin-en/news/864130!search?formState=eNptj8EOgjAMhl_F9MwBFA3ZTcU76tF4mKPgEthwKyohvLtFQ7h4-9t839-0h1wSnqQp0YPoIdnE0SoZU-FsDcK0VRUA2V8ahgAKqZBmNgZxgV22PTeI6g5XJhpZaiNJWzNSzr6YjtYBeJKOQISM2KLwSFP9o0XXTUNl1dc9_ltu65umVHOTUQgCliHwPYfeH55oaM-_lHbWvB0PAr5Hp6lkh3nKyCJHr1hUrXNsZbLkrmj4AJUjWvw&page={}", 
            linkbase    = "https://www.bundeskanzlerin.de", 
            maxpage     = 7, 
            npage       = 1,
            xpathLinks  = '/html/body/div[1]/div[1]/div[3]/div/div/div[1]/div/div/div[2]/div/ol/li[*]/h3/a', 
            xpathTitles = '/html/body/div[1]/div[1]/div[3]/div/div/div[1]/div/div/div[2]/div/ol/li[*]/h3/a', 
            xpathDates  = '/html/body/div[1]/div[1]/div[3]/div/div/div[1]/div/div/div[2]/div/ol/li[*]/p', 
            regexDates  = '(.*)', 
            strToDates  = "%b %d, %Y-",
            mindate     = "20/07/2019")

#%% DE (german)
linkScraper(file        = 'DE_de'+dt, 
            path        = linkdir, 
            sender      = "A. Merkel", 
            url         = "https://www.bundeskanzlerin.de/bkin-de/aktuelles/70298!search?formState=eNptj8EOgjAMhl_F9MwBSdS4G4p31KPxMEeHJLDhVlRCeHc7DXrx9rf5vr_pAIUkPEhTogcxwCpO1kkI2tkGhOnqOgKynzSOEWipkL7oEsQJNnl6bBHVFc4MtLKsjKTKmgA5-2B4vojAk3QUIjNWa4801d86dP001Fa95f2_ZdpcKsoqrjIKQUASAx906P3ujoa2_Eppf5q34SLgMzhtLXssMkZmBXrFouqcYyuXJXcl4wtfGVrH&page={}", 
            linkbase    = "https://www.bundeskanzlerin.de", 
            maxpage     = 59, 
            npage       = 1,
            xpathLinks  = '/html/body/div[1]/div[1]/div[3]/div/div/div[1]/div/div/div[2]/div/ol/li[*]/h3/a', 
            xpathTitles = '/html/body/div[1]/div[1]/div[3]/div/div/div[1]/div/div/div[2]/div/ol/li[*]/h3/a', 
            xpathDates  = '/html/body/div[1]/div[1]/div[3]/div/div/div[1]/div/div/div[2]/div/ol/li[*]/p', 
            regexDates  = '.*, (.*)-', 
            strToDates  = "%d. %B %Y",
            language    = "german",
            mindate     = "20/07/2019")

#%% CZ (english)
linkScraper(file        = 'CZ_en'+dt, 
            path        = linkdir, 
            sender      = "A. Babis", 
            url         = "https://www.vlada.cz/scripts/detail.php?pgid=1016&conn=10175&pg=&conn=10175&pg={}", 
            linkbase    = "http://www.vlada.cz", 
            maxpage     = 3, 
            npage       = 1,
            xpathLinks  = '//*[@class="record"]/h2/a', 
            xpathTitles = '//*[@class="record"]/h2/a', 
            xpathDates  = '//*[@class="info"]', 
            regexDates  = '(.*)', 
            strToDates  = "%d. %m. %Y",
            mindate     = "16/05/2019")

#%% CZ (czech)
linkScraper(file        = 'CZ_cz'+dt, 
            path        = linkdir, 
            sender      = "A. Babis", 
            url         = "https://www.vlada.cz/scripts/detail.php?pgid=1013&conn=10155&pg=&conn=10155&pg={}", 
            linkbase    = "https://www.vlada.cz", 
            maxpage     = 5, 
            npage       = 1,
            xpathLinks  = '//*[@class="record"]/h2/a', 
            xpathTitles = '//*[@class="record"]/h2/a', 
            xpathDates  = '//*[@class="info"]', 
            regexDates  = '(.*)', 
            strToDates  = "%d. %m. %Y",
            mindate     = "16/05/2019")

#%% FR (french)
linkScraper(file        = 'FR_fr'+dt, 
            path        = linkdir, 
            sender      = "E. Macron", 
            url         = "https://www.vie-publique.fr/recherche?search_api_fulltext=emmanuel%20macron&sort_by=field_update_date&f%5B0%5D=categories%3Adiscours&f%5B0%5D=categories%3Adiscours&page={}", 
            start       = 0,
            linkbase    = "", 
            maxpage     = 20, 
            npage       = 1,
            xpathLinks  = '/html/body//h2/a[@class="link-multiple"]', 
            xpathTitles = "/html/body//span[@class='field--name-title']", 
            xpathDates  = '/html/body//time[@class="datetime"]', 
            regexDates  = '(.*)', 
            strToDates  = "%d/%m/%Y",
            mindate     = "15/07/2019")

#%% Italy (italian)
linkScraper(file='IT_it'+dt, 
            path=linkdir, 
            sender="G. Conte", 
            url="http://www.governo.it/it/interventi?page={}", 
            linkbase="http://www.governo.it", 
            maxpage=8,
            xpathLinks="/html/body//a[h2]", 
            xpathTitles="/html/body//h2[@class='h4']", 
            xpathDates='/html/body//div[@class="h6 clearfix dataleft"]', 
            regexDates="(.*)", 
            strToDates="%d %B %Y", 
            language="italian",
            start=0)

#%% Denmark (EN)

# M. Frederiksen 2020
linkScraper(file='DK_en'+dt, 
            path=linkdir, 
            sender="M. Frederiksen", 
            url="http://www.stm.dk/index.dsp?page=11004&action=page_overview_search&l1_valg=3420&l2_valg=3440", 
            linkbase="http://www.stm.dk/", 
            xpathLinks="/html/body//div[@class = 'headline']/a", 
            xpathTitles="/html/body//div[@class = 'headline']/a", 
            xpathDates="/html/body//div[@class = 'headline']/span", 
            regexDates="(.*)", 
            strToDates=["%d.%m.%y","%d.%m.%Y"],
            fmt_url=False
            )

# M. Frederiksen 2019
linkScraper(file='DK_en'+dt, 
            path=linkdir, 
            sender="M. Frederiksen", 
            url="http://www.stm.dk/index.dsp?page=11004&action=page_overview_search&l1_valg=3420&l2_valg=3421", 
            linkbase="http://www.stm.dk/", 
            xpathLinks="/html/body//div[@class = 'headline']/a", 
            xpathTitles="/html/body//div[@class = 'headline']/a", 
            xpathDates="/html/body//div[@class = 'headline']/span", 
            regexDates="(.*)", 
            strToDates=["%d.%m.%y","%d.%m.%Y"],
            mindate = "26/06/2019",
            fmt_url=False
            )


# L. Rasmussen 2019
linkScraper(file='DK_en'+dt, 
            path=linkdir,
            sender="L. Rasmussen", 
            url="http://www.stm.dk/index.dsp?page=11004&action=page_overview_search&l1_valg=3175&l2_valg=3421", 
            linkbase="http://www.stm.dk/", 
            xpathLinks="/html/body//div[@class = 'headline']/a", 
            xpathTitles="/html/body//div[@class = 'headline']/a", 
            xpathDates="/html/body//div[@class = 'headline']/span", 
            regexDates="(.*)", 
            strToDates=["%d.%m.%y","%d.%m.%Y"],
            fmt_url=False            
            )

#%% Denmark (DK)

# M. Frederiksen 2020
linkScraper(file='DK_dk'+dt, 
            path=linkdir, 
            sender="M. Frederiksen", 
            url="http://www.stm.dk/index.dsp?page=7990&action=page_overview_search&l1_valg=3406&l2_valg=3433", 
            linkbase="http://www.stm.dk/", 
            xpathLinks="/html/body//div[@class = 'headline']/a", 
            xpathTitles="/html/body//div[@class = 'headline']/a", 
            xpathDates="/html/body//div[@class = 'headline']/span", 
            regexDates="(.*)", 
            strToDates=["%d.%m.%y","%d.%m.%Y"],
            fmt_url=False
            )

# M. Frederiksen 2019
linkScraper(file='DK_dk'+dt, 
            path=linkdir, 
            sender="M. Frederiksen", 
            url="http://www.stm.dk/index.dsp?page=7990&action=page_overview_search&l1_valg=3406&l2_valg=3413", 
            linkbase="http://www.stm.dk/", 
            xpathLinks="/html/body//div[@class = 'headline']/a", 
            xpathTitles="/html/body//div[@class = 'headline']/a", 
            xpathDates="/html/body//div[@class = 'headline']/span", 
            regexDates="(.*)", 
            strToDates=["%d.%m.%y","%d.%m.%Y"],
            mindate = "26/06/2019",
            fmt_url=False
            )


# L. Rasmussen 2019
linkScraper(file='DK_dk'+dt, 
            path=linkdir, 
            sender="L. Rasmussen", 
            url="http://www.stm.dk/index.dsp?page=7990&action=page_overview_search&l1_valg=3168&l2_valg=3413", 
            linkbase="http://www.stm.dk/", 
            xpathLinks="/html/body//div[@class = 'headline']/a", 
            xpathTitles="/html/body//div[@class = 'headline']/a", 
            xpathDates="/html/body//div[@class = 'headline']/span", 
            regexDates="(.*)", 
            strToDates=["%d.%m.%y","%d.%m.%Y"],
            fmt_url=False
            )


#%% NO english
linkScraper(file='NO_en'+dt, 
            path=linkdir, 
            sender="E. Solberg", 
            url="https://www.regjeringen.no/en/whatsnew/speeches_articles/id1334/?ownerid=875&page={}",
            linkbase='https://www.regjeringen.no',
            xpathLinks='//*[@id="searchResultsListing"]/li[*]/h2/a', 
            xpathTitles='//*[@id="searchResultsListing"]/li[*]/h2/a',
            xpathDates='//*[@id="searchResultsListing"]/li[*]/div/span[1]', 
            regexDates='(.*)', 
            strToDates='%d/%m/%Y',
            maxpage=12,
            mindate='05/07/2019')

#%% NO norwegian
linkScraper(file='NO_no'+dt, 
            path=linkdir, 
            sender="E. Solberg", 
            url="https://www.regjeringen.no/no/aktuelt/taler_artikler/id1334/?ownerid=875&page={}",
            linkbase='https://www.regjeringen.no',
            xpathLinks='//*[@id="searchResultsListing"]/li[*]/h2/a', 
            xpathTitles='//*[@id="searchResultsListing"]/li[*]/h2/a',
            xpathDates='//*[@id="searchResultsListing"]/li[*]/div/span[1]', 
            regexDates='(.*)', 
            strToDates='%d.%m.%Y',
            maxpage=30,
            mindate='05/07/2019')

#%% EE english
linkScraper(file='EE_en'+dt, 
            path=linkdir, 
            sender='J.Ratas', 
            url='https://www.valitsus.ee/en/news?title=&title_op=allwords&source=23&date=All&date_custom%5Bmin%5D=&date_custom%5Bmax%5D=&field_news_subject_tid_i18n=139&page={}', 
            linkbase="https://www.valitsus.ee", 
            xpathLinks='//*[@id="block-system-main"]/div/div/div/div[1]/div[*]/div[2]/h2/a', 
            xpathTitles='//*[@id="block-system-main"]/div/div/div/div[1]/div[*]/div[2]/h2/a', 
            xpathDates='//*[@id="block-system-main"]/div/div/div/div[1]/div[*]/div[2]/div[1]', 
            regexDates='(.*)', 
            strToDates='%d.%m.%Y', 
            start=0,
            maxpage=4,
            mindate='26/02/2019')

#%% EE estonian
linkScraper(file='EE_ee'+dt, 
            path=linkdir, 
            sender='J.Ratas', 
            url='https://www.valitsus.ee/et/uudised?title=&title_op=allwords&source=23&date=All&date_custom%5Bmin%5D=&date_custom%5Bmax%5D=&field_news_subject_tid_i18n=139&page={}', 
            linkbase="https://www.valitsus.ee", 
            xpathLinks='//*[@id="block-system-main"]/div/div/div/div[1]/div[*]/div[2]/h2/a', 
            xpathTitles='//*[@id="block-system-main"]/div/div/div/div[1]/div[*]/div[2]/h2/a', 
            xpathDates='//*[@id="block-system-main"]/div/div/div/div[1]/div[*]/div[2]/div[1]', 
            regexDates='(.*)', 
            strToDates='%d.%m.%Y', 
            start=0,
            maxpage=7,
            mindate='26/02/2019')

#%% Linkcollection Boris Johnson
linkScraper(str('GB'+dt), 
            str(path+'CompleteLinks/'), 
            sender='B. Johnson', 
            url='https://www.gov.uk/search/news-and-communications?order=updated-newest&page={}&people%5B%5D=boris-johnson', 
            linkbase='https://www.gov.uk', 
            xpathLinks='//*[@class="gem-c-document-list__item  "]/a', 
            xpathTitles='//*[@class="gem-c-document-list__item  "]/a', 
            xpathDates='//*[@class="gem-c-document-list__item  "]//time', 
            regexDates='(.*)', 
            strToDates='%d %B %Y', 
            mindate='24/07/2019',
            maxpage=35)

#%% Linkcollection Theresa May
linkScraper(str('GB'+dt), 
            str(path+'CompleteLinks/'), 
            sender='T. May', 
            url='https://www.gov.uk/search/news-and-communications?order=updated-newest&page={}&people%5B%5D=theresa-may&public_timestamp%5Bto%5D=24%2F7%2F2019', 
            linkbase='https://www.gov.uk', 
            xpathLinks='//*[@class="gem-c-document-list__item  "]/a', 
            xpathTitles='//*[@class="gem-c-document-list__item  "]/a', 
            xpathDates='//*[@class="gem-c-document-list__item  "]//time', 
            regexDates='(.*)', 
            strToDates='%d %B %Y',
            mindate='18/07/2019',
            maxpage=35)
            


