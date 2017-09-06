# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 15:10:13 2016
@author: Michael Schilling
"""
from gtts import gTTS
import os
import pygame
import time

def babel(blabla,language='en'):
    try:
        tts = gTTS(text=blabla, lang=language)
        filename = '/tmp/temp1.mp3'
        blankname = '/tmp/blank.mp3'
        try:
            tts.save(filename)
        except:
            os.remove(filename)
            tts.save(filename)
            
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy(): 
            time.sleep(1)
            
        if os.path.isfile(blankname):
            pygame.mixer.music.load(blankname)
        else:
            tts = gTTS(text='blank', lang='en')
            tts.save(blankname)
            os.remove(filename)
    except:
        print(blabla+' (speech synthesis offline)')
    
    return 1