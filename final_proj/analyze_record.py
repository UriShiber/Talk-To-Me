"""
this version detects sounds great but letters poorly
"""

import numpy as np
import os
import wave
import pyaudio
# import matplotlib.pyplot as plt
from convert_audio_file_to_wave import convert_file_to_wav
import librosa
import librosa.display
import threading
import queue

RECORDING_DIR = r"C:\Users\Noa\Desktop\uri- final project\Recordings"
FILES_TO_CONVERT_DIR = r"C:\Users\Noa\Desktop\uri- final project\Files to convert"
EXAMPLE_FILE = r"C:\Users\Noa\Desktop\uri- final project\Recordings\record_try_1.wav"
AUDIO_CHUNKS_DIR = r"C:\Users\Noa\Desktop\uri- final project\Recordings\audio_chunks"


def detect_silence(audio_file):
    """
    the len normalizer is in prepare_full_file
    detect spaces.
    first we divide a file to milliseconds - for comfort, we see for each chunk
    if its peak is more than 380 (roughly the volume of speech in these kinds of
    measuring), we write to a new file we open for each word thus (according to
    different kinds of limitations, such as len of silence=100, the norma).
    we get the audio file split to spaces in separate wav files.
    and we get the start and end indexes of a word - for debugging
    letters that are hard to manage (when opening a word):
    f
    heit
    chaf
    sameh
    shin
    """
    wave_file, chunk, stream, p = prepare_full_file(audio_file, bool_normalize_duration=False)
    # detects the volume parameter of each record file in order to normalize
    # the audio chunks we get out of it to a 1000 volume
    data = wave_file.readframes(chunk)
    # represents the time of the words ([start, end....]) for debugging
    words_time = []
    not_a_word = []
    num_of_files = 1
    for file in os.listdir(AUDIO_CHUNKS_DIR):
        if os.path.isfile(os.path.join(AUDIO_CHUNKS_DIR, file)):
            num_of_files += 1
    in_a_word = False
    # represents the min len of silence (counts from 0 till 1000)
    times_under_400 = 0
    # represents the milliseconds
    counter = 0
    # if it is the first file i open
    first = True
    # before the loop, the first file must be already declared and opened
    new_wav_file = wave.open(r"C:\Users\Noa\Desktop\uri- final project\Recordings\audio_chunks\audio_chunk{0}.wav".
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
                if peak > 300:
                    in_a_word = True
                    words_time.append(counter)
                    # if this is the second file, i need to open a new one
                    if not first:
                        num_of_files += 1
                        new_wav_file = wave. \
                            open(r"C:\Users\Noa\Desktop\uri- final project\Recordings\audio_chunks\audio_chunk{0}.wav".
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
                if peak < 300:
                    times_under_400 += 1
                    if times_under_400 >= 150:  # len of silence
                        in_a_word = False
                        first = False
                        words_time.append(counter)
                        times_under_400 = 0
                        if words_time[-1] - words_time[-2] < 300:
                            not_a_word.append(num_of_files)
                else:
                    times_under_400 = 0
            # for debugging - good indicate for the volume
            # bars = "#" * int(1000 * int(peak) / 2 ** 16)
            int(peak)
            # print("%04d %05d %s" % (counter, peak, bars))
    except ValueError:
        pass
    # stops the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    return words_time.__len__() / 2, not_a_word


def prepare_full_file(audio_file, bool_normalize_duration):
    """
    a problem with the duration normalizer !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    in order to normalize the duration, needs to be called with a file name and
    true (otherwise calculates regularly):
    600 milliseconds is approximately the duration of a word, as a result i want
    that the duration of all the files will be as if it was 600 so
    each chunk will represent the data of each 1/600 instead of each millisecond
    for example if word's duration is 477, each chunk length will be
    48 (normal proportional chunk size in millisecond) * the duration parameter
    which is duration / 600 which means that every chunk will represent the num
    of frames / 600
    """
    wave_file = wave.open(audio_file, 'rb')
    duration = wave_file.getnframes() / float(wave_file.getframerate())
    duration = duration * 1000
    # the rate of an audio file means the number of updates or chunks in seconds
    # divide that by 1000 and we will get that each chunk will be a millisecond
    # i want that each chunk will be in the size of a millisecond (like in the
    # graph i drew earlier)
    if bool_normalize_duration:
        duration_parameter = duration / 600
        chunk = round(float(wave_file.getframerate() * duration_parameter)
                      / 1000)
    else:
        chunk = round(float(wave_file.getframerate()) / 1000)
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wave_file.getsampwidth()),
                    channels=wave_file.getnchannels(),
                    rate=wave_file.getframerate(),
                    output=True)
    return wave_file, chunk, stream, p


def remove_record_garbage(not_a_word, num_of_chunks):
    """
    deletes the audio chunks that are not words
    :return:
    """
    i = 0
    while i < not_a_word.__len__():
        os.remove(r"C:\Users\Noa\Desktop\uri- final project\Recordings\audio_chunks\audio_chunk{0}.wav".
                  format(not_a_word[i]))
        i += 1
        num_of_chunks -= 1
    return num_of_chunks


def compare_power(signal_power_1, signal_power_2):
    distance = np.linalg.norm(signal_power_1 - signal_power_2)
    return distance


def prepare_return_vowel(vowel, return_string, is_final_letter):
    """
    need to add shva vowel and the check- if it is the final letter
    :param vowel:
    :param return_string:
    :param is_final_letter:
    :return:
    """
    if vowel == 'aa':
        if is_final_letter:
            return_string = 'ה'
        else:
            return_string = ''
    elif vowel == 'a':
        if is_final_letter:
            return_string = 'ה'
        else:
            return_string = ''
    elif vowel == 'i':
        return_string = 'י'
    elif vowel == 'o':
        return_string = 'ו'
    elif vowel == 'u':
        return_string = 'ו'
    elif vowel == 'e':
        return_string = ''
    return return_string


def detect_vowel(my_que, new_example_spec, new_mel_spec, new_end_of_shape, new_relative_index, this_num_of_vowel):
    """
    i did some things to make it better:
    1) i put it in the same part as the new audio (same indexes)
    2) i took an even part of values from each array
    *** need to check vowels u, o, i, e with all the other letters
    *** in the long future need to see if it is in the end of the word or not, if not in the end of the word, i need to
        check only the o, u and i
    :param my_que:
    :param this_num_of_vowel:
    :param new_relative_index:
    :param new_end_of_shape:
    :param new_mel_spec:
    :param new_example_spec:
    :return:
    """
    sum_distance = 0
    num_of_folders = 1
    while num_of_folders <= 5:
        path = os.path.join(RECORDING_DIR, "audio_chunks")
        path = os.path.join(path, "vowels{0}".format(num_of_folders))
        example_spec = np.zeros((80, 1200))

        mel_spec = do_mel_spec(os.path.join(path, "audio_chunk{0}.wav".format(this_num_of_vowel)))
        example_spec[example_spec == 0] = np.min(new_mel_spec)

        start_of_shape, end_of_shape = take_period_of_high_frequency_vowel(mel_spec)
        relative_index = start_of_shape + int((end_of_shape - start_of_shape) / 2)
        mel_spec[:, :] += np.min(new_mel_spec) - np.min(mel_spec)

        example_spec[:, new_relative_index:new_end_of_shape - 20] = \
            mel_spec[:, relative_index:relative_index + new_end_of_shape - new_relative_index - 20]

        distance = compare_power(example_spec, new_example_spec)
        sum_distance += distance
        num_of_folders += 1

    my_que.put(sum_distance)


def new_vowel(file_name):
    """
    detects the characteristics of the new vowel
    :param file_name:
    :return:
    """
    new_example_spec = np.zeros((80, 1200))
    new_path = os.path.join(RECORDING_DIR, file_name)
    new_mel_spec = do_mel_spec(new_path)
    new_example_spec[new_example_spec == 0] = np.min(new_mel_spec)

    new_start_shape, new_end_of_shape = take_period_of_high_frequency_vowel(new_mel_spec)
    new_relative_index = new_start_shape + int((new_end_of_shape - new_start_shape) / 2)

    new_example_spec[:, new_relative_index:new_end_of_shape - 20] = \
        new_mel_spec[:, new_relative_index:new_end_of_shape - 20]
    return new_example_spec, new_mel_spec, new_end_of_shape, new_relative_index


def new_letter(file_name):
    """
        detects the characteristics of the new letter
        :param file_name:
        :return:
        """
    new_example_spec = np.zeros((80, 1200))
    new_path = os.path.join(RECORDING_DIR, file_name)
    new_mel_spec = do_mel_spec(new_path)
    new_example_spec[new_example_spec == 0] = np.min(new_mel_spec)

    new_start_shape, new_end_of_shape = take_period_of_high_frequency_letter(new_mel_spec)
    new_relative_index = new_start_shape + int((new_end_of_shape - new_start_shape) / 2)
    # print("new_start_shape:", new_start_shape)
    # if new_start_shape >= 50:
    new_example_spec[:, :new_start_shape + 10] = new_mel_spec[:, :new_start_shape + 10]
    # else:
    # there are 2 options:
    # 1) keep the same number of samples (100) each time
    # 2) check until start_of_shape + 50 even if it means different num of samples
    # new_example_spec[:, :150] = new_mel_spec[:, :150]
    # print(new_start_shape)
    return new_example_spec, new_mel_spec, new_end_of_shape, new_relative_index


def detect_letter(my_que, new_example_spec, new_mel_spec, this_num_of_vowel):
    """
    at this moment i don't use new_end_of_shape and new_relative_index but i pass them anyway
    can use also new_end_of_shape or new_relative_index but dosent for now
    :param my_que:
    :param new_example_spec:
    :param new_mel_spec:
    :param this_num_of_vowel:
    :return:
    """
    sum_distance = 0
    # number of times i recorded each letter in the specified sound (the number of folders)
    num_of_folders = 1
    while num_of_folders <= 10:
        path = os.path.join(RECORDING_DIR, "audio_chunks")
        path = os.path.join(path, "hebrew aaa {0}".format(num_of_folders))
        mel_spec = do_mel_spec(os.path.join(path, "audio_chunk{0}.wav".format(this_num_of_vowel)))
        example_spec = np.zeros((80, 1200))
        example_spec[example_spec == 0] = np.min(new_mel_spec)
        start_of_shape, end_of_shape = take_period_of_high_frequency_letter(mel_spec)
        # relative_index = start_of_shape + int((end_of_shape - start_of_shape) / 2)
        mel_spec[:, :] += np.min(new_mel_spec) - np.min(mel_spec)
        # if start_of_shape >= 50:
        example_spec[:, :start_of_shape + 10] = mel_spec[:, :start_of_shape + 10]
        # else:
        # there are 2 options:
        # 1) keep the same number of samples (100) each time
        # 2) check until start_of_shape + 50 even if it means different num of samples
        # example_spec[:, :100] = mel_spec[:, :100]
        # print(np.min(example_spec))
        distance = compare_power(new_example_spec, example_spec)
        print(this_num_of_vowel, num_of_folders, distance)
        sum_distance += distance
        num_of_folders += 1
    my_que.put(sum_distance)


def take_period_of_high_frequency_letter(mel_spec):
    """
        :param mel_spec:[0] represents the rows
                        [1] represents the columns
        :return:
        """
    x = np.min(mel_spec)
    i = 0
    j = 0
    firsts = []
    not_first = False
    lasts = [np.shape(mel_spec)[1]]
    time_above_frequency = 0
    while i < np.shape(mel_spec)[1]:
        while j < np.shape(mel_spec)[0]:
            if mel_spec[j, i] > x + 40:
                time_above_frequency += 1
            if time_above_frequency > 10:
                j = np.shape(mel_spec)[0]
            j += 1
        if not_first:
            if time_above_frequency < 10:
                lasts.append(i)
                not_first = False
        if not not_first:
            if time_above_frequency > 10:
                firsts.append(i)
                not_first = True
        j = 0
        i += 1
        time_above_frequency = 0
    # print(firsts[0], lasts[-1])
    if not firsts:
        firsts.append(0)
    return firsts[0], lasts[-1]


def take_period_of_high_frequency_vowel(mel_spec):
    """
    i changed 5 times instead of 10
    :param mel_spec:[0] represents the rows
                    [1] represents the columns
    :return:
    """
    x = np.min(mel_spec)
    i = 0
    j = 0
    firsts = []
    not_first = False
    lasts = [np.shape(mel_spec)[1]]
    time_above_frequency = 0
    while i < np.shape(mel_spec)[1]:
        while j < np.shape(mel_spec)[0]:
            if mel_spec[j, i] > x + 30:
                time_above_frequency += 1
            if time_above_frequency > 5:
                j = np.shape(mel_spec)[0]
            j += 1
        if not_first:
            if time_above_frequency < 5:
                lasts.append(i)
                not_first = False
        if not not_first:
            if time_above_frequency > 5:
                firsts.append(i)
                not_first = True
        j = 0
        i += 1
        time_above_frequency = 0
    # print(firsts[0], lasts[-1])
    return firsts[0], lasts[-1]


def do_mel_spec(audio_path):
    """
    i got two ways:
    1) maybe i can get the most dominant frequency of every time perioud (0.01s) and then i can shrink the specto and
       do the graph
    2) i can get an average of the power in each frequency for each 10 periods of time (0.1s) and then do a graph of it

    :param audio_path:
    :return:
    """
    # sr = sample rate
    # y = audio time signal (i think amplitude to time) if i take this shape and divide to the sr i get the duration so
    # 4800 values in this will give me each 0.1 second
    # log specto = the power in each frequency and second.
    # in the log_specto if we indice it [:10] it changes the height of each db square so it stretches it over larger
    # amount of frequencies that means that each row in the table represents different frequency or
    # and every colum represents roughly 0.01 seconds
    [y, sr] = librosa.core.load(audio_path, sr=48000)
    specto = librosa.feature.melspectrogram(y, sr=sr, n_fft=400, hop_length=65, n_mels=80)
    log_specto = librosa.core.amplitude_to_db(specto)
    # plt.figure(figsize=(12, 4))
    # librosa.display.specshow(log_specto, sr=sr, x_axis='time', y_axis='mel')
    # plt.title('mel power spectrogram {0}'.format(audio_path))
    # plt.colorbar(format='%+02.0f dB')
    # plt.tight_layout()
    # plt.show()
    return log_specto


def create_threads_for_vowels(num_of_values, file):
    """
    creates threads (no more than 8, computer's ability)
    """
    vowels = ['aa', 'a', 'o', 'u', 'i', 'e']
    total_distances = []
    new_example_spec, new_mel_spec, new_end_of_shape, new_relative_index = new_vowel(file)
    my_que = queue.Queue()
    this_num_of_values = 0
    while this_num_of_values < num_of_values:
        if threading.active_count() <= 5:
            this_num_of_values += 1
            th = threading.Thread(target=detect_vowel, args=(my_que, new_example_spec, new_mel_spec,
                                                             new_end_of_shape, new_relative_index,
                                                             this_num_of_values))
            th.start()
            result = my_que.get()
            total_distances.append(result)
    print(total_distances)
    if any(total_distances) == 0:
        return vowels[5]
    return vowels[total_distances.index(min(total_distances))]


def create_threads_for_letters(num_of_values, file):
    """
    creates threads (no more than 8, computer's ability)
    """
    letters = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש',
               'ת', 'פ']
    total_distances = []
    new_example_spec, new_mel_spec, new_end_of_shape, new_relative_index = new_letter(file)
    my_que = queue.Queue()
    this_num_of_values = 0
    while this_num_of_values < num_of_values:
        if threading.active_count() <= 1:
            # print(this_num_of_values)
            this_num_of_values += 1
            th = threading.Thread(target=detect_letter, args=(my_que, new_example_spec, new_mel_spec,
                                                              this_num_of_values))
            th.start()
            if this_num_of_values >= num_of_values:
                break
        result = my_que.get()
        total_distances.append(result)
    result = my_que.get()
    total_distances.append(result)
    for i in range(total_distances.__len__()):
        print(i + 1, total_distances[i])
    return letters[total_distances.index(min(total_distances))]


def main_analyzer():
    """
    in detecting the word i will need to see first if the file exist because i am deleting some that are not good
    =======================================================
    for now, seperate to words, acts like seperate to vowels
    because i am saying the vowel with space- for comfort,
    untill i will seperate the audio in to vowels
    as a result, there is a variable num_of_vowels, instead
    num_of_words
    =======================================================
    in the future i will make each vowel a process so i can analyze 5 vowels at a time and that the time to develop
    4 vowels will be like 1- 7.5s (only if connected to the electricity - on the laptop)
    :return:
    """
    # creating a wav file from a recording -------------------------------------
    # audio_file = convert_file_to_wav(os.path.join(FILES_TO_CONVERT_DIR, "ר5.m4a"))
    # audio_file = convert_file_to_wav(os.path.join(FILES_TO_CONVERT_DIR, "my_record1"))
    # --------------------------------------------------------------------------
    i = 1
    for file in os.listdir(AUDIO_CHUNKS_DIR):
        if os.path.isfile(os.path.join(AUDIO_CHUNKS_DIR, file)):
            i += 1

    # separating the audio into words ------------------------------------------
    # num_of_chunks, not_a_word = detect_silence(audio_file)
    # num_of_vowels = remove_record_garbage(not_a_word, num_of_chunks)
    # detecting the letter and the vowel ---------------------------------------
    # --------------------------------------------------------------------------
    return_string = ""
    # num_of_vowels += i - 1
    i = 1
    num_of_vowels = 1
    print("num_of_vowels:", num_of_vowels)
    while i <= num_of_vowels:
        # file = os.path.join(AUDIO_CHUNKS_DIR, "audio_chunk{0}.wav".format(i))
        file = os.path.join(r"C:\Users\Noa\Desktop\uri- final project\Recordings\audio_chunks\repair2\ף", "audio_chunk20.wav")
        return_string += create_threads_for_letters(23, file)
        vowel = create_threads_for_vowels(6, file)
        return_string += prepare_return_vowel(vowel, return_string, True)
        i += 1
    # --------------------------------------------------------------------------
    print(return_string)
    return return_string
    # file = os.path.join(r"C:\Users\Noa\Desktop\uri- final project\Recordings\sounds of b", "b.wav")
    # do_mel_spec(file)
    # vowel = create_threads_for_vowels(5, file)
    # print(vowel)


if __name__ == '__main__':
    main_analyzer()
