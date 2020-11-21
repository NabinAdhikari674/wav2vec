#from fairseq.models.wav2vec import Wav2VecModel
#import torch
torch=1
Wav2VecModel = 1

class Model(self):
    def __init__(self):
        print("Model Manager Initiated")
        #self.modelpath = modelpath
    
    def load_model(self,modelpath):
        if not modelpath[-1][:2] == '.pt':
            print('The Model is not Valid. Try again with a valid Model.\nGiven Model Path : ',modelpath)
            return 
        print("Loading wav2vec Model ... ")
        cp = torch.load('Data/wav2vec_large.pt')
        model = Wav2VecModel.build_model(cp['args'], task=None)
        model.load_state_dict(cp['model'])
        model.eval()
        print("\n\tDone ##")