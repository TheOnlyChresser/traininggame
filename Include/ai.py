import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR  ### temp 
import math

from data.torchDATA import TorcHdata

class dataStruct:
    def __init__(self):
#       validate input
        self.dataset = []
        self.datafile = ""
#       load from json file
        exit

    def reloadStruct():
        exit

    def upload(self , LossFunktion, aktiveringsFunktion, dataset):
        exit


class UserAI:
    def __init__(self, Lag, Bias, Vægte, AktiveringsFunktion, LossFunktion, Dataset, device, Epocs, LearningRate=1e-6):
   
#        if not ValidInput:
#            exit
        self.Lag = Lag
        self.Bias = Bias
        self.Vægte = Vægte
        self.LearningRate = LearningRate
        self.AktiveringsFunktion = AktiveringsFunktion
        self.LossFunktion = LossFunktion
        self.Dataset = Dataset
        self.Epocs = Epocs
        self.modelInfo = {}
        self.device = device
    
    def Setter(self, variableSet):
        pass

    def Getter(self, variableGet):
        exit

    def save():
        exit

    def load():
        exit
    
    def NNconstructor(self):
        for i in range(len(self.Lag)):
            self.modelInfo.update({self.Lag[i] + i:TorcHdata["lagTyper"][self.Lag]})

    def Run(self):
        w = torch.empty((max(self.Lag), len(self.Lag)), dtype=torch.float64)
        
        torch.nn.init.xavier_uniform_(w, gain=torch.nn.init.calculate_gain("softmax"))
        x = torch.linspace(-math.pi, math.pi, self.Lag[0], dtype=torch.float64)
        y = torch.sin(x)

        model = nn.Sequential(self.modelInfo)

        for i in range(self.Epocs):
            y_pred = model()