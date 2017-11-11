"""
Model hybrid TCAT fuel consumption
"""

import math
import numpy as np
import json
import pandas
from itertools import chain
from functiontools import reduce
from copy import deepcopy
from src import constants as c


'''
An internal_state object is given in the following form:
    {
        isDiesel: bool
        battery: float
        fuel_used: float
    }

An external_state object is given in the following form:
    {
        grade: int
        speed: float
        acceleration: float
    }
'''

class Path:
    def __init__(self, lst_points):
        '''lst_points is the output of the path importer'''
        self.points = lst_points

    def distance(self, type='3d'):
        return sum([pt[type+'_dist'] for pt in self.points])

    def grade_at_distance(self, target, type='3d'):
        dist = 0
        for i,pt in enumerate(self.points{1:]):
            dist += pt[type+'_dist']
            if dist >= target:
                left_point_index = i-1
                break
        l_pt = self.points[left_point_index]
        r_pt = self.points[left_point_index+1]
        return (r_pt['elevation'] - l_pt['elevation']) / r_pt['2d_dist']

    def get_intervals(self):
        '''returns a smaller path objects for each interval'''
        index_A = [i for i,x in enumerate(self.points) if x['stop'] == 'A'][0]
        new_pts = self.points[index_A:] + self.points[:index_A]
        
        intervals = []
        cur_interval = []
        for pt in new_pts:
            if pt['stop'] and cur_interval:
                intervals.append(Path(cur_interval))
                cur_interval = [pt]
            else:
                cur_interval.append(pt)

        cur_interval.append(new_pts[0])
        intervals.append(Path(cur_interval))
        return intervals


class SimpleDriver:
    def __init__(self, path, duration, max_speed):
        '''path is a Path object, durration is time in seconds (int)'''
        self.path = path
        self.duration = duration
        self.max_speed = max_speed

    def run(self):
        '''returns a list of states, one per second, with duration+1 elements.

        stopped in first and last states
        '''
        dist = self.path.distance()
        # TODO


class RoutePlanner:
    '''a class for converting a router's description to a set of states'''
    def __init__(self, path, schedule, driver):
        self.path = path
        self.schdule = schedule
        self.driver = driver

    def run(self):
        intervals = self.path.get_intervals()
        state_intervals = [
                driver(sub_path,time)
                for sub_path,time in zip(intervals,schedule)
        ]
        return chain(*state_intervals)


class Engine:
    def tick_time(self, internal_state, external_state):
        #TODO
        dt = 1

        new_internal_state = internal_state


        #calculate power needed
        #time is 1 second, d = rt
        a = external_state['acceleration']
        dist = external_state['speed']*dt
        theta = external_state['angle']
        m = c.MASS

        #if going uphill or flat
        if theta >= 0:
            F = m * c.g * np.cos(theta) + m * a
            # integrate
            W = F * dist
            # power = work/time. t=1
            power = W/dt
        else:
            F = -1 * m * c.g * np.cos(theta) + m * a
            W = F * dist
            power = W/dt

        #where does that power come from or go?

        #if force positive, we're using engine, either battery or diesel
        if F > 0:
            #use battery
            if not(internal_state['isDiesel']) & internal_state['battery'] >= W & c.POWER_CAP_ELECTRIC >= power:
                new_internal_state['battery'] = new_internal_state['battery'] - (1/c.ELECTRIC_ENGINE_EFFICIENCY)*W
            #use fuel
            else:
                new_internal_state['fuel-used'] = new_internal_state['fuel-used'] + (1/c.DIESEL_ENGINE_EFFICIENCY)*W
                new_internal_state['battery'] += c.BATTERY_CHARGE_FROM_DIESEL
        else:
            #charge battery
            if not(internal_state['isDiesel']) & internal_state['battery'] < c.BATTERY_CAP:
                new_internal_state['battery'] = min(new_internal_state['battery'] + c.MAX_BATTERY_CHARGE_RATE*dt,
                                                    c.BATTERY_CAP, new_internal_state['battery'] - W)
                #-W becasue force is negative here and want to add to battery

                # if power <= c.MAX_BATTERY_CHARGE_RATE:
                #     new_internal_state['battery'] = min(new_internal_state['battery'] + W, c.BATTERY_CAP)
                # else:
                #     new_internal_state['battery'] = min(new_internal_state['battery'] + c.MAX_BATTERY_CHARGE_RATE, c.BATTERY_CAP)

        return new_internal_state


class Simulator:
    def __init__(self, path, schedule, engine):
        self.states = states
        self.tick_function = tick_function

    def _run_sim(self, states, tick_function):
        '''a helper function for simulating a list of states'''
        pass

    def run(self):
        #TODO
        return {
                'fuel_used': 5
        }


# process route
def makeRoute(pointsFile, timesFile):
	"""each arg is a file-like object"""

	allpts = json.load(pointsFile)
	# allpts = [] # array of Point data structures with input data
	routeStartTime = 0 # start time in seconds of route
	# stopTimes = [] # array of stop times, including 0
	intervals = [] # array of intervals in which v is constant
	routeEndTime = 0
	# read in all normal points
	# with open(pointsFile) as f:
	# 	lines = f.readlines()
	# 	for l in lines:
	# 		pt = l.strip().split(',')
	# 		newpt = Point(
	# 			int(pt[0]), 
	# 			int(pt[1]), 
	# 			int(pt[2]), 
	# 			int(pt[3]))
	# 		if pt[4] != "":
	# 			newpt.isStop = True
	# 			newpt.stopNum = int(pt[4])
	# 		allpts.append(newpt)


	# read in stop times
	with open(timesFile) as f:
		lines = f.readlines()

		p = 0 # index of point in allpts; reading thru allpts to find matching busstop id
		for l in lines: # last point refers to closing cycle
			# num,time = [int(x) for x in l.strip().split(',')]
			numr,timer = l.strip().split(',')
			num = int(numr)
			time = float(timer)

			intervalDistance = -allpts[p].dist

			# search allpts until we find the stop with matching stopnum
			while (p < len(allpts) and allpts[p].stopNum != num):
				intervalDistance += allpts[p].dist
				p += 1
			
			# ran out of points; time to link back to first stop again
			if p == len(allpts):
				if num != 0:
					print ("invalid cycle closure in stoptimes")
					break
				else:
					newpt = deepcopy(allpts[0])
					newpt["stop"] = num
					# newpt[""] = time* 60 - routeStartTime
					routeTotalTime = int(time*60 - routeStartTime)
					allpts.append(newpt)
			
			intervalDistance += allpts[p]["3d_dist"]
			# print(intervalDistance)


			# sketchy check for first stop
			if p == 0:
				routeStartTime = time * 60

			# time since route started
			# allpts[p].stopTime = time * 60 - routeStartTime
			stopTimes.append(allpts[p].stopTime)

			# even sketchier check for non-first stop
			if len(stopTimes) > 1:
				lastStopTime = stopTimes[-2]
				thisStopTime = stopTimes[-1]

				interval = Interval(allpts[p].stopNum, lastStopTime, thisStopTime, intervalDistance)
				intervals.append(interval)

	print("=======")
	print ("total time %d" % routeTotalTime)
	for i in intervals:
		print (i)
	for p in allpts:
		print(p)
	print("=======")

	return Route(routeStartTime, routeTotalTime, allpts, stopTimes, intervals)


# caluclate velocity at every second
def velocity(route, accel, brake):
	timeline = []

	
	intervalid = 0
	interval = route.intervals[intervalid]

	for iv in route.intervals:

		a = (-0.5)*(1/accel + 1/brake)
		b = (iv.endTime - iv.startTime)
		c = -interval.dist
		print(a,b,c)

		print(np.roots([a,b,c]))
		interval.v = max(np.roots([a,b,c]))
		interval.accelTime = interval.v / accel
		interval.brakeTime = interval.v / brake

	for r in (route.intervals):
		print("speed:%d, acceltime:%d, deceltime:%d, cruisetime:%d" % (interval.v, interval.accelTime, interval.brakeTime,
			interval.endTime - interval.startTime - interval.accelTime - interval.brakeTime))

	# for sec in range(route.routeTotalTime):
		
	# 	state = State(0,0,0)
	# 	print(interval)
	# 	if sec > interval.endTime:
	# 		intervalid +=1
	# 		interval = route.intervals[intervalid]
	# 	else:
	# 		if sec > interval.startTime and sec < interval.accelTime:

	# 			print("%d: accelerating" % sec)
	# 			velocity = (sec - interval.startTime) * accel
	# 		elif sec > interval.startTime + interval.accelTime and sec < interval.endTime - interval.brakeTime:
	# 			print("%d: cruising"%sec)
	# 			velocity = interval.v
	# 		elif sec > interval.endTime - interval.brakeTime and sec < interval.endTime:
	# 			print("%d: decelerating"%sec)
	# 			minusblock = interval.endTime - interval.startTime - interval.brakeTime
	# 			decelTime = sec - interval.startTime - minusblock
	# 			velocity = interval.v - decelTime * brake
	# 		timeline.append(state)
	# 		print(state)

	return timeline

# calculate fuel consumption at every second
def fuelConsumed(timeline):
	fuel = 0
	for t in timeline:
		pass
	return fuel


# for t in velocity(makeRoute(POINTS, STOPS), 1,2):
# 	print (t)
velocity(makeRoute(POINTS, STOPS), 2,2)
