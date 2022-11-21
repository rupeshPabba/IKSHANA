from gtts import gTTS
import os
import pyglet
import time

filename="hello.mp3"
tts=gTTS(text="hey sriya",lang="en")
tts.save(filename)

pyglet.options['audio']=('openal','pulse','directsound','silent')
audio=pyglet.media.load(filename,streaming=False)
audio.play()
time.sleep(audio.duration)