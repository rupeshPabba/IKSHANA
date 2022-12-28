import speech_recognition as sr
from playsound import playsound
import os
from gtts import gTTS
import random
import object_detection as ik
import datetime
from urllib.request import urlopen
import json
import wikipedia
import webbrowser
from ecapture import ecapture as ec
import pyjokes
import wolframalpha
def name_generator():
    ran = random.randint(1,5000)
    ran = str(ran)
    return ran

def speak(detect):
    tts = gTTS(detect,lang="en")
    new_name = name_generator()
    new_name=  new_name+".mp3"
    tts.save(new_name)
    playsound(new_name)
    os.remove(new_name) 


r=sr.Recognizer()

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("speak anything")
    tts = gTTS('speak anything',lang="en")
    speak = name_generator()
    speak=  speak+".mp3"
    tts.save(speak)
    playsound(speak)
    os.remove(speak) 
    audio=r.listen(source)
    
    try:
        txt=r.recognize_google(audio)
        print(txt)
        if txt=='guide me':
            
            objects=ik.p
            detected=objects + "is in the front"
            tts = gTTS(detected,lang="en")
            new_name = name_generator()
            new_name=  new_name+".mp3"
            tts.save(new_name)
            playsound(new_name)
            os.remove(new_name) 
        elif txt=='what is the date and time':
            strTime = datetime.datetime.now()
            datestrtime=str(strTime)
            print(datestrtime)
            time1="the date and time is" + datestrtime
            tts = gTTS(time1,lang="en")
            new_name = name_generator()
            new_name=  new_name+".mp3"
            tts.save(new_name)
            playsound(new_name)
            os.remove(new_name) 
        
        elif txt=="play music":
            music_dir = r"C:\Users\dell\Music"
            songs = os.listdir(music_dir)
            print(songs)
            random = os.startfile(os.path.join(music_dir, songs[1]))
        
        elif txt=='news':

            try:
                jsonObj = urlopen('''https://newsapi.org / v1 / articles?source = the-times-of-india&sortBy = top&apiKey =\\times of India Api key\\''')
                data = json.load(jsonObj)
                i = 1

                
                print('''=============== TIMES OF INDIA ============'''+ '\n')

                for item in data['articles']:
                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    i += 1
            except Exception as e:

                print(str(e))

        elif txt=='what is love':
            love="It is 7th sense that destroy all other senses"
            tts = gTTS(love,lang="en")
            new_name = name_generator()
            new_name=  new_name+".mp3"
            tts.save(new_name)
            playsound(new_name)
            os.remove(new_name) 

        elif txt=="where" :
            query = txt.replace("where is", "")
            location = query
            webbrowser.open("https://www.google.nl / maps / place/" + location + "")

        elif txt=='how are you':
            f1="I am fine, Thank you"
            tts = gTTS(f1,lang="en")
            new_name = name_generator()
            new_name=  new_name+".mp3"
            tts.save(new_name)
            playsound(new_name)
            os.remove(new_name)
            

        
        
        elif txt=='tell me a joke':
            joke=pyjokes.get_joke()
            tts = gTTS(joke,lang="en")
            new_name = name_generator()
            new_name=  new_name+".mp3"
            tts.save(new_name)
            playsound(new_name)
            os.remove(new_name)

        
        
        elif txt=="Wikipedia" or "wikipedia":
            tts = gTTS("what you wanted to search",lang="en")
            new_name = name_generator()
            new_name=  new_name+".mp3"
            tts.save(new_name)
            playsound(new_name)
            os.remove(new_name) 

            r=sr.Recognizer()

            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                audio=r.listen(source)
                txt=r.recognize_google(audio)
                result = wikipedia.summary(txt, sentences = 2)
                tts = gTTS(result,lang="en")
                new_name = name_generator()
                new_name=  new_name+".mp3"
                tts.save(new_name)
                playsound(new_name)
                os.remove(new_name)
        



         
            
    except:
        print('sorry couldnt recognize your voice')
        tts = gTTS('sorry couldnt reconize your voice',lang="en")
        new_name = name_generator()
        new_name=  new_name+".mp3"
        tts.save(new_name)
        playsound(new_name)
        os.remove(new_name) 


    