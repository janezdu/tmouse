import json
import sys
import numpy as np
import matplotlib.pyplot as plt

def speedPlotter(fo):
    data = json.load(fo)

    val = [obj['external_state']['speed'] for obj in data]
    x = np.arange(len(val))

    fig, ax = plt.subplots()
    ax.stackplot(x,val)
    plt.show()



def heatMapBasic(fo, val):
    '''relies on schema wiht lat, lon, some other value to plot'''

    data = json.load(fo)

    val = [obj[val] for obj in data]

    x = np.arange(len(val))

    fig, ax = plt.subplots()
    ax.stackplot(x,val)
    plt.show()

heatMapStates(open(sys.argv[1]))