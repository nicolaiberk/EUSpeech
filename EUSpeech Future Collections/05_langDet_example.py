from functions import langdetectspeeches
import os
basedir = os.getcwd()

inputcsv=basedir+"/speeches/speeches"
outputcsv=basedir+"/speeches/speeches_LangDet"

langdetectspeeches(inputcsv,
                   outputcsv)
