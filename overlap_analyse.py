import torch
import wget
from os.path import join, basename, isfile
from os import getcwd, remove
from tinytag import TinyTag
from pydub import AudioSegment
import pickle
import atexit


HEADER = 15
FOOTER = 40
model = torch.hub.load('pyannote/pyannote-audio', 'ovl_dihard', pipeline=True, verbose=False)
audio_path = join(getcwd(), "data", "audio")
result_path = join(getcwd(), "data", "results")
episodes = join(getcwd(), "list_of_dr_laura.txt")
counter_path = join(getcwd(), "counter.pkl")


class Counter():
    def __init__(self):
        self.total_duration = 0
        self.total_overlap = 0
        self.average_time_before_overlap = 0
        self.files_seen = 0


def wav_duration(fname):
    tag = TinyTag.get(fname)
    return tag.duration


def convert_mp3_to_wav(mp3, wav):
    sound = AudioSegment.from_mp3(mp3)
    sound.export(wav, format="wav")


def save_results(speech_activity_detection, wav):
    res = join(result_path, str(basename(wav).split('.')[0]) + '.rttm')
    with open(res, 'w+') as f:
        speech_activity_detection.write_rttm(f)


def overlap_duration(wav):
    speech_activity_detection = model({'audio': wav})
    save_results(speech_activity_detection, wav)
    total_overlap = 0
    num_of_regions = 1
    for speech_region in speech_activity_detection.get_timeline():
        if HEADER < speech_region.start < (wav_duration(wav) - FOOTER):
            total_overlap += speech_region.end - speech_region.start
            num_of_regions += 1
    average_time_before_overlap = (wav_duration(wav) - HEADER - FOOTER) / num_of_regions
    return total_overlap, average_time_before_overlap


def save_and_print_results(i, wav, c):
    c.files_seen = i + 1
    c.total_duration += round((wav_duration(wav) - HEADER - FOOTER), 2)
    overlap, average = overlap_duration(wav)
    c.total_overlap += round(overlap, 2)
    c.average_time_before_overlap = round(((c.average_time_before_overlap*(c.files_seen-1))+average)/c.files_seen, 2)
    average_overlap_duration = round(c.total_overlap / c.total_duration, 4) * 100
    print("Seen " + str(c.files_seen) + " files: average overlap time = " + str(average_overlap_duration)
          + "%; average time between overlaps = " + str(c.average_time_before_overlap) + "s")
    return c


def load_counter():
    if isfile(counter_path):
        with open(counter_path, 'rb') as file:
            c = pickle.load(file)
    else:
        c = Counter()
    return c


def save_counter(c):
    with open(counter_path, 'wb') as file:
        pickle.dump(c, file)


def main():
    c = load_counter()
    atexit.register(save_counter, c)
    try:
        with open(episodes, "r") as f:
            ep_urls = f.read().split()
        for i, url in enumerate(ep_urls):
            if i < c.files_seen:
                continue
            mp3 = join(audio_path, basename(url))
            wav = str(mp3.split('.')[0]) + ".wav"
            wget.download(url, mp3)
            convert_mp3_to_wav(mp3, wav)
            remove(mp3)
            if wav_duration(wav) > (HEADER + FOOTER):
                c = save_and_print_results(i, wav, c)
            remove(wav)
    except Exception:
        save_counter(c)


if __name__ == "__main__":
    main()
