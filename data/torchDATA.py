import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR  ### temp 
import math

TorcHdata = {
    "lagTyper":{
        "Conv2d":nn.Conv2d,
        "Transformer":nn.Transformer,
        "Dropout":nn.Dropout,
        "Linear":nn.Linear,
        "RNN":nn.RNN,
        "AvgPool1d":nn.AvgPool1d,
        "Flatten":nn.Flatten
    },
    "lossFunktioner":{
        "L1Loss":nn.L1Loss,
        "MSELoss":nn.MSELoss,
        "GaussianNLLLoss":nn.GaussianNLLLoss,
        "HuberLoss":nn.HuberLoss,
        "CosineEmbeddingLoss":nn.CosineEmbeddingLoss,
        "BCEWithLogitsLoss":nn.BCEWithLogitsLoss,
        "CTCLoss":nn.CTCLoss,
        "KLDivLoss":nn.KLDivLoss,
        "CrossEntropyLoss":nn.CrossEntropyLoss,
    },
    "aktFunktioner":{
        "ELU":nn.ELU,
        "LeakyReLU":nn.LeakyReLU,
        "LogSigmoid":nn.LogSigmoid,
        "ReLU":nn.ReLU,
        "Softmax":nn.Softmax,
        "Tanh":nn.Tanh,
    },
    "optimizer":{
        "Adam":optim.Adam,
        "ASGD":optim.ASGD,
        "RMSprop":optim.RMSprop,
        "SGD":optim.SGD,
        "RAdam":optim.RAdam,
        "adagrad":optim.Adagrad
    }
}

