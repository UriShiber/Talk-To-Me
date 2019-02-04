"""
this version got the first version of the func detect silence and an un
finish converter to wav
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment
import os
import wave
import pyaudio


RECORDING_DIR = r"C:\final_proj\Recordings"
FILES_TO_CONVERT_DIR = r"C:\final_proj\Files_To_Convert"


def convert_m4a_to_wav(file_name):
    """
    will be attached later after i will see the type of the file i will get from
    the front - end
    :param file_name:
    :return:
    """
    counter = 1
    for file in os.listdir(RECORDING_DIR):
        if os.path.isfile(os.path.join(RECORDING_DIR, file)):
            counter += 1
    # audio_signal_segment = AudioSegment.\
        # from_file(os.path.join(FILES_TO_CONVERT_DIR, file_name), 'm4a')
    audio_signal_segment = AudioSegment.\
        from_file(file_name, format="3gp")
    audio_file = os.path.join(RECORDING_DIR, "record_try_{0}".format(counter))
    audio_signal_segment.export(audio_file, 'wav')
    return audio_file


def detect_silence(audio_file):
    """
    detect spaces.
    first we divide a file to milliseconds - for comfort, we see for each chunk
    if its peak is more than 380 (roughly the volume of speech in these kinds of
    measuring), we write to a new file we open for each word thus (according to
    different kinds of limitations, such as len of silence=100, the norma).
    we get the audio file split to spaces in separate wav files.
    and we get the start and end indexes of a word - for debugging
    """
    wave_file, chunk, stream, p = prepare_full_file(audio_file)
    data = wave_file.readframes(chunk)
    # represents the time of the words ([start, end....]) for debugging
    words_time = []
    num_of_files = 1
    in_a_word = False
    # represents the min len of silence (counts from 0 till 1000)
    times_under_400 = 0
    # represents the milliseconds
    counter = 0
    # if it is the first file i open
    first = True
    # before the loop, the first file must be already declared and opened
    new_wav_file = wave.open(r"C:\final_proj\audio_chunk{0}.wav".
                             format(num_of_files), 'wb')
    new_wav_file.setparams((wave_file.getnchannels(),
                            wave_file.getsampwidth(),
                            wave_file.getframerate(),
                            wave_file.getnframes(),
                            wave_file.getcomptype(),
                            wave_file.getcompname()))
    try:
        # till the end of the file
        while data is not '':
            counter += 1
            # taking the info in chunk of millisecond in np int.16 format
            data = np.fromstring(wave_file.readframes(chunk), dtype=np.int16)
            # calculates a num for a margin of the highest part and lowest parts
            # by taking the absolute value for each member, then
            # calculates the average
            peak = np.average(np.abs(data))
            if not in_a_word:
                if peak > 400:
                    in_a_word = True
                    words_time.append(counter)
                    # if this is the second file, i need to open a new one
                    if not first:
                        num_of_files += 1
                        new_wav_file = wave. \
                            open(r"C:\final_proj\audio_chunk{0}.wav".
                                 format(num_of_files), 'wb')
                        new_wav_file.setparams((wave_file.getnchannels(),
                                                wave_file.getsampwidth(),
                                                wave_file.getframerate(),
                                                wave_file.getnframes(),
                                                wave_file.getcomptype(),
                                                wave_file.getcompname()))
                    # writes the sound to the new file (for each millisecond)
                    # (the start of a new word)
                    new_wav_file.writeframesraw(data)
            if in_a_word:
                # in a word, so write the sound to the new file till you get out
                # of the word
                new_wav_file.writeframesraw(data)
                if peak < 400:
                    times_under_400 += 1
                    if times_under_400 >= 50:  # len of silence
                        in_a_word = False
                        first = False
                        words_time.append(counter)
                        times_under_400 = 0
                else:
                    times_under_400 = 0
            # for debugging - good indicate for the volume
            bars = "#" * int(1000 * int(peak) / 2 ** 16)
            print("%04d %05d %s" % (counter, peak, bars))
    except ValueError:
        print('finished')
        print(words_time)
    # stops the stream
    stream.stop_stream()
    stream.close()
    p.terminate()


def prepare_full_file(audio_file):
    """

    :param audio_file:
    :return:
    """
    wave_file = wave.open(audio_file, 'rb')
    duration = wave_file.getnframes() / float(wave_file.getframerate())
    print(duration * 1000)
    print(wave_file.getframerate())
    print(wave_file.getnframes())
    print(wave_file.getnframes() / (duration * 1000))
    # the rate of an audio file means the number of updates or chunks in seconds
    # divide that by 1000 and we will get that each chunk will be a millisecond
    # i want that each chunk will be in the size of a millisecond (like in the
    # graph i drew earlier)
    chunk = round((wave_file.getnframes()) / (duration * 1000))
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wave_file.getsampwidth()),
                    channels=wave_file.getnchannels(),
                    rate=wave_file.getframerate(),
                    output=True)
    return wave_file, chunk, stream, p


def prepare_for_graphs():
    # for drawing the graphs====================================================
    frequency_sampling, audio_signal = wavfile. \
        read(r"C:\final_proj\Recordings\record_try_2.wav")
    # show characteristics to me
    print('Signal shape:', audio_signal.shape)
    print('Signal Datatype:', audio_signal.dtype)
    print('Signal duration:', round(audio_signal.shape[0] /
                                    float(frequency_sampling), 2), 'seconds')
    # normalizes the audio signal
    audio_signal = (audio_signal / np.power(2, 15))
    # first part - graph of amplitude to time ----------------------------------
    time_axis = amplitude_to_time(audio_signal, frequency_sampling)
    draw(time_axis, audio_signal, 'Time (milliseconds)', 'Amplitude')
    # second part - graph of power to frequency --------------------------------
    x_axis, signal_power = power_to_frequency(audio_signal, frequency_sampling)
    draw(x_axis, signal_power, 'Frequency (kHz)', 'Signal power (dB)')
    # third part (to do) -------------------------------------------------------
    # ==========================================================================


def draw(x_axis, audio, x_label, y_label):
    plt.plot(x_axis, audio, color='blue')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title('Input audio signal')
    plt.show()


def amplitude_to_time(audio_signal, frequency_sampling):
    """
    does the first part in the paper - preparing the audio signal to be drawn.
    """
    # audio_signal = audio_signal[:100]
    time_axis = 1000 * np.arange(0, len(audio_signal), 1) /\
        float(frequency_sampling)
    return time_axis


def power_to_frequency(audio_signal, frequency_sampling):
    """
    need to figure out what it does
    :param audio_signal:
    :param frequency_sampling:
    :return:
    """
    length_signal = len(audio_signal)
    half_length = np.ceil((length_signal + 1) / 2.0).astype(np.int)
    signal_frequency = np.fft.fft(audio_signal)
    signal_frequency = abs(signal_frequency[0:half_length]) / length_signal
    signal_frequency **= 2
    len_fts = len(signal_frequency)
    if length_signal % 2:
        signal_frequency[1:len_fts] *= 2
    else:
        signal_frequency[1:len_fts-1] *= 2
    try:
        signal_power = 10 * np.log10(signal_frequency)
    except RuntimeWarning:
        signal_power = 0
    x_axis = np.arange(0, len_fts, 1) * (frequency_sampling / length_signal) /\
        1000.0
    return x_axis, signal_power


def main():
    # creating a wav file from a recording -------------------------------------
    # audio_file = convert_m4a_to_wav("record_try_1.3gp")
    # --------------------------------------------------------------------------

    # separating the audio into words ------------------------------------------
    detect_silence(audio_file=r"C:\final_proj\Recordings\record_try_17.wav")
    # --------------------------------------------------------------------------

    # drawing the graphs (amplitude to time and power to frequency)-------------
    prepare_for_graphs()
    # --------------------------------------------------------------------------


if __name__ == '__main__':
    main()
