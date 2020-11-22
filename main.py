#main.py
import os
import shutil
from tqdm import tqdm
from pydub import AudioSegment
from pydub.utils import mediainfo
import subprocess

from process_audio import sample_change,SplitWavAudio
from model_manager import Model

def check_sample_rate(audio_path,sampled_path):
    print(">> Checking if Audio Files are in Recommended Sample Rate (and Converting if not) : ")
    for file in tqdm(os.listdir(audio_path)):
        file = os.path.join(audio_path,file)
        if os.path.isfile(file):
            info = mediainfo(file)
            if(info['sample_rate'] != 16000):
                sample_change(file,16000,sampled_path)
            else :
                shutil.copyfile(file,sampled_path)

def check_rec_length(sampled_path,split_path):
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

def create_manifest(generator,audio_path,manifest_path):
    print("\n>> Creating Manifest Files for Training ... ")
    generator = os.path.join(generator,'wav2vec_manifest.py')
    cmd = 'python {} {} --dest {} --ext wav --valid-percent 0.01'.format(generator,audio_path,manifest_path)
    subprocess.run(cmd)
    print("\t Manifest Created in : ",manifest_path)

def train_model(trainer,manifest_path,model_path):
    print("Starting the Training of the wav2vec Model ... ")
    
    trainer = os.path.join(trainer,'train.py')
    manifest = manifest_path # Path for manifest files to be used in training
    model = model_path  # Path to store Output Model
    convFeatureLayers = "[(512, 10, 5), (512, 8, 4), (512, 4, 2), (512, 4, 2), (512, 4, 2), (512, 1, 1), (512, 1, 1)]"
    convAggregatorLayers = "[(512, 2, 1), (512, 3, 1), (512, 4, 1), (512, 5, 1), (512, 6, 1), (512, 7, 1), (512, 8, 1), (512, 9, 1), (512, 10, 1), (512, 11, 1), (512, 12, 1), (512, 13, 1)]"
    lr = 1e-06 # Learning Rate
    minLr = 1e-09 # Min Learning Rate
    #optimizer = "adam"
    maxLr = 0.005 # Max Learning Rate

    cmd = 'python {} {} --save-dir {}'.format(trainer,manifest,model)
    cmd += ' --num-workers 6 --fp16 --max-update 400000 --save-interval 1 --no-epoch-checkpoints --arch wav2vec --task audio_pretraining'
    cmd += ' --lr {} --min-lr {} --optimizer adam --max-lr {} --lr-scheduler cosine'.format(lr,minLr,maxLr)
    cmd += ' --conv-feature-layers {} --conv-aggregator-layers {}'.format(convFeatureLayers,convAggregatorLayers)
    cmd += ' --skip-connections-agg --residual-scale 0.5 --log-compression --warmup-updates 500'
    cmd += ' --warmup-init-lr 1e-07 --criterion wav2vec --num-negatives 10 --max-sample-size 150000'
    cmd += ' --max-tokens 1500000 --skip-invalid-size-inputs-valid-test'

    subprocess.run(cmd)


def main():
    base = os.getcwd()
    audio_path = os.path.join(base,'audio')
    sampled_path = os.path.join(audio_path,'SampledAudio')
    split_path = os.path.join(audio_path,'SplitAudio')
    manifest_path = os.path.join(base,'manifest')
    model_path = os.path.join(base,'model')
    
    #final_path =os.path.join(audio_path,'FinalAudio')
    for paths in [sampled_path,split_path,manifest_path,model_path]: #,final_path
        if not os.path.exists(paths):
            os.mkdir(paths)

    check_sample_rate(audio_path,sampled_path)
    check_rec_length(sampled_path,split_path)
    
    wav2vec_path = os.path.join(base,'fairseq','examples','wav2vec')
    
    create_manifest(wav2vec_path,split_path,manifest_path)

    train_model(os.path.join(base,'fairseq'),manifest_path,model_path)


if __name__ == "__main__":
    print("\n\t ## Wav2Vec v 0.1 by NabinAdhikari674\n")
    main()

        


