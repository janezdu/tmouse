"""
Model hybrid TCAT fuel consumption
"""

import math
import numpy as np
import json
#import pandas
from itertools import chain
from copy import deepcopy
import constants as c


"""
An internal_state object is given in the following form:
    {
        is_diesl: bool
        battery: float
        fuel_used: float
    }

An external_state object is given in the following form:
    {
        grade: float
        speed: float
        acceleration: float
    }
"""

class Path:
    '''a representation of a path through space

    includes elevation, many lat and lon points

    must be a loop unless it is a single path between only two stations

    A must be the first station

    supports tagging points as stations and helper functions on the path'''
    def __init__(self, lst_points):
        '''lst_points is the output of the path importer'''
        self.points = lst_points

    def distance(self, type='3d'):
        '''gets the distance of a point from the start (the first pt)

        type can be 3d or 2d
        '''
        return sum([pt[type+'_dist'] for pt in self.points])

    def grade_at_distance(self, target, type='3d'):
        '''gets the grade at a certain distance

        target is the distance from the start of the loop to measure the
        grade at

        type can be 3d or 2d, specifying how the target distance is measured
        '''
        dist = 0
        for i,pt in enumerate(self.points[1:]):
            dist += pt[type+'_dist']
            if dist >= target:
                left_point_index = i-1
                break
        l_pt = self.points[left_point_index]
        r_pt = self.points[left_point_index+1]
        if r_pt['2d_dist']:
            return (r_pt['elevation'] - l_pt['elevation']) / r_pt['2d_dist']
        else:
            return 0

    def get_intervals(self, stations=None):
        '''returns a smaller path objects for each interval,

        where each interval is a labeled station

        if stations is provided then only those stations are considered
        real stations, (A) must be included
        '''
        index_A = [i for i,x in enumerate(self.points) if x['stop'] == 'A'][0]
        new_pts = self.points[index_A:] + self.points[:index_A]

        intervals = []
        cur_interval = []
        for pt in new_pts:
            if pt['stop'] \
                        and (stations is None or pt['stop'] in stations) \
                        and cur_interval:
                intervals.append(Path(cur_interval))
                cur_interval = [pt]
            else:
                cur_interval.append(pt)

        cur_interval.append(new_pts[0])
        intervals.append(Path(cur_interval))
        return intervals


    #@staticmethod()
    #def from_file()

class Schedule:
    def __init__(self, table):
        '''table should be a list of (label, time) tuples

        time can be a string like '0715', or a relative num of minutes
        '''
        for i,(_,t) in enumerate(table):
            if type(t) == str:
                table[i][1] = int(t[:2]) * 60 + int(t[2:])
        self.table = table

    def get_stops(self):
        '''gets the stops on this schedule'''
        return [x for x,_ in self.tables]

    def duration(self, stop):
        '''returns the time to get to stop from the previous station

        only defined on stations after the first
        '''
        last = None
        for label,time in self.table:
            if label == stop:
                return time - last
            else:
                last = time

    def get(self, i):
        '''gets the duration between ()i-1)-th station and i-th station'''
        return self.duration(self.table[i][0])


class SimpleDriver:
    '''A representation of a driver who accelerates, cruses, and
    breaks to arrive on time

    The driver accelerates at a constant speed to reach x, then slows at
    a constant speed to stop at the station exactly on time, varrying x to
    acchieve this.
    '''
    def __init__(self, max_acc=None, max_dec=None):
        self.max_acc = max_acc if max_acc else c.SIMPLE_DRIVER_ACCELERATION
        self.max_dec = max_dec if max_dec else c.SIMPLE_DRIVER_DECELERATION

    def run(self, path, duration):
        '''returns a list of external states, one per second, with duration+1 elements.

        path is a Path object, durration is time in seconds (int)
        stopped in first and last states
        '''
        dist = path.distance()

        # solving a quadratic, ignore lesser value
        a = -0.5
        b = duration * self.max_acc * self.max_dec
        c = dist * self.max_acc * self.max_dec
        max_speed = (-b - math.sqrt(b**2 - 4 * a * c))/(2*a)

        # make external state for every time step
        def get_state(t):
            speed = min(self.max_acc * t, max_speed)
            if speed < max_speed:
                # still acc
                acc = self.max_acc
                loc = 0.5 * self.max_acc**2 * t
            else:
                speed = min(speed, self.max_dec * (duration - t))
                if speed < max_speed:
                    # now dec
                    acc = - self.max_dec
                    loc = dist - (0.5 * self.max_dec**2 * (duration - t))
                else:
                    # crusing
                    acc = 0
                    acc_time = max_speed / self.max_acc
                    loc = max_speed * (t - 0.5 * acc_time)

            return {
                    'grade': path.grade_at_distance(loc),
                    'speed': speed,
                    'acceleration': acc
            }

        return [get_state(t) for t in range(duration+1)]


class RoutePlanner:
    '''a class for converting a router's description to a set of states

    accepts an input of a driver to model how the bus moves
    '''
    def __init__(self, path, schedule, driver):
        '''accepts a path, the accompaning schedule, and a driver function

        the driver function accepts (sub_path, time) where sub_path is a
        Path object along an interval, and time is the duration the bus has
        to get from start to end
        '''
        self.path = path
        self.schedule = schedule
        self.driver = driver

    def run(self):
        ''''''
        intervals = self.path.get_intervals()
        state_intervals = [
                self.driver(sub_path, self.schedule.get(i+1))
                for i,sub_path in enumerate(intervals)
        ]
        return chain(*state_intervals)


class Engine:
    '''a model of how an external_state affects the internal state

    Takes in an external state (accelleration, grade, speed) and a current
    internal state (electricity levels) and computes the next time step,
    one second later
    '''
    def tick_time(self, internal_state, external_state):
        '''this calculates the effect of one time step on the internal_state

        returns a new internal state
        '''
        #TODO
        dt = 1

        new_internal_state = internal_state


        #calculate power needed
        #time is 1 second, d = rt
        a = external_state['acceleration']
        dist = external_state['speed']*dt
        grade = external_state['grade']
        theta = np.arctan(grade)
        m = c.MASS

        #if going uphill or flat

        F = m * c.g * np.sin(theta) + m * a
        # integrate
        W = F * dist
        # power = work/time. t=1
        power = W/dt

        print(power)

        #where does that power come from or go?

        #if force positive, we're using engine, either battery or diesel
        if F > 0:
            #use battery
            if not internal_state['is_diesl'] and (internal_state['battery'] >= W) and (c.POWER_CAP_ELECTRIC >= power):
                print('here')
                new_internal_state['battery'] = new_internal_state['battery'] - (1/c.ELECTRIC_ENGINE_EFFICIENCY)*W
            #use fuel
            else:
                new_internal_state['fuel_used'] = new_internal_state['fuel_used'] + (1/c.DIESEL_ENGINE_EFFICIENCY)*W
                if not internal_state['is_diesl']:
                    new_internal_state['battery'] += c.BATTERY_CHARGE_FROM_DIESEL
        else:
            #charge battery
            if not internal_state['is_diesl'] and (internal_state['battery'] < c.BATTERY_CAP):
                new_internal_state['battery'] = min(new_internal_state['battery'] + c.MAX_BATTERY_CHARGE_RATE*dt,
                                                    c.BATTERY_CAP, new_internal_state['battery'] - W)
                #-W becasue force is negative here and want to add to battery

                # if power <= c.MAX_BATTERY_CHARGE_RATE:
                #     new_internal_state['battery'] = min(new_internal_state['battery'] + W, c.BATTERY_CAP)
                # else:
                #     new_internal_state['battery'] = min(new_internal_state['battery'] + c.MAX_BATTERY_CHARGE_RATE, c.BATTERY_CAP)

        return new_internal_state


class Simulator:
    def __init__(self, path, driver, schedule, engine):
        '''creates a new simulation ready to be run for a choice of car

        schedule is a list of times at which A,B,C,etc stations are reached
        '''
        self.path = path
        self.driver = driver
        self.schedule = schedule
        self.engine = engine

    def _run_sim(self, external_states, tick_function, start_state):
        '''a helper function for simulating a list of states'''
        internal_state = start_state
        for external_state in external_states:
            internal_state = tick_function(internal_state, external_state)
        return internal_state

    def run(self, is_diel, init_electricity=0):
        '''runs the internal state'''
        start_state = {
                'is_diel': is_diel,
                'fuel_used': 0,
                'electricity': init_electricity,
        }
        states = RoutePlanner(self.path, self.schedule, self.driver).run()
        return self._run_sim(states, self.engine.tick_time, start_state)

