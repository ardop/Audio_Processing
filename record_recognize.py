import pygame
import pyaudio
import wave
import speech_recognition as sr
import sys
import numpy as np
import matplotlib.pyplot as plt

pygame.init()

RED=(255,0,0)
BLACK=(0,0,0)

#width and height of screen
size=(400, 400)
screen= pygame.display.set_mode(size)

pygame.display.set_caption("VOICE")
clock=pygame.time.Clock() 

CHUNK = 1024
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 1 
RATE = 44100 #sample rate
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output.wav"

frames = []

p = pyaudio.PyAudio()

stream = 0

def draw_circle(radius):
	pygame.draw.circle(screen, RED, [200, 200], radius)

def clear_screen():
	screen.fill(BLACK)
	pygame.display.flip()

def start_recording():
	data = stream.read(CHUNK)
	frames.append(data) 


def record_sound():

	global frames
	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	frames = []
	wf.close()
	print "Done Saving"

def recognize():

	r = sr.Recognizer()
	with sr.WavFile(WAVE_OUTPUT_FILENAME) as source:              # use "test.wav" as the audio source
	    audio = r.record(source)                        # extract audio data from the file

	try:
	    print("Transcription: " + r.recognize(audio))   # recognize speech using Google Speech Recognition
	except LookupError:                                 # speech is unintelligible
	    print("Could not understand audio")

def process():

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'r')

	signal = wf.readframes(-1)
	signal = np.fromstring(signal, 'Int16')
	fs = wf.getframerate()

	time = np.linspace(0, len(signal)/fs, num = len(signal))
	
	plt.figure(1)
	plt.title('Signal wave')
	# plt.plot(signal)
	plt.plot(time, signal)
	plt.show()

	print max(signal)
	print min(signal)


done = False

while not done:

	keys = pygame.key.get_pressed()
	if keys[pygame.K_r]:
		start_recording()

	for event in pygame.event.get():
		if event.type==pygame.QUIT:
		    done = True
		    stream.stop_stream()
		    stream.close()
		    p.terminate()

		if event.type==pygame.KEYDOWN:

		    if event.key == pygame.K_ESCAPE:
		    	done = True
		    	p.terminate()
		    	stream.stop_stream()
		    	stream.close()

		    if event.key == pygame.K_r:
		    	stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
		    	draw_circle(50)
		    

		elif event.type == pygame.KEYUP:
		    if event.key == pygame.K_r:
		    	clear_screen()
		    	record_sound()
		    	stream.stop_stream()
		    	stream.close()
		    	recognize()
		    	# process()


		pygame.display.flip()




pygame.quit()


