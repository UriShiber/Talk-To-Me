"""

    copied from https://www.tutorialspoint.com/
    artificial_intelligence_with_python/
    artificial_intelligence_with_python_speech_recognition.htm

    another website:
    https://www.pythonforengineers.com/audio-and-digital-signal-processingdsp-
    in-python/
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import silence, AudioSegment
import os

RECORDING_DIR = r"C:\final_proj\Recordings"
FILES_TO_CONVERT_DIR = r"C:\final_proj\Files_To_Convert"


def convert_m4a_to_wav(file_name):
    counter = 1
    for file in os.listdir(RECORDING_DIR):
        if os.path.isfile(os.path.join(RECORDING_DIR, file)):
            counter += 1
    # audio_signal_segment = AudioSegment.\
        # from_file(os.path.join(FILES_TO_CONVERT_DIR, file_name), 'm4a')
    audio_signal_segment = AudioSegment.\
        from_file(r"C:\final_proj\Files_To_Convert\try1.wav", format="wav")
    audio_file = os.path.join(RECORDING_DIR, "record_try_{0}".format(counter))
    audio_signal_segment.export(audio_file, 'wav')
    return audio_file


def detect_silence(audio_file):
    """
    detect spaces by analyzing the graph of the first part and seeing there if
    the y value is less than 1500, if it does:
    take x value of it and save it as the start position of the silent. and
    actually the end position of a word
    after we have the start of the silent part, we need to look for the finish
    of it, (and the starting of a new word) there we need to see if the y value
    is more than 1500.
    we get the start index of a word and its end index so we need to create a
    file to it.
    """
    try:
        audio_signal_segment = AudioSegment.\
            from_file(audio_file)
        chunks = silence.split_on_silence(audio_signal_segment,
                                          min_silence_len=100,
                                          silence_thresh=-16)
        for i, chunk in enumerate(chunks):
            chunk.export(r"C:\final_proj\chunk{0}".format(i), format="wav")
    except RuntimeWarning:
        pass


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
    detect_silence(audio_file=r"C:\final_proj\Files_To_Convert\try1.wav")
    # --------------------------------------------------------------------------

    # for drawing the graphs====================================================
    frequency_sampling, audio_signal = wavfile.read(audio_file)
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


if __name__ == '__main__':
    main()
