import torch
from torch import nn, optim
import torch.nn.functional as F
from torch.distributions import Categorical

import copy

import gym
import environment  # lgtm[py/unused-import]
import pyBaba
import os
import gc
from tensorboardX import SummaryWriter

gc.collect()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#device = torch.device('mps:0' if torch.backends.mps.is_available() else 'cpu')
device = torch.device('cpu')
print (f"PyTorch version:{torch.__version__}") # 1.12.1 이상
print(f"MPS device built: {torch.backends.mps.is_built()}") # True 여야 합니다.
print(f"MPS device available: {torch.backends.mps.is_available()}") # True 여야 합니다.

env = gym.make('baba-babaisyou-v0')


class Network(nn.Module):
    def __init__(self):
        super(Network, self).__init__()

        self.conv1 = nn.Conv2d(pyBaba.Preprocess.TENSOR_DIM, 128, 3, padding=1)
        self.conv2 = nn.Conv2d(128, 128, 3, padding=1)
        self.conv3 = nn.Conv2d(128, 128, 3, padding=1)
        self.conv4 = nn.Conv2d(128, 128, 3, padding=1)
        self.conv5 = nn.Conv2d(128, 1, 1, padding=0)
        self.fc = nn.Linear(99, 4)

        self.log_probs = []
        self.rewards = []

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        x = F.relu(self.conv5(x))

        x = x.view(x.data.size(0), -1)
        x = self.fc(x)

        return F.softmax(x, dim=1)


net = Network().to(device)

opt = optim.Adam(net.parameters(), lr=1e-4)


def get_action(state):
    state = torch.tensor(state).to(device)

    policy = net(state)

    m = Categorical(policy)
    action = m.sample()

    net.log_probs.append(m.log_prob(action))
    return env.action_space[action.item()]



def train():
    R = 0

    loss = []
    returns = []

    for r in net.rewards[::-1]:
        R = r + 0.99 * R
        returns.insert(0, R)

    returns = torch.tensor(returns)
    returns = (returns - returns.mean()) / (returns.std() + 1e-3)

    for prob, R in zip(net.log_probs, returns):
        loss.append(-prob * R)

    opt.zero_grad()

    loss = torch.cat(loss).sum()
    loss.backward()

    opt.step()

    del net.log_probs[:]
    del net.rewards[:]


if __name__ == '__main__':
    writer = SummaryWriter()

    global_step = 0

    for e in range(1000):
        score = 0

        state = env.reset().reshape(1, -1, 9, 11)

        step = 0
        while step < 200:
            global_step += 1

            action = get_action(state)

            env.render()

            next_state, reward, done, _ = env.step(action)
            next_state = next_state.reshape(1, -1, 9, 11)

            net.rewards.append(reward)
            score += reward
            state = copy.deepcopy(next_state)

            step += 1

            if env.done:
                break

        train()

        writer.add_scalar('Reward', score, e)
        writer.add_scalar('Step', step, e)

        print(
            f'Episode {e}: score: {score:.3f} time_step: {global_step} step: {step}')
