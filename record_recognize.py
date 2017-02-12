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

#Sound recording information
CHUNK = 1024
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 1 
RATE = 44100 #sample rate
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output.wav"

frames = []

p = pyaudio.PyAudio()

stream = 0


# Pygame UI funcitons ---------------------------------------------
def draw_circle(radius):
	pygame.draw.circle(screen, RED, [200, 200], radius)

def clear_screen():
	screen.fill(BLACK)
	pygame.display.flip()

#Recording functions ----------------------------------------------

def start_recording():
	#Append to the stream
	data = stream.read(CHUNK)
	frames.append(data) 


def record_sound():

	#Save the stream and clear frames to prepare for the next recording

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

	#Plotting the wav file

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


done = False

while not done:

	keys = pygame.key.get_pressed()
	if keys[pygame.K_r]:
		#Keep recording as long as the button is held down
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
		    	#Start the stream when the button is first pressed
		    	stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
		    	#Visual indicator while recording
		    	draw_circle(50)
		    

		elif event.type == pygame.KEYUP:
		    if event.key == pygame.K_r:
		    	clear_screen()
		    	record_sound()
		    	stream.stop_stream()
		    	stream.close()
		    	recognize()
		    	# process()

		#Updating display
		pygame.display.flip()




pygame.quit()


