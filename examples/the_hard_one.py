"""
This is the hard one. I need to handle it by my own
"""
import random

import matplotlib.pyplot as plot
import time

import numpy

import layers
from core import FeedForward, Ensemble, from_csv, separate_data, noise
from core.estimators import cv


def normal(arr):
    s = numpy.sum(numpy.abs(arr))
    return numpy.round(numpy.abs(arr) / s, decimals=2)


def rand(left, right):
    return (right - left) * random.random() + left


def gen_networks(how_much=10):
    lr = 0.05
    for _ in range(how_much):
        momentum = rand(0.1, 0.2)
        weight_decay = rand(0.4, 0.65)
        nn = FeedForward(learn_rate=lr, momentum=momentum, weight_decay=weight_decay)
        nn += layers.Tanh(6, 23)
        nn += layers.Dropout(layers.Tanh(23, 28), percentage=0.3)
        nn += layers.Dropout(layers.Tanh(28, 28), percentage=0.3)
        nn += layers.Dropout(layers.Tanh(28, 28), percentage=0.3)
        nn += layers.Dropout(layers.Tanh(28, 28), percentage=0.3)
        nn += layers.Linear(28, 7)
        yield nn


training, validation = separate_data(from_csv("D:\\DELETE\\Дипломмо\\output.csv"), 0.15)

# noise(training, from_range=(0, 2), axis=0)
# noise(training, from_range=(-0.05, 0.05), axis=1)
#
# ff1 = FeedForward(learn_rate=0.05, momentum=0.2, weight_decay=0.5)
# ff1 += layers.Tanh(6, 23)
# ff1 += layers.Dropout(layers.Tanh(23, 28), percentage=0.3)
# ff1 += layers.Dropout(layers.Tanh(28, 28), percentage=0.3)
# ff1 += layers.Dropout(layers.Tanh(28, 28), percentage=0.3)
# ff1 += layers.Dropout(layers.Tanh(28, 28), percentage=0.3)
# ff1 += layers.Linear(28, 7)
#
# ff2 = FeedForward(learn_rate=0.07, momentum=0.2, weight_decay=0.23)
# ff2 += layers.Tanh(6, 23)
# ff2 += layers.Dropout(layers.Tanh(23, 28), percentage=0.3)
# ff2 += layers.Dropout(layers.Tanh(28, 28), percentage=0.3)
# ff2 += layers.Dropout(layers.Tanh(28, 28), percentage=0.3)
# ff2 += layers.Dropout(layers.Tanh(28, 28), percentage=0.3)
# ff2 += layers.Linear(28, 7)
#
# ff3 = FeedForward(learn_rate=0.04, momentum=0.6, weight_decay=0.4)
# ff3 += layers.Tanh(6, 23)
# ff3 += layers.Dropout(layers.Sigmoid(23, 28), percentage=0.3)
# ff3 += layers.Dropout(layers.Sigmoid(28, 28), percentage=0.3)
# ff3 += layers.Dropout(layers.Sigmoid(28, 28), percentage=0.3)
# ff3 += layers.Dropout(layers.Sigmoid(28, 28), percentage=0.3)
# ff3 += layers.Linear(28, 7)

ensemble = Ensemble(*gen_networks(how_much=1))

test = (
    [10, 12, 0, 0, 3, 17],
    [5, 8, 0, 0, 5, 21],
    [10, 0, 15, 0, 6, 11],
)

error = []
v_error = []
mean_error = 0
print("Training starts...")
prev = time.time()
for i in range(1200):
    r = random.randint(0, len(training) - 1)
    ensemble.fit(*training[r])
    error.append(ensemble.error)

    if i % 10 == 0:
        v_error.append(cv(ensemble, validation))
    if i > 1000:
        mean_error += v_error[-1]

print(f"Training is finished! Spend time: {time.time() - prev:.2f}")
print(f"Mean validation error: {mean_error / (len(error) - 1000)}")

for t in test:
    print(f"{t} -> {normal(ensemble.get(t)) * 50}")

plot.title("Learning error")
plot.plot(error)
plot.plot([i * 10 for i in range(len(v_error))], v_error)
plot.show()