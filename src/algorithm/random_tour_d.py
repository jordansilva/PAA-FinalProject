#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: Jordan Silva <@jordansilva>
# Created: December 10th 2015

import json
import os
import time
import sys
import math
import random
from datetime import timedelta, time

class RandomTourD:

  PERCENTAGE_CUT = 0.5

  def __init__(self, graph):
    self.graph        = graph
    self.period       = None

  def execute(self, period):
    self.solution = None
    self.period   = period

    # print '\n### Random Tour D ###'
    # print '[ Start Hour ] %s' % self.period[0]
    # print '[ Final Hour ] %s\n' % self.period[1]

    #construct
    pois = self.get_most_valuable_places(current = None, places = [], cut = self.PERCENTAGE_CUT)
    self.solve(places=pois, time = self.period[0])
    # self.solve(places=self.graph.vertices, time = self.period[0])
    
    points     = self.solution[1]
    print 'points: %f' % points
    
    # self.print_solution(self.solution)

    return


  #strategy
  #1. get higher score place with lowest spending time and lowest travel time
  #2. get 10 higher score place with lowest spending time and lowest travel time
  def solve(self, places, poi = None, sum_points = 0, pois_visited = None, time = None):
    for v in places:
      if pois_visited != None and v in pois_visited:
        continue

      #instance util variables
      current_poi  = poi
      points       = sum_points
      current_time = time

      #estimating travel time from current poi to v
      driving_time = 0
      if current_poi != None:
        driving_time = self.graph.getTimeTravel(current_poi.id, v.id)

      #estimating arrival time (current + driving)
      arrival_time = current_time + timedelta(minutes=int(driving_time))

      #total time in new place (arrival + spend time)
      total_time   = arrival_time + v.time_spend

      places = []
      if pois_visited != None:
        places.extend(pois_visited)

      #check if V point is practicable
      if (total_time <= self.period[1]) and (arrival_time >= v.start_hour) and (total_time <= v.end_hour):
        current_poi  = v
        points      += v.weight
        current_time = total_time
        places.append(v)

        #explore children
        children = self.get_most_valuable_places(v, places)
        self.solve(children, current_poi, points, places, current_time)

    if ((self.solution is None) or (sum_points > self.solution[1]) or (sum_points == self.solution[1] and len(pois_visited) > len(self.solution[2]))):
      self.solution = (pois_visited[-1], sum_points, pois_visited, time)

  def get_most_valuable_places(self, current, places, cut = None):
    tuples = []
    vertices = {}
    for v in self.graph.vertices:
      if v in places:
        continue

      vertices[v.id] = v

      driving_time = 0
      if current != None:
        driving_time = self.graph.getTimeTravel(current.id, v.id)
      
      time_spend   = v.time_spend + timedelta(minutes=int(driving_time))

      tuples.append((v.id, v.weight, time_spend))

    tuples.sort(key=lambda x:(x[2], -x[1]))

    end = 1
    if cut != None:
      end = int(math.ceil(len(tuples)*cut))
      

    result = []
    for t in tuples[0:end]:
      result.append(vertices[t[0]])

    return result

  def print_solution(self, solution):
    if solution is None:
      print 'Solution is None'
      return

    last_point = solution[0]
    points     = solution[1]
    places     = solution[2]
    last_time  = solution[3]

    current = None
    print_time = self.period[0]
    print 'Places (%d)' % (len(places))
    for p in places:
      driving_time = timedelta(minutes=int(0))
      if current != None:
        driving_time = self.graph.getTimeTravel(current.id, p.id)
        driving_time = timedelta(minutes=int(driving_time))
        #print '[ %s ] Driving Time' % driving_time
      
      print_time += driving_time
      print '[ (%s) | %s ] %.3f %s | %s %s %s | %s' % (driving_time, print_time, p.weight, p.id.encode('utf8'), p.start_hour, p.end_hour, p.time_spend, p.name.encode('utf8'))
      print_time += p.time_spend
      current = p

    #printing
    print 'Last POI: %s' % last_point.name.encode('utf8')
    print 'Total Points: %s' % points
    print 'Ending Time: %s' % last_time
    

    return