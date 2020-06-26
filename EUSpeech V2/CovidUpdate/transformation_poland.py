#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 16:43:58 2020

Processing polish data

@author: Nicolai Berk
"""

import csv
import os
from datetime import datetime as dt
import re

os.chdir(os.path.expanduser('~/Dropbox/Studium/Amsterdam/Gijs/CovidUpdate/Speeches'))

with open('speeches_20200506-172749.csv',mode='a') as fo:
    with open('poland.csv',mode='r') as fi:
        reader = csv.reader(fi)
        writer = csv.writer(fo)
        next(reader)
        for row in reader:
            date = dt.strftime(dt.strptime(row[1], ' %d %B %Y'), '%d-%m-%Y')
            text = re.sub("\r|\n|\t|\\xa0"," ",row[2].strip())
            writer.writerow([date,'A. Duda','NA','NA',text])
            
        print('Done')