from playsound import playsound
#import webSearch
import os
import random
from gtts import gTTS
import time

def name_generator():
    ran = random.randint(1,5000)
    ran = str(ran)
    return ran


def TalkBack(case_ans):
    print("in ...................................")
    tts = gTTS(text=case_ans,lang="en")
    new_name = name_generator()
    new_name= new_name +".mp3"
    tts.save(new_name)
    try:  
        print("saving...............................")
        playsound(new_name)
        print("saying................................")
        
        #os.remove(new_name) 
    except:
        print("i cant")

x=["hello","this is team","ikshana vision","we are","isomniacs"]
for i in x:
    TalkBack(i)
    