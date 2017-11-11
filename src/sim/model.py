"""
Model hybrid TCAT fuel consumption
"""

import math
import numpy as np
import json
import pandas
from itertools import chain
from copy import deepcopy
from src import constants as c


'''
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
    def __init__(self, max_acc, max_dec):
        self.max_acc = max_acc
        self.max_dec = max_dec

    def run(self, path, duration):
        '''returns a list of states, one per second, with duration+1 elements.

        path is a Path object, durration is time in seconds (int)
        stopped in first and last states
        '''
        dist = self.path.distance()
        
        # solving a quadratic, ignore lesser value
        a = -0.5
        b = duration * self.max_acc * self.max_dec
        c = dist * self.max_acc * self.max_dec
        max_speed = (-b + math.sqrt(b**2 - 4 * a * c))/(2*a)
        
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
            if not(internal_state['is_diesl']) & internal_state['battery'] >= W & c.POWER_CAP_ELECTRIC >= power:
                new_internal_state['battery'] = new_internal_state['battery'] - (1/c.ELECTRIC_ENGINE_EFFICIENCY)*W
            #use fuel
            else:
                new_internal_state['fuel-used'] = new_internal_state['fuel-used'] + (1/c.DIESEL_ENGINE_EFFICIENCY)*W
                new_internal_state['battery'] += c.BATTERY_CHARGE_FROM_DIESEL
        else:
            #charge battery
            if not(internal_state['is_diesl']) & internal_state['battery'] < c.BATTERY_CAP:
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
        self.path = path
        self.driver = driver
        self.schedule = schedule
        self.engine = engine

    def _run_sim(self, external_states, tick_function, start_state):
        '''a helper function for simulating a list of states'''
        internal_state = start_state
        for external_state in external_states:
            internal_state = tick_function(internal_state, state)
        return internal_state

    def run(self, is_diel, init_electricity=0):
        start_state = {
                'is_diel': is_diel,
                'fuel_used': 0,
                'electricity': init_electricity,
        }
        states = RoutePlanner(self.path, self.schedule, self.driver).run()
        return self._run_sim(states, engine.tick_time, start_state)

