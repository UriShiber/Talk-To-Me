import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import silence, AudioSegment
import os
import wave


wave_file = wave.open(r"C:\final_proj\Recordings\record_try_2.wav", 'rb')
duration = wave_file.getnframes() / float(wave_file.getframerate())
print(duration * 1000)
print(wave_file.getnframes() / (duration * 1000))
# the rate of an audio file means the number of updates or chunks in seconds,
# divide that by 1000 and we will get that each chunk will be a millisecond
# i want that each chunk will be in the size of a millisecond (like in the graph
# i drew earlier)
rate = wave_file.getframerate()
chunk = round((wave_file.getnframes()) / (duration * 1000))

p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wave_file.getsampwidth()),
                channels=wave_file.getnchannels(),
                rate=wave_file.getframerate(),
                output=True)

data = wave_file.readframes(chunk)
counter = 0
try:
    while data is not '':
        counter += 1
        data = np.fromstring(wave_file.readframes(chunk), dtype=np.int16)
        peak = np.average(np.abs(data))*2
        bars = "#" * int(500 * int(peak)/2**16)
        print("%04d %05d %s" % (counter, peak, bars))
except ValueError:
    print('finished')

stream.stop_stream()
stream.close()
p.terminate()

