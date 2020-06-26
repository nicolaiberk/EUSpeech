"""
Nicolai Berk
time taken to run - approx 
"""

# from nltk import wordpunct_tokenize
# from nltk.corpus import stopwords
import csv
from langdetect import detect
from langdetect import detect_langs
# from collections import Counter
import re
import sys
import csv

csv.field_size_limit(sys.maxsize)

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

#%% 
# def _calculate_languages_ratios(text):
#     languages_ratios = {}
#     tokens = wordpunct_tokenize(text)
#     words = [word.lower() for word in tokens]
#     for language in stopwords.fileids():
#         stopwords_set = set(stopwords.words(language))
#         words_set = set(words)
#         common_elements = words_set.intersection(stopwords_set)

#         languages_ratios[language] = len(common_elements) # language "score"
#     return languages_ratios
# #----------------------------------------------------------------------
# def detect_language(text):
#     ratios = _calculate_languages_ratios(text)
#     most_rated_language = max(ratios, key=ratios.get)
#     return most_rated_language
# #----------------------------------------------------------------------
# def detectenglishspeeches(path,inputcsv,outputcsv):
#     completelinks=[]
#     date=[]
#     speaker=[]
#     country=[]
#     language=[]
#     title=[]
#     fulltext=[]
#     nooflanguages=[]
#     langdetect=[]
#     langprobdetect=[]
#     nooflang=[]
#     lenspeech=[]
#     lenspeech2=[]
#     origtext=[]
    
#     sno=0
#     with open(""+path+inputcsv+".csv",mode="r",encoding="utf-8") as fi:
#         reader=csv.reader(fi,delimiter=",")
#         for row in reader:
#             date.append(row[0])
#             country.append(row[1])
#             speaker.append(row[2])
#             language.append(row[3])
#             title.append(row[4])
#             completelinks.append(row[5])
#             origtext.append(row[6])
#             fulltext.append(row[7])
#             langdetect.append(row[8])
#             langprobdetect.append(row[9])
#             nooflang.append(row[10])
#             lenspeech.append(row[11])
#             lenspeech2.append(row[12])
#             sno=sno+1

#     sno=-1
#     secondcheck=[]
#     secondchecklang=[]
#     firstlanguage=[]
#     secondlanguage=[]
#     for word in langdetect:
#         sno=sno+1
#         q = int(nooflang[sno])
#         if word=="en":
#             firstlanguage.append("en")
#             #print(word, "in english")
#             if q == 1:  
#                 ratio = _calculate_languages_ratios(fulltext[sno])
#                 ratio2 = dict(Counter(ratio).most_common(2))
#                 l=[]
#                 [l.extend([k,v]) for k,v in ratio2.items()]
#                 if abs(l[1]-l[3])<50 and int(l[1])>25 and int(l[3])>25:
#                     nooflang[sno]="2"
#                     if (l[2] == "english"):                   
#                         secondlanguage.append(str(l[0]))
#                     elif (l[0] == "english"):
#                         secondlanguage.append(str(l[2]))
#                 else:
#                     secondlanguage.append("none")
#             else:
#                 z = langprobdetect[sno].split()
#                 y = z[1]
#                 t = y[:2]
#                 secondlanguage.append(t)
#         else:
#             #print(word, "in other")
#             firstlanguage.append(word)
#             if q == 1:   
#                 secondlanguage.append("none")
#             else:
#                 z = langprobdetect[sno].split()
#                 y = z[1]
#                 t = y[:2]
#                 secondlanguage.append(t)

    
#     sno=0
#     for word in secondlanguage:
#         if word == "french":
#             secondlanguage[sno]= "fr"
#         elif word == "german":
#             secondlanguage[sno]= "de"
#         elif word == "italian":
#             secondlanguage[sno]= "it"
#         elif word == "spanish":
#             secondlanguage[sno] = "es"
#         elif word == "dutch":
#             secondlanguage[sno] = "nl"
#         sno=sno+1
            
#     output= zip(date,country,speaker,title,completelinks,origtext,fulltext,langprobdetect,lenspeech, lenspeech2,nooflang, firstlanguage, secondlanguage)        
#     with open(""+path+outputcsv+".csv",mode="w",encoding="utf-8") as fo:
#         writer=csv.writer(fo)
#         writer.writerows(output)

#     print("Done",outputcsv)
