from gtts import gTTS 
import pygame

tts = gTTS(text = "Hello. I am ardop. How are you? Nice to meet you", lang = 'en-us')
# tts = gTTS(text = "indict", lang = 'en-us')

tts.save('tmp.mp3')

pygame.mixer.init()
pygame.init()
pygame.mixer.music.load('tmp.mp3')
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue

