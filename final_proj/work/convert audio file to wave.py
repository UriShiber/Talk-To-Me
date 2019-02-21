"""
needs to move the ffmpeg to the same dir as this file
"""
from pydub import AudioSegment
import os
import wave

RECORDING_DIR = r"C:\final_proj\Recordings"
FILES_TO_CONVERT_DIR = r"C:\final_proj\Files_To_Convert"


def convert_file_to_wav(file_name):
    """
    will be attached later after i will see the type of the file i will get from
    the front - end
    :param file_name:
    :return:
    """
    counter = 1
    wave_file = wave.open(r"C:\final_proj\Recordings\record_try_1.wav", 'rb')
    for file in os.listdir(RECORDING_DIR):
        if os.path.isfile(os.path.join(RECORDING_DIR, file)):
            counter += 1

    audio_signal_segment = AudioSegment.from_file(file_name)
    audio_file = os.path.join(RECORDING_DIR, "record_try_{0}.wav".
                              format(counter))
    audio_signal_segment = audio_signal_segment.set_channels(wave_file.
                                                             getnchannels())
    audio_signal_segment = audio_signal_segment.set_frame_rate(wave_file.
                                                               getframerate())
    audio_signal_segment = audio_signal_segment.set_sample_width(wave_file.
                                                                 getsampwidth())
    audio_signal_segment.export(audio_file, format='wav')
    return audio_file


