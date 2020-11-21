from pydub import AudioSegment
import math
import os

def sample_change(filename,sample_rate,dest):
    dest = os.path.join(dest,'8K_'+os.path.basename(filename))
    sound = AudioSegment.from_file(filename)
    sound = sound.set_frame_rate(sample_rate)
    sound.export(dest,format="wav")

class SplitWavAudio():
    def __init__(self, filepath,destination):
        self.filename = os.path.basename(filepath)
        self.filepath = filepath
        self.destination = destination
        self.folder = os.path.dirname(filepath)
        self.audio = AudioSegment.from_file(self.filepath)

    def get_duration(self):
        return self.audio.duration_seconds

    def single_split(self, from_sec, to_sec, split_filename):
        t1 = from_sec  * 1000
        t2 = to_sec  * 1000
        split_audio = self.audio[t1:t2]
        dest = os.path.join(self.destination,split_filename)
        if not os.path.exists(self.destination):
            os.mkdir(self.destination)
        split_audio.export(dest, format="wav")  

    def multiple_split(self, sec_per_split):
        total_sec = math.ceil(self.get_duration())
        for i in range(0, total_sec, sec_per_split):
            split_fn = str(i) + '_' + self.filename
            self.single_split(i, i+sec_per_split, split_fn)
        #print('\tAudio file \'',self.filename,"\' split into ",int(i/30+1)," parts.")
