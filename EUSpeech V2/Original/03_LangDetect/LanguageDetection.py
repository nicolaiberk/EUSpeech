"""
Nicolai Berk
time taken to run - approx # for # speeches
"""


import os

path=os.path.expanduser("~/Documents/Gijs/EUSpeech2/")
os.chdir(path)

from functions import langdetectspeeches

#%% run language detection

inputcsv="data/input/speeches_20200414_1621"
outputcsv="data/output/speeches2019_LangDet_new"
output= ["date",
         "country",
         "speaker",
         "language",
         "title",
         "completelinks",
         "origtext",
         "fulltext",
         "lang",
         "lang_prob",
         "nooflanguages",
         "lenspeech",
         "lenspeech2",
         "checkspeech"]

langdetectspeeches(path,
                   inputcsv,
                   outputcsv,
                   n_tot=4000,
                   writeHeader=output)