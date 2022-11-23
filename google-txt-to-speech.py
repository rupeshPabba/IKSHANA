from gtts import gTTS
import os
import pyglet
import time

x=["person","dog","cell phone","hello"]

for i in x:
    filename="sound.mp3"
    tts=gTTS(text=i,lang="en")
    tts.save(filename)

    pyglet.options['audio']=('openal','pulse','directsound','silent')
    audio=pyglet.media.load(filename,streaming=False)
    audio.play()
    time.sleep(audio.duration)