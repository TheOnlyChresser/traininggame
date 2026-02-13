from data.torchDATA import TorcHdata
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import collections
import typing

transforms = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,),(0.3081,))
])

trainSet = datasets.MNIST(root='./data', train=True, download=True, transform=transforms)
trainLoader = DataLoader(trainSet, batch_size=32, shuffle=True)

arr = [1,5,3,5,62,7,2,2,4,6,7,3,525,7,9,785,674,643,52,9]

dict = collections.OrderedDict()

dict.update({"Conv2d" + str(1):TorcHdata["lagTyper"]["Conv2d"](in_channels=1, out_channels=32, kernel_size=3, padding=1)})
dict.update({"ReLU" + str(2):TorcHdata["aktFunktioner"]["ReLU"]()})
dict.update({"MaxPool2d" + str(3):TorcHdata["lagTyper"]["MaxPool2d"](kernel_size=2, stride=2)})

dict.update({"Conv2d" + str(4):TorcHdata["lagTyper"]["Conv2d"](in_channels=32, out_channels=64, kernel_size=3, padding=1)})
dict.update({"ReLU" + str(5):TorcHdata["aktFunktioner"]["ReLU"]()})
dict.update({"MaxPool2d" + str(6):TorcHdata["lagTyper"]["MaxPool2d"](kernel_size=2, stride=2)})

dict.update({"Flatten" + str(7):TorcHdata["lagTyper"]["Flatten"]()})
dict.update({"Linear" + str(8):TorcHdata["lagTyper"]["Linear"](64*7*7,128)})
dict.update({"ReLU" + str(9):TorcHdata["aktFunktioner"]["ReLU"]()})
dict.update({"Linear" + str(10):TorcHdata["lagTyper"]["Linear"](128,10)})

model = nn.Sequential(dict)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

numEpocs = 3

model.train()
for epoc in range(numEpocs):
    for batchIdx, (data, target) in enumerate(trainLoader):
        data, target = data.to(device), target.to(device)

        optimizer.zero_grad()

        output = model(data)
        loss = criterion(output, target)

        loss.backward()
        optimizer.step()

        if batchIdx % 100 == 0:
            print(f'epoc {epoc}, Batch {batchIdx}: Tab = {loss.item():.8f}')

testSet = datasets.MNIST(root='./data', train=False, transform=transforms)
testLoader = DataLoader(testSet, batch_size=1000, shuffle=False)

dataSize = len(typing.cast(typing.Sized, testLoader.dataset))

model.eval()
testLoss = 0
correct = 0

with torch.no_grad():
    for data, target in testLoader:
        data, target = data.to(device), target.to(device)

        output = model(data)

        pred = output.argmax(dim=1, keepdim=True)

        correct += pred.eq(target.view_as(pred)).sum().item()
    
    acc = 100. * correct / dataSize
    print(f'\nTest resultat: Præcision: {correct}/{dataSize} ({acc:.2f}%)\n')


inputImage = torch.randn(1000,1,28,28)
output = model(inputImage)
print(output.size())
