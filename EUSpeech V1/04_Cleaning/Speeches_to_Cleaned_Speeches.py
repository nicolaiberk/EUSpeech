# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 11:17:30 2016

@author: hjms
"""

#%%
import re
import csv
import codecs
from nltk.corpus import stopwords
from nltk import stem
from nltk.stem import SnowballStemmer


stop = stopwords.words('english')
porter = stem.porter.PorterStemmer()
#dropboxbase="/media/Games/DropboxNIX/Dropbox/Leader Speeches Project/Data/"
dropboxbase="/media/Games/DropboxNIX/Dropbox/Leader Speeches Project/Data/"
path=""+dropboxbase+"3_Language_Detection_Speeches/Language detected & verified csvs/"
pathout=""+dropboxbase+"4_Cleaned_Speeches/Cleaned_Speeches/"

# PO and CZ stopword lists obtained from:
#https://github.com/trec-kba/many-stop-words/tree/master/many_stop_words
#https://sites.google.com/site/kevinbouge/stopwords-lists

#czech_list = codecs.open("C:/Users/gschuma1/Dropbox/Papers/Leader Speeches Project/Data/4_Cleaned_Speeches/Many_stop_words/many_stop_words/stopwords-cz.txt", "r", "utf-8")
czech_list = codecs.open(""+dropboxbase+"4_Cleaned_Speeches/Many_stop_words/many_stop_words/stopwords-cz.txt", "r", "utf-8")
czech = czech_list.readlines()
czech = [x.strip() for x in czech]

#polish_list = codecs.open("C:/Users/gschuma1/Dropbox/Papers/Leader Speeches Project/Data/4_Cleaned_Speeches/Many_stop_words/many_stop_words/stopwords-pl.txt", "r", "utf-8")
polish_list = codecs.open(""+dropboxbase+"4_Cleaned_Speeches/Many_stop_words/many_stop_words/stopwords-pl.txt", "r", "utf-8")
polish = polish_list.readlines()
polish = [x.strip() for x in polish]

#greek_list = codecs.open("C:/Users/gschuma1/Dropbox/Papers/Leader Speeches Project/Data/4_Cleaned_Speeches/Many_stop_words/many_stop_words/stopwords-el.txt", "r", "utf-8")
greek_list = codecs.open(""+dropboxbase+"4_Cleaned_Speeches/Many_stop_words/many_stop_words/stopwords-el.txt", "r", "utf-8")
greek = greek_list.readlines()
greek = [x.strip() for x in greek]
#%%

dutch = stopwords.words('dutch')
dutch_stemmer = SnowballStemmer('dutch')
english = stopwords.words('english')
english_stemmer = SnowballStemmer('english')
french = stopwords.words('french')
french_stemmer = SnowballStemmer('french')
german = stopwords.words('german')
german_stemmer = SnowballStemmer('german')
italian = stopwords.words('italian')
italian_stemmer = SnowballStemmer('italian')
portuguese = stopwords.words('portuguese')
portuguese_stemmer = SnowballStemmer('portuguese')
spanish = stopwords.words('spanish')
spanish_stemmer = SnowballStemmer('spanish')
#%%
custom=[]
with open(""+dropboxbase+"4_Cleaned_Speeches/Many_stop_words/many_stop_words/names.csv", mode="r", encoding="utf-8") as fi:
    reader = csv.reader(fi, delimiter = ",")
    next(reader)    
    for row in list(reader):
        custom.append(row[1])

#%%
def clean_speeches(path, inputcsv, outputcsv):
    
    date = []
    institution = []
    speaker = []
    title=[]
    fulltext=[]
    lang = []
    words_stemmed = []
    length=[]
    
    with open(""+path+inputcsv+"", mode="r", encoding="utf-8") as fi:
        reader = csv.reader(fi, delimiter = ",")
        for row in list(reader):
            if row[10] == "1": #Checking if total number of languages is not more than 1
                date.append(row[0])
                institution.append(row[1])
                speaker.append(row[2])
                title.append(row[3])
                fulltext.append(row[5])
                length.append(row[8])
                lang.append(row[11])
    
    for i,j in zip(fulltext, lang):
        
        raw = i.lower() 
        raw = re.sub(r'\b-\b|\b/\b', '', raw) #concatenate hyphenated words
        raw = re.sub(r'<p>|</p>', '', raw)    #remove p-tags   
        raw = re.sub(r'\W+|\d+',' ', raw)     #remove non-words
        raw = raw.split()
        raw = [i for i in raw if not i in custom]
    
        stopped_tokens = []
        
        if j.lower() == "cs":
            stopped_tokens = [i for i in raw if not i in czech]
        elif j.lower() == "nl":
            stopped_tokens = [i for i in raw if not i in dutch]
            stopped_tokens = [dutch_stemmer.stem(x) for x in stopped_tokens]
        elif j.lower() == "en":
            stopped_tokens = [i for i in raw if not i in english]
            stopped_tokens = [english_stemmer.stem(x) for x in stopped_tokens]
        elif j.lower() == "fr":
            stopped_tokens = [i for i in raw if not i in french]
            stopped_tokens = [french_stemmer.stem(x) for x in stopped_tokens]
        elif j.lower() == "de":
            stopped_tokens = [i for i in raw if not i in german]
            stopped_tokens = [german_stemmer.stem(x) for x in stopped_tokens]
        elif j.lower() == "el":
            stopped_tokens = [i for i in raw if not i in greek]        
        elif j.lower() == "it":
            stopped_tokens = [i for i in raw if not i in italian]
            stopped_tokens = [italian_stemmer.stem(x) for x in stopped_tokens]
        elif j.lower() == "pl":
            stopped_tokens = [i for i in raw if not i in polish]
        elif j.lower() == "pt":
            stopped_tokens = [i for i in raw if not i in portuguese]
            stopped_tokens = [portuguese_stemmer.stem(x) for x in stopped_tokens]
        elif j.lower() == "es":
            stopped_tokens = [i for i in raw if not i in spanish]
            stopped_tokens = [spanish_stemmer.stem(x) for x in stopped_tokens]             
        words_stemmed.append(" ".join(stopped_tokens))
            
    output= zip(title, date, institution, speaker, length, fulltext, words_stemmed, lang)
    with open(outputcsv,mode="w",encoding="utf-8") as fo:
        writer=csv.writer(fo)
        writer.writerows(output)
            
    print("Done",inputcsv)
        
#%%
def merge_files(path,inputcsv1,inputcsv2,outputcsv):
    date = []
    institution = []
    speaker = []
    title=[]
    fulltext=[]
    lang = []
    words_stemmed = []
    length=[]

    with open(inputcsv1, mode="r", encoding="utf-8") as fi:
        reader = csv.reader(fi, delimiter = ",")
        for row in list(reader):
            title.append(row[0])
            date.append(row[1])
            institution.append(row[2])            
            speaker.append(row[3])
            length.append(row[4])            
            fulltext.append(row[5])
            words_stemmed.append(row[6])
            lang.append(row[7])
    with open(inputcsv2, mode="r", encoding="utf-8") as fi:
        reader = csv.reader(fi, delimiter = ",")
        for row in list(reader):
            title.append(row[0])
            date.append(row[1])
            institution.append(row[2])            
            speaker.append(row[3])
            length.append(row[4])            
            fulltext.append(row[5])
            words_stemmed.append(row[6])
            lang.append(row[7])
    output= zip(title, date, institution, speaker, length, fulltext, words_stemmed, lang)
    with open(outputcsv,mode="w",encoding="utf-8") as fo:
        writer=csv.writer(fo)
        writer.writerows(output)
#%%
#CHANGE PATH AND OUTPUTCSV AS REQUIRED

inputcsv="SpeechesALDE.csv"
outputcsv=""+pathout+"Speeches_ALDE_Cleaned.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv="SpeechesCZ.csv"
outputcsv=""+pathout+"Speeches_CZ_Cleaned.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv="SpeechesDE.csv"
outputcsv=""+pathout+"Speeches_DE_Cleaned.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv="SpeechesEC.csv"
outputcsv=""+pathout+"Speeches_EC_Cleaned.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv="SpeechesECB.csv"
outputcsv=""+pathout+"Speeches_ECB_Cleaned.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv="SpeechesECR.csv"
outputcsv=""+pathout+"Speeches_ECR_Cleaned.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv="SpeechesEP.csv"
outputcsv=""+pathout+"Speeches_EP_Cleaned.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv="SpeechesEUCouncil.csv"
outputcsv=""+pathout+"Speeches_EUCouncil_CleanedTemp.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv="SpeechesEUCouncilPDF.csv"
outputcsv=""+pathout+"Speeches_EUCouncilPDF_CleanedTemp.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv1=""+pathout+"Speeches_EUCouncil_CleanedTemp.csv"
inputcsv2=""+pathout+"Speeches_EUCouncilPDF_CleanedTemp.csv"
outputcsv=""+pathout+"Speeches_EUCouncil_Cleaned.csv"
merge_files(path,inputcsv1,inputcsv2,outputcsv)

inputcsv="SpeechesFR.csv"
outputcsv=""+pathout+"Speeches_FR_Cleaned.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv="SpeechesGR.csv"
outputcsv=""+pathout+"Speeches_GR_CleanedTemp.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv="SpeechesGRWB.csv"
outputcsv=""+pathout+"Speeches_GRWB_CleanedTemp.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv1=""+pathout+"Speeches_GR_CleanedTemp.csv"
inputcsv2=""+pathout+"Speeches_GRWB_CleanedTemp.csv"
outputcsv=""+pathout+"Speeches_GR_Cleaned.csv"
merge_files(path,inputcsv1,inputcsv2,outputcsv)

inputcsv="SpeechesIMF.csv"
outputcsv=""+pathout+"Speeches_IMF_Cleaned.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv="SpeechesIT.csv"
outputcsv=""+pathout+"Speeches_IT_Cleaned.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv="SpeechesNL.csv"
outputcsv=""+pathout+"Speeches_NL_Cleaned.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv="SpeechesPL.csv"
outputcsv=""+pathout+"Speeches_PL_Cleaned.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv="SpeechesPO.csv"
outputcsv=""+pathout+"Speeches_PO_CleanedTemp.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv="SpeechesPOPDF.csv"
outputcsv=""+pathout+"Speeches_POPDF_CleanedTemp.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv1=""+pathout+"Speeches_PO_CleanedTemp.csv"
inputcsv2=""+pathout+"Speeches_POPDF_CleanedTemp.csv"
outputcsv=""+pathout+"Speeches_PO_Cleaned.csv"
merge_files(path,inputcsv1,inputcsv2,outputcsv)

inputcsv="SpeechesSP.csv"
outputcsv=""+pathout+"Speeches_SP_Cleaned.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv="SpeechesUK.csv"
outputcsv=""+pathout+"Speeches_UK_CleanedTemp.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv="SpeechesUKWB.csv"
outputcsv=""+pathout+"Speeches_UKWB_CleanedTemp.csv"
clean_speeches(path,inputcsv,outputcsv)

inputcsv1=""+pathout+"Speeches_UK_CleanedTemp.csv"
inputcsv2=""+pathout+"Speeches_UKWB_CleanedTemp.csv"
outputcsv=""+pathout+"Speeches_UK_Cleaned.csv"
merge_files(path,inputcsv1,inputcsv2,outputcsv)
