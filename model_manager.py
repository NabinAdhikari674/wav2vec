#from fairseq.models.wav2vec import Wav2VecModel
#import torch
#import torchaudio
torchaudio=1
torch=1
Wav2VecModel = 1

class Model():
    def __init__(self):
        print("Model Manager Initiated")
        #self.modelpath = modelpath
    
    def load_model(self,modelpath):
        if not modelpath[-3:] == '.pt':
            print('The Model is not Valid. Try again with a valid Model.\n Given Model Path : ',modelpath)
            return 
        print("Loading wav2vec Model ... ",end='')
        tload = torch.load(modelpath)
        self.model = Wav2VecModel.build_model(tload['args'], task=None)
        self.model.load_state_dict(tload['model'])
        self.model.eval()
        print(" ## Model Loaded ##")

    def load_audio(self,audiopath):
        self.waveform, self.sample_rate = torchaudio.load(audiopath)
        return self.waveform,self.sample_rate

    @property
    def feature_extractor(self):
        self.features = self.model.feature_extractor(self.waveform)
        return self.features
    @property
    def feature_aggregator(self):
        self.afeature = self.model.feature_aggregator(self.features)
        return self.afeature
    
