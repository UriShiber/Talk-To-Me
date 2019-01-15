"""
    copied from https://www.tutorialspoint.com/
    artificial_intelligence_with_python/
    artificial_intelligence_with_python_speech_recognition.htm

    another website:
    https://www.pythonforengineers.com/audio-and-digital-signal-processingdsp-in-python/
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile


def first_part(audio_signal, frequency_sampling):
    """
        does the first part in the paper - preparing the audio signal to be drawn.
    """
    audio_signal = (audio_signal / np.power(2, 15))
    # audio_signal = audio_signal[:100]
    time_axis = 1000 * np.arange(0, len(audio_signal), 1) / float(frequency_sampling)
    return time_axis


def draw(time_axis, audio_signal, x_label, y_label):
    plt.plot(time_axis, audio_signal, color='blue')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title('Input audio signal')
    plt.show()


def second_part(audio_signal, frequency_sampling):
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
    x_axis = np.arange(0, len_fts, 1) * (frequency_sampling / length_signal) / 1000.0
    return x_axis, signal_power


def main():
    frequency_sampling, audio_signal = wavfile.read(r"C:\Users\cyber\PycharmProjects\uri- sound wave\Cartoon-02.wav")
    # show characteristics to me ------------------------------------------------
    print('Signal shape:', audio_signal.shape)
    print('Signal Datatype:', audio_signal.dtype)
    print('Signal duration:', round(audio_signal.shape[0] / float(frequency_sampling), 2), 'seconds')
    # first part ----------------------------------------------------------------
    time_axis = first_part(audio_signal, frequency_sampling)
    draw(time_axis, audio_signal, 'Time (milliseconds)', 'Amplitude')
    # second part ---------------------------------------------------------------
    x_axis, signal_power = second_part(audio_signal, frequency_sampling)
    draw(x_axis, signal_power, 'Frequency (kHz)', 'Signal power (dB)')
    # third part (to do) --------------------------------------------------------
    # fourth part ---------------------------------------------------------------


if __name__ == '__main__':
    main()
