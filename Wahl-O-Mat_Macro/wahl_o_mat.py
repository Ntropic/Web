# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 13:40:33 2017

@author: Michael Schilling
"""

import os
import time
import base64
import urllib

import codecs

from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
   
import re
import Speak_Up

import math
import matplotlib.pyplot as plt
import numpy as np

url_start='https://www.wahl-o-mat.de/bundestagswahl2017/'

## Start Selenium -------------------------------------------------------------
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome('C:\Chromedriver\chromedriver.exe',chrome_options=options)



driver.get(url_start)

#Erste Frage
driver.find_element_by_class_name('wom_begin').click()

Speak_Up.babel('Start answering questions now.')

condition=1
while condition:
    #Repeat
    time.sleep(0.5)
    site=driver.current_url
    test_url='www.wahl-o-mat.de/bundestagswahl2017/main_app.php?cb_themen=change&womres0bundestagswahl2017'
    if site.find(test_url)!=-1:
        	condition=0
            
Speak_Up.babel('Fetching the results for all parties.')    
party_list=driver.find_elements_by_css_selector('.wom_grayfilter.wom_grayfilter_edge.wom_grayfilter_over') 

how_often=int(math.ceil(len(party_list)/8.0))
ergebnis=[]
for i in range(0,how_often):
    party_list=driver.find_elements_by_css_selector('.wom_grayfilter.wom_grayfilter_edge.wom_grayfilter_over') 
    for j in range(0,8):
        party_list[j+i*8].click()
        
    time.sleep(0.5)
    next_page=driver.find_element_by_class_name('wom_next')
    next_page.click()
    
    ergebnis_elements=driver.find_elements_by_class_name('wom_ergebnis_partei')
    for j in range(0,8):
        ergebnis.append(ergebnis_elements[j].text)
    
    prev_page=driver.find_element_by_class_name('wom_previous')
    prev_page.click()
    
    party_list=driver.find_elements_by_css_selector('.wom_grayfilter.wom_grayfilter_edge.wom_grayfilter_over')
    for j in range(0,8):
        party_list[j+i*8].click()
        
party_names=[]
party_percent=[]
for i in range(0,len(ergebnis)):
    splitter=ergebnis[i].split('\n')
    splitter[1]=splitter[1][0:(len(splitter[1])-1)]
    splitter[1]=splitter[1].replace(',','.')
    party_names.append(splitter[0])
    party_percent.append(float(splitter[1]))
    
#Reorder
new=sorted((e,i) for i,e in enumerate(party_percent))
newer=np.int_(np.asarray(new))
newer=newer[:,1].tolist()

party_per=[]
party_nam=[]
for i in range(0,len(newer)):
    party_per.append(party_percent[newer[i]])
    party_nam.append(party_names[newer[i]])

ind=np.arange(len(party_names))
width=[0.8]*len(party_names)

fig,ax=plt.subplots(figsize=(20, 10))
ax.barh(ind,party_per,width)
ax.set(yticks=ind,yticklabels=party_nam,ylim=[-1,len(df)],xlim=[0,100])
fig.savefig('wohl-o-mat_results.png')