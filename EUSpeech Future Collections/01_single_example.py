from functions import linkScraper

import os
linkdir=os.getcwd()+'/CompleteLinks/'

#%% NL (english)
linkScraper(file        = 'example_links', 
            path        = linkdir, 
            sender      = "M. Rutte", 
            url         = "https://www.government.nl/government/members-of-cabinet/mark-rutte/documents?type=Speech&page=1", 
            linkbase    = "https://www.government.nl", 
            xpathLinks  = '//*[@class="common results"]/a', 
            xpathTitles = '//*[@class="publication"]/h3', 
            xpathDates  = '//*[@class="meta"]', 
            regexDates  = ' *Speech \| (.*)', 
            strToDates  = "%d-%m-%Y")
