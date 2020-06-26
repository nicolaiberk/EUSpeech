from functions import seleniumScraper

seleniumScraper(file = 'example_links',
                path = 'CompleteLinks/',
                sender = 'E. Macron',
                url = 'https://www.elysee.fr/toutes-les-actualites?categories%5B%5D=discours',       
                xpathLinks = '/html/body/main/article/section[{}]/div/div/a',
                xpathTitles = '/html/body/main/article/section[{}]/div/div/a/h2',
                xpathDates = '/html/body/main/article/section[{}]/div/div/p', 
                strToDates = '%d %B %Y',
                regexDates='(.*)', 
                mindate='01/03/2020',
                language="french",
                country='France',
                xpbutton = '//*[@id="main"]/section[2]/p/button',
                xpcookie = '//*[@id="tarteaucitronPersonalize"]',
                process     = 'button')
