
"""
Model hybrid TCAT fuel consumption
"""

import math
import numpy as np

POINTS = "../../data/example/points.csv"
STOPS = "../../data/example/stops.csv"


class State:

	# initialize State
    def __init__(self, speed, grade, battery):
    	self.battery = battery
    	self.grade = grade
    	self.speed = speed


    # copy state
    def copy(self):
    	return State(self.speed, self.grade, self.battery)

class Interval:
	def __init__(self, es, s, endtime, dist):
		self.endStop = es
		self.startTime = s
		self.endTime = endtime
		self.dist = dist
		self.v = 0
		self.accelTime = 0
		self.brakeTime = 0
	def __repr__(self):
		return "sn:%d\tst:%d\tet:%d\td:%d" % (self.endStop, self.startTime, self.endTime,self.dist)

class Point:
	def __init__(self, x, y, dist, elev):
		self.x = x
		self.y = y
		self.dist = dist
		self.elev = elev
		self.isStop = False
		self.stopNum = -1
		self.stopTime = -1

	def __repr__(self):
		return "(%d,%d)\tnum:%d\tst:%d\tdist:%d\tstoptime:%d" % ( self.x, self.y, self.stopNum, self.stopTime,self.dist,self.stopTime)

class Route:
	def __init__(self, routeStartTime, routeTotalTime, allpts, stopTimes, intervals):
		self.routeStartTime = routeStartTime
		self.allpts = allpts
		self.stopTimes = stopTimes
		self.intervals = intervals
		self.routeTotalTime = routeTotalTime


# process route
def makeRoute(pointsFile, timesFile):

	allpts = [] # array of Point data structures with input data
	routeStartTime = 0 # start time in seconds of route
	stopTimes = [] # array of stop times, including 0
	intervals = [] # array of intervals in which v is constant
	routeEndTime = 0
	# read in all normal points
	with open(pointsFile) as f:
		lines = f.readlines()
		for l in lines:
			pt = l.strip().split(',')
			newpt = Point(
				int(pt[0]), 
				int(pt[1]), 
				int(pt[2]), 
				int(pt[3]))
			if pt[4] != "":
				newpt.isStop = True
				newpt.stopNum = int(pt[4])
			allpts.append(newpt)


	# read in stop times
	with open(timesFile) as f:
		lines = f.readlines()

		p = 0 # index of point in allpts; reading thru allpts to find matching busstop id
		for l in lines: # last point refers to closing cycle
			num,time = [int(x) for x in l.strip().split(',')]
			intervalDistance = -allpts[p].dist

			# print("%d, %d"% (allpts[p].stopNum, num))
			# search allpts until we find the stop with matching stopnum
			while (p < len(allpts) and allpts[p].stopNum != num):
				# print("p:%d, p+1:%d"% (p,p+1))	
				intervalDistance += allpts[p].dist
				p += 1
			
			# print("stop to anlayz %d" % p)	
			# ran out of points; time to link back to first stop again
			if p == len(allpts):
				if num != 0:
					print ("invalid cycle closure in stoptimes")
					break
				else:
					src = allpts[0]
					newpt = Point(src.x, src.y,  src.dist,src.elev)
					newpt.stopNum = num
					newpt.stopTime = time - routeStartTime
					newpt.isStop = True
					# print("making new pt %s" %str(newpt))
					routeTotalTime = time - routeStartTime
					allpts.append(newpt)
			
			intervalDistance += allpts[p].dist
			# print(intervalDistance)


			# sketchy check for first stop
			if p == 0:
				routeStartTime = time * 60

			# time since route started
			allpts[p].stopTime = time * 60 - routeStartTime
			stopTimes.append(allpts[p].stopTime)

			# even sketchier check for non-first stop
			if len(stopTimes) > 1:
				lastStopTime = stopTimes[-2]
				thisStopTime = stopTimes[-1]

				interval = Interval(allpts[p].stopNum, lastStopTime, thisStopTime, intervalDistance)
				# print ("distance:%d" % intervalDistance)
				intervals.append(interval)
				# print(interval)
			# p+=1

	print("=======")
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
		c = interval.dist

		roots = np.roots([a,b,c])
		print(roots)

	# for sec in range(route.routeTotalTime):
	# 	if sec > interval.endTime:
	# 		intervalid +=1
	# 		interval = route.intervals[intervalid]

	# return timeline

# calculate fuel consumption at every second
def fuelConsumed(timeline):
	fuel = 0
	for t in timeline:
		pass
	return fuel

velocity(makeRoute(POINTS, STOPS), 1,2)