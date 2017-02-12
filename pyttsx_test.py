import pyttsx

engine = pyttsx.init()

engine.setProperty('rate', 150)
engine.say('Hello. I am ardop. How are you? Nice to meet you.')
print engine.getProperty('rate')



engine.runAndWait()