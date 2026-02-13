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
        "GRU":nn.GRU,
        "LSTMCell":nn.LSTMCell,
        "SyncBatchNorm":nn.SyncBatchNorm,
        "RMSNorm":nn.RMSNorm,
        "CircularPad1d":nn.CircularPad1d,
        "ConstantPad1d":nn.ConstantPad1d,
        "ZeroPad1d":nn.ZeroPad1d,
        "MaxPool1d":nn.MaxPool1d,
        "MaxPool2d":nn.MaxPool2d,
        "AvgPool1d":nn.AvgPool1d,
        "FractionalMaxPool2d":nn.FractionalMaxPool2d,
        "AdaptiveMaxPool1d":nn.AdaptiveMaxPool1d,
        "LazyConv2d":nn.LazyConv2d,
        "ConvTranspose2d":nn.ConvTranspose2d,
        "LazyConvTranspose2d":nn.LazyConvTranspose2d,
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

