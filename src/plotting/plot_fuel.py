import json
import sys
import numpy as np
import matplotlib.pyplot as plt

RESULTSPATH = 'results'

def areaGraph(data, val, routenum, engtype):
    y = [obj[val] for obj in data]
    x = np.arange(len(y))

    fig, ax = plt.subplots()
    ax.stackplot(x, y)
    plt.savefig(RESULTSPATH + '/' +'%s_%s_%s.png'%(val, routenum, engtype))
    # plt.show()

def incrementalFuel(data, routenum, engtype):
    fuel = [obj['fuel_used'] for obj in data]

    y = [fuel[i]- fuel[i-1] for i in range(1,len(fuel)-1)]
    x = np.arange(len(y))

    fig, ax = plt.subplots()
    ax.stackplot(x, y)
    plt.savefig(RESULTSPATH + '/' + 'incr_fuel_%s_%s.png'%(routenum, engtype))
    # plt.show()

def lineGraph(data, val, routenum, engtype):
    y = [obj[val] for obj in data]
    x = np.arange(len(y))

    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.savefig(RESULTSPATH + '/' +'%s_%s_%s.png'%(val,routenum, engtype))
    # plt.show()


routenums = ['10', '11', '15','82']
engines = ['hybrid', 'diesl']

for num in routenums:
    for eng in engines:
        with open('tmp/route_%s/simulator_results_external_%s.json'%(num, eng)) as fo:
            data = json.load(fo)
            lineGraph(data, 'acceleration', num, eng)
            areaGraph(data, 'grade', num, eng)
            lineGraph(data, 'speed', num, eng)

        with open('tmp/route_%s/simulator_results_internal_%s.json'%(num, eng)) as fo:
            data = json.load(fo)
            incrementalFuel(data, num, eng)
            areaGraph(data, 'battery', num, eng)