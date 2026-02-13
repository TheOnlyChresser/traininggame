from data.torchDATA import TorcHdata
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import collections
import typing

# Enkel MNIST-forbehandling brugt i denne røgtestfil.
transforms = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

# Træningsloader til hurtig lokal verifikation.
train_set = datasets.MNIST(root='./data', train=True, download=True, transform=transforms)
train_loader = DataLoader(train_set, batch_size=32, shuffle=True)

# Manuel sekventiel arkitektur brugt som baselinereference.
layer_dict = collections.OrderedDict()

layer_dict.update({"Conv2d" + str(1): TorcHdata["lagTyper"]["Conv2d"](in_channels=1, out_channels=32, kernel_size=3, padding=1)})
layer_dict.update({"ReLU" + str(2): TorcHdata["aktFunktioner"]["ReLU"]()})
layer_dict.update({"MaxPool2d" + str(3): TorcHdata["lagTyper"]["MaxPool2d"](kernel_size=2, stride=2)})

layer_dict.update({"Conv2d" + str(4): TorcHdata["lagTyper"]["Conv2d"](in_channels=32, out_channels=64, kernel_size=3, padding=1)})
layer_dict.update({"ReLU" + str(5): TorcHdata["aktFunktioner"]["ReLU"]()})
layer_dict.update({"MaxPool2d" + str(6): TorcHdata["lagTyper"]["MaxPool2d"](kernel_size=2, stride=2)})

layer_dict.update({"Flatten" + str(7): TorcHdata["lagTyper"]["Flatten"]()})
layer_dict.update({"Linear" + str(8): TorcHdata["lagTyper"]["Linear"](64 * 7 * 7, 128)})
layer_dict.update({"ReLU" + str(9): TorcHdata["aktFunktioner"]["ReLU"]()})
layer_dict.update({"Linear" + str(10): TorcHdata["lagTyper"]["Linear"](128, 10)})

model = nn.Sequential(layer_dict)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 3

model.train()
for epoch in range(num_epochs):
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)

        optimizer.zero_grad()

        output = model(data)
        loss = criterion(output, target)

        loss.backward()
        optimizer.step()

        if batch_idx % 100 == 0:
            print(f'epoch {epoch}, batch {batch_idx}: loss = {loss.item():.8f}')

# Enkel evalueringsrunde på MNIST-testsplit.
test_set = datasets.MNIST(root='./data', train=False, transform=transforms)
test_loader = DataLoader(test_set, batch_size=1000, shuffle=False)

data_size = len(typing.cast(typing.Sized, test_loader.dataset))

model.eval()
correct = 0

with torch.no_grad():
    for data, target in test_loader:
        data, target = data.to(device), target.to(device)

        output = model(data)
        pred = output.argmax(dim=1, keepdim=True)

        correct += pred.eq(target.view_as(pred)).sum().item()

    acc = 100.0 * correct / data_size
    print(f'\nTest result: Accuracy: {correct}/{data_size} ({acc:.2f}%)\n')

# Hurtig formkontrol af modellens endelige output.
input_image = torch.randn(1000, 1, 28, 28)
output = model(input_image)
print(output.size())
