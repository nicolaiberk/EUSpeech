"""
Nicolai Berk
time taken to run - approx 
"""

import csv
from langdetect import detect
from langdetect import detect_langs
import re
import sys
import csv
from lxml import html
from urllib import request
import time
from sys import stdout
csv.field_size_limit(sys.maxsize)



#%% link collection
def linkScraper(file,
                path,
                sender,    
                url,       
                linkbase,  
                xpathLinks,
                xpathTitles,
                xpathDates, 
                regexDates, 
                strToDates,
                mindate=None,
                maxdate=None,
                language="english",
                maxpage=0,   
                npage=1,     
                start=1,
                fmt_url=True,
                country=None
                ):
    
    '''
    scrapes links for subsequent collection from and writes them to a csv
    
    ----------------------------------------------------------------------------------
    
    Parameters:
    
    file        # str, name of output file 
    
    path        # str, output path
    
    sender      # str, sender
    
    url         # str, url that links should be collected from, input for format()
    
    
    linkbase    # str, linkbase that directed links should be appended to
    
    xpathLinks  # str, xpath to link elements
    
    xpathTitles # str, xpath to title elements
    
    xpathDates  # str, xpath to date elements
    
    regexDates  # str, regular expression to find date (matches first group)
    
    strToDates  # str, pattern for strptime, also accepts a list
    
    maxpage     # int, max number of pages that the scraper should go through when formatting url
    
    mindate     # str, earliest date to be scraped, formatted in %d/%m/%Y, if undefined everything will be scraped

    language    # str, language of date format, default is english. Supports german and italian.
    
    npage       # int, number to multiply by in case url formatting is not following pattern [0,1,2,3, ...]
    
    start       # int, first page number, if undefined start = 1
    
    '''




    
    # define time for filename
    # now = str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',}
    
    # open csvs we want to write to
    with open(path + file + '.csv', mode="a", encoding="utf-8") as fo:
        writer=csv.writer(fo, lineterminator='\n')
        with open(path + file + 'Deadpages.csv', mode="a", encoding="utf-8") as dl:
            dead_writer=csv.writer(dl, lineterminator='\n')
            
            print('\n\nFetching links ' + sender + '...')
            i = 0            
            n = start-1
            
            # loop through collection of pages
            
            while n <= maxpage:
                
                # define url
                n+=1
                if fmt_url == True:
                    fetchLink = url.format(n*npage)
                else:
                    fetchLink = url 
                
                
                for attempt in range(4):
                    try:
                        
                        # get page content
                        req = request.Request(fetchLink, headers = header)
                        tree = html.fromstring(request.urlopen(req).read().decode(encoding="utf-8",errors="ignore"))
                    
                        # identify relevant objects on the webpage
                        tempLinks   = tree.xpath(xpathLinks)
                        tempDates    = tree.xpath(xpathDates)
                        tempTitles   = tree.xpath(xpathTitles)
                        
                        if len(tempLinks) == len(tempDates) == len(tempTitles):
                            pass
                        else:
                            print("Error, Lists of links, dates, and titles are not same length!")
                            n=maxpage
                            break
                        
                        # bind link, sender, title, and date of a given release and write it into csv
                        for lk, dt, tt in zip(tempLinks, tempDates, tempTitles):
                            tt = "".join("".join("".join(tt.text.split("\n")).split("\r")).split("  "))
                            dt = "".join("".join("".join(dt.text.split("\n")).split("\r")).split("  "))
                            
                            try:
                                dt = re.match(regexDates, dt).group(1)
                            except AttributeError:
                                pass
    
                            if language != None:
                            
                                if language.lower() == "german":
                                    dt = dt.replace('Januar',    'January')
                                    dt = dt.replace('Februar',   'February')
                                    dt = dt.replace('März',      'March')
                                    dt = dt.replace('Mai',       'May')
                                    dt = dt.replace('Juni',      'June')
                                    dt = dt.replace('Juli',      'July')
                                    dt = dt.replace('Oktober',   'October')
                                    dt = dt.replace('Dezember',  'December')
                                    
                                elif language.lower() == "italian":
                                    dt = dt.replace('Gennaio',    'January')
                                    dt = dt.replace('Febbraio',   'February')
                                    dt = dt.replace('Marzo',      'March')
                                    dt = dt.replace('Aprile',     'April')
                                    dt = dt.replace('Maggio',     'May')
                                    dt = dt.replace('Giugno',     'June')
                                    dt = dt.replace('Luglio',     'July')
                                    dt = dt.replace('Agosto',     'August')
                                    dt = dt.replace('Settembre',  'September')
                                    dt = dt.replace('Ottobre',    'October')
                                    dt = dt.replace('Novembre',   'November')
                                    dt = dt.replace('Dicembre',   'December')
                                
                            elif language.lower() != 'english':                            
                                    print("Error: unknown date language specified. Choose german or italian. do not specify for english.")
                                
                            if type(strToDates) == list:
                                for s in strToDates:
                                    try:
                                        tmpdt = time.strptime(dt, s)
                                    except:
                                        pass
                            else:
                                tmpdt = time.strptime(dt, strToDates)
                            
                            if mindate != None:
                                if time.strptime(mindate, "%d/%m/%Y") > tmpdt:
                                    print("\n\tReached ", mindate, " (min), stopping process...")
                                    n=maxpage+1 #breaks iteration
                                    break
                            
                            if maxdate != None:
                                if time.strptime(maxdate, "%d/%m/%Y") < tmpdt:
                                    print("\n\tReached ", maxdate, " (max), skipping item...")
                                    continue                                    
                                    
                            date = time.strftime("%d-%m-%Y", tmpdt)
                            link = linkbase + lk.get('href')                            
                            
                            if country == None:
                                output = [date, sender, tt, link]
                            else:
                                output = [date, country, sender, tt, link]
                            writer.writerow(output)
                            dead_writer.writerow("0")
                            i += 1
                        break
                            
                        
                    # exceptions for errors
                    except request.HTTPError:
                        if attempt < 3:
                            print('\n\t\t attempt #' + str(attempt) + ' ' + fetchLink + '\n\t\tdid not work (HTTP Error), retrying...')
                            time.sleep(5)
                            continue
                        else:
                            dead_writer.writerow(fetchLink)
                            print('\n\t\tCollection failed due to HTTPError:\n\t\t' + fetchLink)
                            break
                    except request.URLError:
                        if attempt < 3:
                            print('\n\t\t attempt #' + str(attempt) + ' ' + fetchLink + '\n\t\tdid not work (URL Error), retrying...')
                            time.sleep(5)
                            continue
                        else:
                            dead_writer.writerow(fetchLink)
                            print('\n\t\tCollection failed due to URLError:\n\t\t' + fetchLink)
                            break
                    except Exception as e:
                        if attempt < 3:
                            print('\n\t\t attempt #' + str(i) + '/' + str(attempt) + ',/t' + fetchLink + '\n\t\tdid not work (', e, '), retrying...')
                            time.sleep(5)
                        else:
                            dead_writer.writerow(fetchLink)
                            print('\n\t\tCollection failed due to ', e,':\n\t\t' + fetchLink)
                            break

                # update progress bar
                if maxpage > 0:
                    bar = str('\t\t[' + '='*int((n + 1)/ (maxpage / 30)) + ' '*(30-int((n + 1) / (maxpage / 30))) + ']   ' + str((n + 1)) + '/' + str(maxpage))
                    stdout.write('%s\r' % bar)
                    stdout.flush()
                    
                
            # message when collection of one url is finished
            print(str('\nFinished collecting ' + str(i) + ' links for ' + sender))
            
#%% Speechscraper
def SpeechScraper(file, linkdir, speechdir, xpath, regex=0, dt="", fr=False):

    print('Start fetching speeches...\n')
    
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',}
    i=0
    mis=0
    skip=0
    
    deadlinks=[]
    
    with open(linkdir+file, mode="r",encoding="utf-8") as fi: # Change to correct directory before importing
        with open(speechdir+"speeches_"+dt+".csv", mode="a",encoding="utf-8") as fo: # Change to correct directory before importing
            reader = csv.reader(fi,delimiter=",")
            writer = csv.writer(fo, lineterminator = '\n')
            for row in reader:
                i+=1
                if len(row) == 4:
                    fetchlink = row[3]
                    title = row[2]
                    speaker= row[1]
                    
                elif len(row) == 5:
                    fetchlink = row[4]
                    title = row[3]
                    speaker = row[2]

                else:
                    print('InputError: Input format unknown, should be either [date,speaker,title,url] or [date,country,speaker,title,url]')
                    break

                print("\tFetching speech #", str(i+1), '... (', file , end = ")\r")
                for attempt in range(3):
                    try:
                        req = request.Request(url = fetchlink, headers = headers)
                        tree = html.fromstring(request.urlopen(req).read().decode(encoding="utf-8"))
                    except request.HTTPError:
                        print("Whoops, that went wrong, retrying page "+ fetchlink +" for "+ speaker + " "+ fetchlink)
                        if attempt == 2:
                            print("Fetching page " + fetchlink +" for "+ speaker + " "+ fetchlink + " failed due to HTTPError")
                            deadlinks.append(fetchlink)
                            mis += 1
                        time.sleep(5)
                    except request.URLError:
                        print("Whoops, that went wrong, retrying page "+ fetchlink +" for "+ speaker + " "+ fetchlink)
                        if attempt == 2:
                            print("Fetching page " + fetchlink +" for "+ speaker + " "+ fetchlink + " failed due to URLError")
                            deadlinks.append(fetchlink)
                            mis += 1
                        time.sleep(5)
                    except:
                        print("Whoops, that went wrong, retrying page "+ fetchlink +" for "+ speaker + " "+ fetchlink)
                        if attempt == 2:
                            print("Fetching page " + fetchlink +" for "+ speaker + " "+ fetchlink + " failed due to Unknown Error")
                            deadlinks.append(fetchlink)
                            mis += 1
                        time.sleep(5)
                            

                if fr==True and re.match('.*[Dd]éclaration.*', title) == None:
                    print('\n\nNot a speech, skipping\n\n')
                    skip+=1
                    continue
                else:
                    txt = tree.xpath(xpath)
           
                if txt == []:
                    print('\n\nNo speech found for\n\t', fetchlink, '\n\t using xpath: \n\n', xpath)
                    deadlinks.append(fetchlink)
                    mis += 1
                    continue
                    
                txtstr = ''
                
                try:
                    for t in txt:
                        if t.text != None:
                            txtstr += t.text + ' '
                except AttributeError:
                    for t in txt:
                        txtstr+=t+' '
                
                cleantxt = re.sub("\r|\n|\t|\\xa0|\* \* \*"," ",txtstr.lstrip())
                
                if regex != 0:
                    try:
                        cleantxt=str(re.match(regex, cleantxt).group(1))
                    except AttributeError:
                        pass
                
                cleantxt = "".join("".join("".join(cleantxt.split("\n")).split("\r")).split("  "))
                
                if len(cleantxt)<200:
                    print('\tVery short speech: ', str(row), '\n\tSKIPPING SPEECH')
                    deadlinks.append(fetchlink)
                    mis += 1
                    continue
                

                row.append(cleantxt)
                writer.writerow(row)
                # time.sleep(randint(1,3))
    
    
    with open(speechdir+"deadlinks_"+dt+".csv", mode="w",encoding="utf-8") as fo: # Change to correct directory before importing
        writer = csv.writer(fo, lineterminator = '\n')
        for dl in deadlinks:
            writer.writerow(dl)  
    
    print('Finished fetching {} speeches,'.format(str(i-skip)))
    print('collection of {} links failed,'.format(str(mis)))
    print('skipped {} links.'.format(str(skip)))
    



#%% language detection
def langdetectspeeches(path,inputcsv,outputcsv, n_tot=30000, readHeader = False, writeHeader = False):
    # detects language(s) of each speech, writes into output file
    
    
    completelinks=[]
    nooflanguages=[]
    lenspeech=[]
    lenspeech2=[]
    checkspeech=[]

    with open(path+inputcsv+".csv",mode="r",encoding="utf-8") as fi:
        reader=csv.reader(fi, delimiter = ',')
        if readHeader == True:
            next(reader) # skip header
        with open(path+outputcsv+".csv",mode="w",encoding="utf-8") as fo:
            writer=csv.writer(fo)
           
            if writeHeader != False:
                writer.writerow(writeHeader)
                
            print('Detecting Languages:')
            
            i=0
            for row in reader:
                i+=1
                
                date = row[0]
                country=row[1]
                speaker = row[2]
                title = row[3]
                completelinks = row[4]
                origtext = row[5]
                

                raw = origtext.lower() 
                raw = re.sub(r'\b-\b|\b/\b', '', raw) #concatenate hyphenated words
                raw = re.sub(r'<p>|</p>', '', raw) #remove p-tags  
                raw = re.sub(r'\W+|\d+',' ', raw) #remove non-words       
                fulltext=raw
                lenspeech = len(raw.split())
                lenspeech2 = len(raw)
                
                if(len(raw)<200 or raw.strip()==""):
                    checkspeech = "0"
                else:
                    checkspeech = "1"
                

                try:
                   lang = detect(fulltext)
                   lang_prob = detect_langs(fulltext)
                except:
                    lang = "no lang"  
                    lang_prob = "no lang"
                       
                nooflanguages = len(lang_prob)
                    
                output= [date,country,speaker,title,completelinks,origtext,lang,lang_prob,nooflanguages,lenspeech,lenspeech2,checkspeech]
                writer.writerow(output)
                
                # progress bar
                bar = str('\t[' + '='*int((i / int(n_tot/30))) + ' '*(30-int((i / int(n_tot/30)))) + ']  | ' + str(i) + ' of ' + str(n_tot))
                sys.stdout.write('%s\r' % bar)
                sys.stdout.flush()
                
            print("Done")
