
# import required module
import os
  
# play sound
file = "audio/startup.wav"
print('playing sound using native player')
os.system("aplay " + file)