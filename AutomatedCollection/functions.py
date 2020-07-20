#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 5 10:46
Scraper Functions for Leader Speech Collection III
@author: Nicolai Berk
"""

from lxml import html
import requests
import time
from datetime import datetime
import csv
import re
from sys import stdout
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from langdetect import detect
from langdetect import detect_langs

csv.field_size_limit(sys.maxsize)


#%% function
def linkScraper(file,
                path,
                sender,
                url,       
                xpathLinks,
                xpathTitles,
                xpathDates, 
                strToDates,
                linkbase='',  
                regexDates='(.*)', 
                mindate=None,
                maxdate=None,
                language="english",
                maxpage=0,   
                npage=1,     
                start=1,
                country=None,
                mode='w'
                ):
    
    '''Scrapes links for subsequent collection from a website and writes them to a csv
    
    
    Parameters
    ----------
    file: string, name of output file 
    path: string, output path
    sender: string, speaker name
    url: string, url that links should be collected from, input for format()
    linkbase: string, linkbase that directed links should be appended to
    xpathLinks: string, xpath to link elements   
    xpathTitles: string, xpath to title elements
    xpathDates: string, xpath to date elements    
    regexDates: string, regular expression to find date (matches first group)
    strToDates: string or list, pattern for strptime (will try all of them if list)
    maxpage: integer, max number of pages that the scraper should go through when formatting url
    mindate: str, earliest date to be scraped, formatted in %d/%m/%Y, if undefined everything will be scraped
    language: string, language of date format, default is english. Supports german and italian.
    npage: integer, number to multiply by in case url formatting is not following pattern [0,1,2,3, ...]
    start: integer, first page number, if undefined start = 1
    country: string, country name, left out if not provided
    mode: string, 'w' for overwriting existing csvs, 'a' for adding to them
    
    Returns
    ------
    Writes a csv file [date, country, sender, tt, link] to the provided path.
    '''




    
    # open csvs we want to write to
    with open(path + file + '.csv', mode=mode, encoding="utf-8") as fo:
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
                fetchLink = url.format(n*npage)
                
                
                # update progress bar
                if maxpage > 0:
                    bar = str('\t\t[' + '='*int((n)/ (maxpage / 30)) + ' '*(30-int((n) / (maxpage / 30))) + ']   ' + str((n)) + '/' + str(maxpage))
                    stdout.write('%s\r' % bar)
                    stdout.flush()
                
                for attempt in range(4):
                    try:
                        
                        # get page content
                        req = requests.get(fetchLink)
                        tree = html.fromstring(req.text)
                    
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
                                dt = re.match(regexDates, dt).group(1).lower()
                            except AttributeError:
                                pass
                            
                            if language != None:
                            
                                if language.lower() == "german":
                                    dt = dt.replace('januar',    'January')
                                    dt = dt.replace('februar',   'February')
                                    dt = dt.replace('märz',      'March')
                                    dt = dt.replace('mai',       'May')
                                    dt = dt.replace('juni',      'June')
                                    dt = dt.replace('juli',      'July')
                                    dt = dt.replace('oktober',   'October')
                                    dt = dt.replace('dezember',  'December')
                                    
                                elif language.lower() == "italian":
                                    dt = dt.replace('gennaio',    'January')
                                    dt = dt.replace('febbraio',   'February')
                                    dt = dt.replace('marzo',      'March')
                                    dt = dt.replace('aprile',     'April')
                                    dt = dt.replace('maggio',     'May')
                                    dt = dt.replace('giugno',     'June')
                                    dt = dt.replace('luglio',     'July')
                                    dt = dt.replace('agosto',     'August')
                                    dt = dt.replace('settembre',  'September')
                                    dt = dt.replace('ottobre',    'October')
                                    dt = dt.replace('novembre',   'November')
                                    dt = dt.replace('dicembre',   'December')
                
                                elif language.lower() == 'french':
                                    dt = dt.replace('janvier',        'January')
                                    dt = dt.replace('février',        'February')
                                    dt = dt.replace('mars',           'March')
                                    dt = dt.replace('avril',          'April')
                                    dt = dt.replace('mai',            'May')
                                    dt = dt.replace('juin',           'June')
                                    dt = dt.replace('juillet',        'July')
                                    dt = dt.replace('août',           'August')
                                    dt = dt.replace('septembre',      'September')
                                    dt = dt.replace('octobre',        'October')
                                    dt = dt.replace('novembre',       'November')
                                    dt = dt.replace('décembre',       'December')

                                elif language.lower() != 'english':                            
                                        print("Error: unknown date language specified. Choose german, french or italian. do not specify for english.")
                                
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
                    except requests.HTTPError:
                        if attempt < 3:
                            print('\n\t\t attempt #' + str(attempt) + ' ' + fetchLink + '\n\t\tdid not work (HTTP Error), retrying...')
                            time.sleep(5)
                            continue
                        else:
                            dead_writer.writerow(fetchLink)
                            print('\n\t\tCollection failed due to HTTPError:\n\t\t' + fetchLink)
                            break
                    except Exception as e:
                        if attempt < 3:
                            print('\n\t\t attempt #' + str(i) + '/' + str(attempt) + ',/t' + fetchLink + '\n\t\tdid not work (', e, '), retrying...')
                            time.sleep(5)
                        else:
                            dead_writer.writerow(fetchLink)
                            print('\n\t\tCollection failed due to ', e,':\n\t\t' + fetchLink)
                            break
                    
                
            # message when collection of one url is finished
            print(str('\nFinished collecting ' + str(i) + ' links for ' + sender))
            
            
#%% Selenium scraper
def seleniumScraper(file,
                    path,
                    sender,
                    url,       
                    xpathLinks,
                    xpathTitles,
                    xpathDates, 
                    strToDates,
                    xpbutton=None,
                    linkbase='',
                    xpcookie = None,  
                    regexDates='(.*)', 
                    mindate=None,
                    maxdate=None,
                    language="english",
                    country=None,
                    mode='w',
                    process = 'scrolling'):


    # setup browser
    stdout.write('Setting up browser...\r')
    stdout.flush()
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(1)

    # click cookie
    if xpcookie != None:
        try:
            btcookie = driver.find_element_by_xpath(xpcookie)
        except:
            time.sleep(5)
            btcookie = driver.find_element_by_xpath(xpcookie)
        
        btcookie.click()
        time.sleep(1)


    with open(path+file+'.csv', mode=mode, encoding="utf-8") as fo:
        writer=csv.writer(fo, lineterminator = '\n')

        i = 1
        coll = 1
        skip = 0
        x = True
        
        print('Collecting links...\n')
        while x == True:
            for attempt in range(4):
                stdout.write(f'\t\tCollecting element #{i} using {process} process...\r')
                try:
                    tt = driver.find_element_by_xpath(xpathTitles.format(i)).text
                    dt = driver.find_element_by_xpath(xpathDates.format(i)).text
                    lk = driver.find_element_by_xpath(xpathLinks.format(i)).get_attribute('href')
                    break

                except NoSuchElementException:
                    
                    if attempt == 2:
                        
                        if process == 'button':
                            try:
                                btnext = driver.find_element_by_xpath(xpbutton)
                                btnext.click()
                                time.sleep(1)
                            except NoSuchElementException:
                                stdout.write('Button not found, trying again...\r')
                                stdout.flush()
                                btnext = driver.find_element_by_xpath(xpbutton)
                                btnext.click()
                                time.sleep(1)
                                
                        elif process == 'scrolling':
                            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                            time.sleep(1)

                        else:
                            print('Unknown process ("{}"), use "button" or "scrolling".'.format(process))
                        
                    if attempt == 3:
                        i +=1
                        skip +=1
                        
                        if skip == 5:
                            print('No more elements found. {} elements collected.'.format(coll))
                            driver.close()
                            sys.exit()
                    
                    else:
                        print(f'\n\t\tElement {i} not found, trying again...')
                        

            if linkbase != None:
                link = linkbase + lk
            else:
                link = lk
                
            try:
                dt = re.match(regexDates, dt).group(1).lower()
            except AttributeError:
                dt = dt.lower()

            if language != None:

                if language.lower() == "german":
                    dt = dt.replace('januar',    'January')
                    dt = dt.replace('februar',   'February')
                    dt = dt.replace('märz',      'March')
                    dt = dt.replace('mai',       'May')
                    dt = dt.replace('juni',      'June')
                    dt = dt.replace('juli',      'July')
                    dt = dt.replace('oktober',   'October')
                    dt = dt.replace('dezember',  'December')

                elif language.lower() == "italian":
                    dt = dt.replace('gennaio',    'January')
                    dt = dt.replace('febbraio',   'February')
                    dt = dt.replace('marzo',      'March')
                    dt = dt.replace('aprile',     'April')
                    dt = dt.replace('maggio',     'May')
                    dt = dt.replace('giugno',     'June')
                    dt = dt.replace('luglio',     'July')
                    dt = dt.replace('agosto',     'August')
                    dt = dt.replace('settembre',  'September')
                    dt = dt.replace('ottobre',    'October')
                    dt = dt.replace('novembre',   'November')
                    dt = dt.replace('dicembre',   'December')


                elif language.lower() == 'french':
                    dt = dt.replace('janvier',    'January')
                    dt = dt.replace('février',    'February')
                    dt = dt.replace('mars',       'March')
                    dt = dt.replace('avril',      'April')
                    dt = dt.replace('mai',        'May')
                    dt = dt.replace('juin',       'June')
                    dt = dt.replace('juillet',    'July')
                    dt = dt.replace('août',       'August')
                    dt = dt.replace('septembre',  'September')
                    dt = dt.replace('octobre',    'October')
                    dt = dt.replace('novembre',   'November')
                    dt = dt.replace('décembre',   'December')


            elif language.lower() != 'english':                            
                    print("Error: unknown language for transformation of months specified. Choose german, french or italian. do not specify for english.")


            if type(strToDates) == list:
                for s in strToDates:
                    try:
                        tmpdt = time.strptime(dt, s)
                    except:
                        pass
            else:
                tmpdt = time.strptime(dt, strToDates)

            date = time.strftime("%d-%m-%Y", tmpdt)

            if mindate != None:
                if time.strptime(mindate, "%d/%m/%Y") > tmpdt:
                    print(f"\n\tReached {mindate},  (min) stopping process after collection of {coll} elements.")
                    driver.close()
                    sys.exit()
                else:
                    pass

            if maxdate != None:
                if time.strptime(maxdate, "%d/%m/%Y") < tmpdt:
                    print("\n\tReached ", maxdate, " (max), skipping item...")
                    continue
                else:
                    pass


            if country == None:
                output = [date, sender, tt, link]
            else:
                output = [date, country, sender, tt, link]

            writer.writerow(output)
            coll += 1
            i += 1
            skip = 0




#%% Speechscraper
def speechScraper(inputfile, linkdir, speechdir, xpath, regex = 0, test_re = 0, mode = 'w', min_len = 200, timestamp = False):

    print('Start fetching speeches...\n')
    
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',}
    i=0
    mis=0
    skip=0
    if timestamp == True:
        now = '_'+time.strftime('%Y%m%d_%H%M%S', time.strptime(str(datetime.now())[0:19], '%Y-%m-%d %H:%M:%S'))
    elif timestamp == False:
        now = ''
    else:
        print("'timestamp' must be True or False")
        quit()
        
    deadlinks=[]
    
    with open(linkdir+inputfile+'.csv', mode="r",encoding="utf-8") as fi: # Change to correct directory before importing
        with open(speechdir+"speeches"+now+".csv", mode=mode,encoding="utf-8") as fo: # Change to correct directory before importing
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

                if test_re != 0 and re.match(test_re, title) == None:
                    print(f'\n\tNot a speech, skipping {i}')
                    skip+=1
                    continue
                else:
                    print("\tFetching speech #", str(i), '... (', inputfile , end = ")\r")
                for attempt in range(3):
                    try:
                        req = requests.get(fetchlink)
                        tree = html.fromstring(req.text)

                    except requests.exceptions.RequestException as e:
                        print("Whoops, that went wrong, retrying page "+ fetchlink +" for "+ speaker)
                        if attempt == 2:
                            print("Fetching page " + fetchlink +" for "+ speaker + " "+ fetchlink + " failed due to " + e)
                            deadlinks.append(fetchlink)
                            mis += 1
                        time.sleep(5)
                    except Exception as e:
                        print("Whoops, that went wrong, retrying page "+ fetchlink +" for "+ speaker)
                        if attempt == 2:
                            print("Fetching page " + fetchlink +" for "+ speaker + " failed due to: "+ e)
                            deadlinks.append(fetchlink)
                            mis += 1
                        time.sleep(5)
                            

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
                
#                 cleantxt = "".join("".join("".join(cleantxt.split("\n")).split("\r")).split("  "))
                
                if len(cleantxt) < min_len:
                    print('\tVery short speech: ', str(row), '\n\tSKIPPING SPEECH')
                    deadlinks.append(fetchlink)
                    mis += 1
                    continue
                

                row.append(cleantxt)
                writer.writerow(row)
                # time.sleep(randint(1,3))
    
    
    with open(speechdir+"deadlinks"+now+".csv", mode="w",encoding="utf-8") as fo: # Change to correct directory before importing
        writer = csv.writer(fo, lineterminator = '\n')
        for dl in deadlinks:
            writer.writerow(dl)  
    
    print('Finished fetching {} speeches,'.format(str(i-skip)))
    print('collection of {} links failed,'.format(str(mis)))
    print('skipped {} links.'.format(str(skip)))
    


#%% language detection
def langdetectspeeches(inputcsv,outputcsv, readHeader = False, mode = 'w', timestamp = False):
    with open(inputcsv+".csv",mode="r",encoding="utf-8") as fi:
        reader=csv.reader(fi, delimiter = ',')
        
        n_tot = sum(1 for row in reader)
        
        fi.seek(0) # this resets the file reader
        reader=csv.reader(fi, delimiter = ',')
        
        if timestamp == True:
            now = '_'+time.strftime('%Y%m%d_%H%M%S', time.strptime(str(datetime.now())[0:19], '%Y-%m-%d %H:%M:%S'))
        elif timestamp == False:
            now = ''
        else:
            print("'timestamp' must be True or False")
            quit()
        
        if readHeader == True:
            next(reader) # skip header
        with open(outputcsv+now+".csv",mode=mode,encoding="utf-8") as fo:
            writer=csv.writer(fo)
           
            writer.writerow(['date',
                            'country',
                            'speaker',
                             'title',
                             'url',
                             'origtext',
                             'lang',
                             'lang_prob',
                             'nooflanguages',
                             'lenspeech_w',
                             'lenspeech_char'])
                
            print('Detecting Languages:')
            
            i=0
            for row in reader:
                i+=1

                
                date = row[0]

                if len(row) == 5:
                    origtext = row[4]
                    completelinks = row[3]
                    title = row[2]
                    speaker= row[1]
                    country = 'Not defined'
                    
                elif len(row) == 6:
                    origtext = row[5]
                    completelinks = row[4]
                    title = row[3]
                    speaker = row[2]
                    country=row[1]
                

                raw = origtext.lower() 
                raw = re.sub(r'\b-\b|\b/\b', '', raw) #concatenate hyphenated words
                raw = re.sub(r'<p>|</p>', '', raw) #remove p-tags  
                raw = re.sub(r'\W+|\d+',' ', raw) #remove non-words       
                fulltext=raw
                lenspeech = len(raw.split())
                lenspeech2 = len(raw)
                

                try:
                   lang = detect(fulltext)
                   lang_prob = detect_langs(fulltext)
                except:
                    lang = "no lang"  
                    lang_prob = "no lang"
                       
                nooflanguages = len(lang_prob)
                    
                output= [date,country,speaker,title,completelinks,origtext,lang,lang_prob,nooflanguages,lenspeech,lenspeech2]
                writer.writerow(output)
                
                # progress bar
                bar = str('\t[' + '='*int((i+0.01 / (n_tot/30))) + ' '*(30-int(i / (n_tot/30))) + ']  | ' + str(i) + ' of ' + str(n_tot)+'   ')
                sys.stdout.write('%s\r' % bar)
                sys.stdout.flush()
                
            print("Done")
