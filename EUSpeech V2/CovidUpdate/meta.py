# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 15:01:24 2019

@author: samunico
"""

#%% import
import csv
import os

speechdir = 'PATH/TO/SPEECHES'

#%% write metafile

print('Write metafile...', end = '\r')

# define header
speaker   = 'speaker'
country = 'country'
count   = 'n_speeches'
startdate = 'startdate'
enddate   = 'enddate'
t = 0

with open(speechdir+"/speechesCovidUpdate_20200511.csv", mode="r",encoding="utf-8") as fi: # Change to correct directory before importing
    reader = csv.reader(fi,delimiter=",")
    next(reader)
    with open(speechdir+"/meta_new.csv", mode = 'w', encoding = 'utf-8') as fo:
        writer = csv.writer(fo, lineterminator = '\n')
        for row in reader:
            # currently starts new count for every change in language -> should only be two lines in file!
            if speaker != row[2]: 
                writer.writerow([speaker, country, count, startdate, enddate])
                startdate = row[0]
                count = 0
            else:
                count +=1
            t += 1
            speaker   = row[2]
            country   = row[1]
            enddate   = row[0]
        writer.writerow([speaker, country, count, startdate, enddate])

print('Finished ({} speeches in total), congratulations!\n'.format(str(t)))
