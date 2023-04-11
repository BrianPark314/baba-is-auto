import torch
from torch import nn, optim
import torch.nn.functional as F
from torch.distributions import Categorical

import copy

import gym
import environment  # lgtm[py/unused-import]
import pyBaba
import os
from tensorboardX import SummaryWriter

os.chdir(os.path.dirname(os.path.abspath(__file__)))

device = torch.device('mps:0' if torch.backends.mps.is_available() else 'cpu')
print (f"PyTorch version:{torch.__version__}") # 1.12.1 이상
print(f"MPS device built: {torch.backends.mps.is_built()}") # True 여야 합니다.
print(f"MPS device available: {torch.backends.mps.is_available()}") # True 여야 합니다.

env = gym.make('baba-babaisyou-v0')