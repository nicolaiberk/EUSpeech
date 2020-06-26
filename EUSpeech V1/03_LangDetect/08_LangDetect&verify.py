"""
tanushree goyal
time taken to run - approx 57 mins for 16,524 speeches
"""

import sys
try:
    from nltk import wordpunct_tokenize
    from nltk.corpus import stopwords
    import csv
    from langdetect import detect
    from langdetect import detect_langs
    from collections import Counter
    import timeit
    import re
except ImportError:
    print("[!] You need to install some packages")

#----------------------------------------------------------------------    
def langdetectspeeches(path,inputcsv,outputcsv):
    completelinks=[]
    date=[]
    speaker=[]
    country=[]
    language=[]
    title=[]
    fulltext=[]
    x=[]
    y=[]
    origtext=[]
    nooflanguages=[]
    lenspeech=[]
    lenspeech2=[]
    with open(""+path+inputcsv+".csv",mode="r",encoding="utf-8") as fi:
        reader=csv.reader(fi,delimiter=",")
        for row in reader:
            date.append(row[0])
            country.append(row[1])
            speaker.append(row[2])
            language.append(row[3])
            title.append(row[4])
            completelinks.append(row[5])
            fulltext.append(row[6])
            origtext.append(row[6])
    

    sno=0  
    checkspeech=[]
    for i in fulltext:
        raw = i.lower() 
        raw = re.sub(r'\b-\b|\b/\b', '', raw) #concatenate hyphenated words
        raw = re.sub(r'<p>|</p>', '', raw) #remove p-tags  
        raw = re.sub(r'\W+|\d+',' ', raw) #remove non-words       
        fulltext[sno]=raw
        sno=sno+1
        lenspeech.append(len(raw.split()))
        lenspeech2.append(len(raw))
        #jprint("words  in - ",sno,"are : ",len(raw.split()))
        if(len(raw)<200 or raw.strip()==""):
            checkspeech.append("0")
        else:
            checkspeech.append("1")

    sno=0   
    for word in fulltext:
        if(word=="404" or word.strip()==""):
            y.append("no lang")    
            x.append("no lang")  
        else:
           y.append(detect(word))
           x.append(detect_langs(word))
        #print(sno) 
        sno=sno+1
    for word in x:
        nooflanguages.append(len(word))

    output= zip(date,country,speaker,language,title,completelinks,origtext,fulltext,y,x,nooflanguages,lenspeech,lenspeech2,checkspeech)        
    with open(""+path+outputcsv+"_1.csv",mode="w",encoding="utf-8") as fo:
        writer=csv.writer(fo)
        writer.writerows(output)

    inputobj = open(""+path+outputcsv+"_1.csv", 'r',encoding = 'utf-8')
    outputobj = open(""+path+outputcsv+".csv", 'w',encoding = 'utf-8')
    writer = csv.writer(outputobj)
    for row in csv.reader(inputobj):
        if row[13] != "0":
            del row[13]
            writer.writerow(row)

    inputobj.close()
    outputobj.close()

    print("Done")

#----------------------------------------------------------------------
def _calculate_languages_ratios(text):
    languages_ratios = {}
    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        languages_ratios[language] = len(common_elements) # language "score"
    return languages_ratios
#----------------------------------------------------------------------
def detect_language(text):
    ratios = _calculate_languages_ratios(text)
    most_rated_language = max(ratios, key=ratios.get)
    return most_rated_language
#----------------------------------------------------------------------
def detectenglishspeeches(path,inputcsv,outputcsv):
    completelinks=[]
    date=[]
    speaker=[]
    country=[]
    language=[]
    title=[]
    fulltext=[]
    nooflanguages=[]
    langdetect=[]
    langprobdetect=[]
    nooflang=[]
    lenspeech=[]
    lenspeech2=[]
    origtext=[]
    
    sno=0
    with open(""+path+inputcsv+".csv",mode="r",encoding="utf-8") as fi:
        reader=csv.reader(fi,delimiter=",")
        for row in reader:
            date.append(row[0])
            country.append(row[1])
            speaker.append(row[2])
            language.append(row[3])
            title.append(row[4])
            completelinks.append(row[5])
            origtext.append(row[6])
            fulltext.append(row[7])
            langdetect.append(row[8])
            langprobdetect.append(row[9])
            nooflang.append(row[10])
            lenspeech.append(row[11])
            lenspeech2.append(row[12])
            sno=sno+1

    sno=-1
    secondcheck=[]
    secondchecklang=[]
    for word in langdetect:
        sno=sno+1
        if word=="en" and nooflang[sno]=="1":
           ratio = _calculate_languages_ratios(fulltext[sno])
           ratio2 = dict(Counter(ratio).most_common(2))
           l=[]
           [l.extend([k,v]) for k,v in ratio2.items()]
           if abs(l[1]-l[3])<50 and int(l[1])>25 and int(l[3])>25:
               secondcheck.append("1")
               if (l[2] == "english"):
                   secondchecklang.append(str(l[0]))
               elif (l[0] == "english"):
                   secondchecklang.append(str(l[2]))
           else:
               secondcheck.append("0")
               secondchecklang.append("Fine english speeches")
        else:
            secondcheck.append("2")
            secondchecklang.append("Other language speeches")

    output= zip(date,country,speaker,language,title,completelinks,origtext,fulltext,langdetect,langprobdetect,nooflang,lenspeech, lenspeech2,secondcheck,secondchecklang)        
    with open(""+path+outputcsv+".csv",mode="w",encoding="utf-8") as fo:
        writer=csv.writer(fo)
        writer.writerows(output)

    print("Done",outputcsv)
#%%
#calling the function for each of the csvs
path="/Users/TanushreeGoyal/Desktop/Project Horizon 2020/Speeches_Final/Speeches_Final/original/"
inputlist = ["SpeechesIMF","SpeechesIT","SpeechesNL","SpeechesALDE","SpeechesCZ","SpeechesDE","SpeechesEC","SpeechesECB","SpeechesECR","SpeechesEP", "SpeechesEUCouncilPDF", "SpeechesFR","SpeechesGR", "SpeechesGRWB","SpeechesPO", "SpeechesPL", "SpeechesPOPDF", "SpeechesUK", "SpeechesUKWB", "SpeechesSP"]
outputlist = ["processed/SpeechesIMF","processed/SpeechesIT","processed/SpeechesNL","processed/SpeechesALDE","processed/SpeechesCZ","processed/SpeechesDE","processed/SpeechesEC","processed/SpeechesECB","processed/SpeechesECR","processed/SpeechesEP", "processed/SpeechesEUCouncilPDF", "processed/SpeechesFR","processed/SpeechesGR", "processed/SpeechesGRWB","processed/SpeechesPO", "processed/SpeechesPL", "processed/SpeechesPOPDF", "processed/SpeechesUK", "processed/SpeechesUKWB", "processed/SpeechesSP"]
print("hello")
i=0
for i in range(0,20):
    print("iteration",i)
    langdetectspeeches(path,inputlist[i],outputlist[i])
    i=i+1
    print("Done",i)
#%%
inputlist = ["processed/SpeechesIMF","processed/SpeechesIT","processed/SpeechesNL","processed/SpeechesALDE","processed/SpeechesCZ","processed/SpeechesDE","processed/SpeechesEC","processed/SpeechesECB","processed/SpeechesECR","processed/SpeechesEP", "processed/SpeechesEUCouncilPDF", "processed/SpeechesFR","processed/SpeechesGR", "processed/SpeechesGRWB","processed/SpeechesPO", "processed/SpeechesPL", "processed/SpeechesPOPDF", "processed/SpeechesUK", "processed/SpeechesUKWB","processed/SpeechesSP"]
outputlist = ["processed2/SpeechesIMF","processed2/SpeechesIT","processed2/SpeechesNL","processed2/SpeechesALDE","processed2/SpeechesCZ","processed2/SpeechesDE","processed2/SpeechesEC","processed2/SpeechesECB","processed2/SpeechesECR","processed2/SpeechesEP", "processed2/SpeechesEUCouncilPDF", "processed2/SpeechesFR","processed2/SpeechesGR", "processed2/SpeechesGRWB","processed2/SpeechesPO", "processed2/SpeechesPL", "processed2/SpeechesPOPDF", "processed2/SpeechesUK", "processed2/SpeechesUKWB", "processed2/SpeechesSP"]
i=0
for i in range(0,20):
    detectenglishspeeches(path,inputlist[i],outputlist[i])
    i=i+1
#%%
path="/Users/TanushreeGoyal/Desktop/Project Horizon 2020/Speeches_Final/Speeches_Final/original/"
inputcsv="SpeechesALDE"
outputcsv="processed/SpeechesALDE"
langdetectspeeches(path,inputcsv,outputcsv)
#%%
detectenglishspeeches(path,"processed/SpeechesALDE","processed/SpeechesALDE2")
