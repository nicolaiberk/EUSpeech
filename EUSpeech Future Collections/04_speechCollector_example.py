from functions import speechScraper
from datetime import date
import os
linkdir = os.getcwd()+'/CompleteLinks/'

speechScraper(inputfile = 'example_links',
                linkdir = linkdir,
                speechdir = os.getcwd()+'/speeches/',
                xpath = '//div[@class="size3-2 reset-last-space ck-styled"]//* | //div[@class ="card"]//*',
                test_re = '.*[Dd]éclaration.*|.*[Aa]dresse.*|.*[Mm]essage')
