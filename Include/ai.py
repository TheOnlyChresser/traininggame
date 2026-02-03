import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import StepLR  ### temp 
import collections
import typing

from data.torchDATA import TorcHdata

class dataStruct:
    def __init__(self):
#       validate input
        self.dataset = []
        self.datafile = ""
#       load from json file
        pass

    def reloadStruct(self):
        pass

    def upload(self , LossFunktion, aktiveringsFunktion, dataset):
        pass


class UserAI:
    def __init__(self, Lag, Bias, Vægte, AktiveringsFunktion, LossFunktion, Dataset, device, Epocs, LearningRate=1e-6):
   
#        if not ValidInput:
#            pass
        self.Lag = Lag
        self.Bias = Bias
        self.Vægte = Vægte
        self.LearningRate = LearningRate
        self.AktiveringsFunktion = AktiveringsFunktion
        self.LossFunktion = LossFunktion
        self.Dataset = Dataset
        self.Epocs = Epocs
        self.Loss = 0
        self.modelInfo = {}
        self.device = device
    
    def Setter(self, variableSet):
        pass

    def Getter(self, variableGet):
        pass

    def save(self):
        pass

    def load(self):
        pass
    
    def NNconstructor(self):
        for i in range(len(self.Lag)):
            self.modelInfo.update({self.Lag[i] + str(i):TorcHdata["lagTyper"][self.Lag]})

    def Run(self):
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,),(0.3081,))
        ])
        
        trainSet = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
        trainLoader = DataLoader(trainSet, batch_size=32, shuffle=True)

        self.modelInfo = collections.OrderedDict(self.modelInfo)
        model = nn.Sequential(self.modelInfo)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)

        numEpocs = 3

        model.train()
        for epoc in range(self.Epocs):
            for batchIdx, (data, target) in enumerate(trainLoader):
                data, target = data.to(device), target.to(device)

                optimizer.zero_grad()

                output = model(data)
                self.Loss = criterion(output, target)

                self.Loss.backward()
                optimizer.step()

                if batchIdx % 100 == 0:
                    print(f'epoc {epoc}, Batch {batchIdx}: Tab = {self.Loss.item():.8f}')
        
        testSet = datasets.MNIST(root='./data', train=False, transform=transform)
        testLoader = DataLoader(testSet, batch_size=1000, shuffle=False)

        dataSize = len(typing.cast(typing.Sized, testLoader.dataset))

        model.eval()
        correct = 0

        with torch.no_grad():
            for data, target in testLoader:
                data, target = data.to(device), target.to(device)

                output = model(data)

                pred = output.argmax(dim=1, keepdim=True)

                correct += pred.eq(target.view_as(pred)).sum().item()
            
            acc = 100. * correct / dataSize
            print(f'\nTest resultat: Præcision: {correct}/{dataSize} ({acc:.2f}%)\n')