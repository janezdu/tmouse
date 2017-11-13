import json
import sys
import numpy as np
import matplotlib.pyplot as plt

def speedPlotter(fo):
    data = json.load(fo)

    val = [obj['external_state']['speed'] for obj in data]
    lat = [obj['external_state']['lat'] for obj in data]
    lon = [obj['external_state']['lon'] for obj in data]
    x = np.arange(len(val))

    fig, ax = plt.subplots()
    ax.scatter(lat, lon)
    plt.show()



def heatMapBasic(fo, val):
    '''relies on schema wiht lat, lon, some other value to plot'''
    data = json.load(fo)
    val = [obj[val] for obj in data]
    lat = [obj['lat'] for obj in data]
    lon = [obj['lon'] for obj in data]
    
    x = np.arange(len(val))

    fig, ax = plt.subplots()
    ax.scatter(x,val)
    plt.show()

speedPlotter(open(sys.argv[1]))