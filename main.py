#main.py
import os
import shutil
from tqdm import tqdm
from pydub import AudioSegment
from pydub.utils import mediainfo
from process_audio import sample_change,SplitWavAudio
from model_manager import Model

def main():
    print("\n\t ## Wav2Vec v 0.1 \n")

    base = os.getcwd()
    audio_path = os.path.join(base,'audio')

    sampled_path = os.path.join(audio_path,'SampledAudio')
    split_path = os.path.join(audio_path,'SplitAudio')
    #final_path =os.path.join(audio_path,'FinalAudio')
    for paths in [sampled_path,split_path]: #,final_path
        if not os.path.exists(paths):
            os.mkdir(paths)

    print(">> Checking if Audio Files are in Recommended Sample Rate (and Converting if not) : ")
    for file in tqdm(os.listdir(audio_path)):
        file = os.path.join(audio_path,file)
        if os.path.isfile(file):
            info = mediainfo(file)
            if(info['sample_rate'] != 16000):
                sample_change(file,16000,sampled_path)
            else :
                shutil.copyfile(file,sampled_path)

    print("\n>> Checking if Audio Files are in Recommended Length[10-30 Sec] (and Splitting them if not) : ")
    for file in tqdm(os.listdir(sampled_path)):
        file = os.path.join(sampled_path,file)
        if os.path.isfile(file):
            audio = AudioSegment.from_file(file)
            if(audio.duration_seconds >= 30):
                split_wav = SplitWavAudio(file,split_path)
                split_wav.multiple_split(sec_per_split=30)
            else :
                shutil.copyfile(file,split_path)
    
main()
        


