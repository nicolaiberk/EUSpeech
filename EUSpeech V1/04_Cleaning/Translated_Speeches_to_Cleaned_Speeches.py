# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 11:17:30 2016

@author: hjms
"""

#%%
import re
import csv
from nltk.corpus import stopwords
from nltk import stem
from nltk.stem import SnowballStemmer


stop = stopwords.words('english')
porter = stem.porter.PorterStemmer()
#dropboxbase="/media/Games/DropboxNIX/Dropbox/Leader Speeches_ Project/Data/"
dropboxbase="/media/Games/DropboxNIX/Dropbox/Leader Speeches Project/Data/"
path=""+dropboxbase+"6_Translated_Speeches/csv/"
pathout=""+dropboxbase+"4_Cleaned_Speeches/Cleaned_Speeches/Translated/"

english = stopwords.words('english')
english_stemmer = SnowballStemmer('english')

custom=[]
with open(""+dropboxbase+"4_Cleaned_Speeches/Many_stop_words/many_stop_words/names.csv", mode="r", encoding="utf-8") as fi:
    reader = csv.reader(fi, delimiter = ",")
    next(reader)    
    for row in list(reader):
        custom.append(row[1])

#%%
def clean_Speeches_(path, inputcsv, outputcsv):
    
    date = []
    institution = []
    speaker = []
    title=[]
    transtext=[]
    orgtext=[]
    words_stemmed = []
    length=[]
    lang=[]
    with open(""+path+inputcsv+"", mode="r", encoding="utf-8") as fi:
        reader = csv.reader(fi, delimiter = ",")
        for row in list(reader):
            date.append(row[1])
            institution.append(row[2])
            speaker.append(row[3])
            title.append(row[0])
            orgtext.append(row[5])            
            transtext.append(row[6])
            length.append(row[4])

    for i in transtext:
        
        raw = i.lower() 
        raw = re.sub(r'\b-\b|\b/\b', '', raw) #concatenate hyphenated words
        raw = re.sub(r'<p>|</p>', '', raw)    #remove p-tags   
        raw = re.sub(r'\W+|\d+',' ', raw)     #remove non-words
        raw = raw.split()
        raw = [i for i in raw if not i in custom]

        stopped_tokens = []
        stopped_tokens = [i for i in raw if not i in english]
        stopped_tokens = [english_stemmer.stem(x) for x in stopped_tokens]
        words_stemmed.append(" ".join(stopped_tokens))
        lang.append("entr")    
    output= zip(title, date, institution, speaker, length, transtext, words_stemmed, orgtext, lang)
    with open(outputcsv,mode="w",encoding="utf-8") as fo:
        writer=csv.writer(fo)
        writer.writerows(output)
            
    print("Done",inputcsv)
    
#%%
#CHANGE PATH AND OUTPUTCSV AS REQUIRED

inputcsv="Speeches_ALDE_Translated.csv"
outputcsv=""+pathout+"Speeches_ALDE_Cleaned_Translated.csv"
clean_Speeches_(path,inputcsv,outputcsv)

inputcsv="Speeches_CZ_Translated.csv"
outputcsv=""+pathout+"Speeches_CZ_Cleaned_Translated.csv"
clean_Speeches_(path,inputcsv,outputcsv)

inputcsv="Speeches_DE_Translated.csv"
outputcsv=""+pathout+"Speeches_DE_Cleaned_Translated.csv"
clean_Speeches_(path,inputcsv,outputcsv)

inputcsv="Speeches_EC_Translated.csv"
outputcsv=""+pathout+"Speeches_EC_Cleaned_Translated.csv"
clean_Speeches_(path,inputcsv,outputcsv)

inputcsv="Speeches_ECB_Translated.csv"
outputcsv=""+pathout+"Speeches_ECB_Cleaned_Translated.csv"
clean_Speeches_(path,inputcsv,outputcsv)

inputcsv="Speeches_ECR_Translated.csv"
outputcsv=""+pathout+"Speeches_ECR_Cleaned_Translated.csv"
clean_Speeches_(path,inputcsv,outputcsv)

inputcsv="Speeches_EP_Translated.csv"
outputcsv=""+pathout+"Speeches_EP_Cleaned_Translated.csv"
clean_Speeches_(path,inputcsv,outputcsv)

inputcsv="Speeches_EUCouncil_Translated.csv"
outputcsv=""+pathout+"Speeches_EUCouncil_Cleaned_Translated.csv"
clean_Speeches_(path,inputcsv,outputcsv)

inputcsv="Speeches_FR_Translated.csv"
outputcsv=""+pathout+"Speeches_FR_Cleaned_Translated.csv"
clean_Speeches_(path,inputcsv,outputcsv)

inputcsv="Speeches_GR_Translated.csv"
outputcsv=""+pathout+"Speeches_GR_Cleaned_Translated.csv"
clean_Speeches_(path,inputcsv,outputcsv)

inputcsv="Speeches_IMF_Translated.csv"
outputcsv=""+pathout+"Speeches_IMF_Cleaned_Translated.csv"
clean_Speeches_(path,inputcsv,outputcsv)

inputcsv="Speeches_IT_Translated.csv"
outputcsv=""+pathout+"Speeches_IT_Cleaned_Translated.csv"
clean_Speeches_(path,inputcsv,outputcsv)

inputcsv="Speeches_NL_Translated.csv"
outputcsv=""+pathout+"Speeches_NL_Cleaned_Translated.csv"
clean_Speeches_(path,inputcsv,outputcsv)

inputcsv="Speeches_PL_Translated.csv"
outputcsv=""+pathout+"Speeches_PL_Cleaned_Translated.csv"
clean_Speeches_(path,inputcsv,outputcsv)

inputcsv="Speeches_PO_Translated.csv"
outputcsv=""+pathout+"Speeches_PO_Cleaned_Translated.csv"
clean_Speeches_(path,inputcsv,outputcsv)

inputcsv="Speeches_SP_Translated.csv"
outputcsv=""+pathout+"Speeches_SP_Cleaned_Translated.csv"
clean_Speeches_(path,inputcsv,outputcsv)

inputcsv="Speeches_UK_Translated.csv"
outputcsv=""+pathout+"Speeches_UK_Cleaned_Translated.csv"
clean_Speeches_(path,inputcsv,outputcsv)