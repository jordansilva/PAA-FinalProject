#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: Jordan Silva <@jordansilva>
# Created: December 09th 2015

import json
import os
import time
import sys
from datetime import timedelta, time

class Baseline:

  def __init__(self, graph):
    self.graph        = graph
    self.graph.vertices = self.graph.vertices
    self.period       = None
    
    self.lower_timespend = sys.maxint
    for v in self.graph.vertices:
      minutes = (v.time_spend.total_seconds() / 60)
      if minutes < self.lower_timespend:
        self.lower_timespend = minutes
    self.lower_timespend = timedelta(minutes=int(self.lower_timespend))

  def execute(self, period):
    # for v in self.graph.vertices:
    #   print '%.3f %s | %s %s %s | %s' % (v.weight, v.id, v.start_hour, v.end_hour, v.time_spend, v.name)

    self.period = period
    self.solution = None
    self.all_nodes_alocated = False

    self.tree()

    print '\n### Baseline ###'
    print '[ Start Hour ] %s' % self.period[0]
    print '[ Final Hour ] %s\n' % self.period[1]

    self.print_solution(self.solution)
    return

  def tree(self, current = None, points = 0, visited = None, time = None):

    if time is None:
      current_time = self.period[0]
    else:
      current_time = time

    if (visited != None and len(visited) == len(self.graph.vertices)):
      self.solution = (visited[-1], points, visited, time)
      self.all_nodes_alocated = True
      return

    #check current_time >= final
    if current_time + self.lower_timespend <= self.period[1] and self.all_nodes_alocated == False:
      for v in self.graph.vertices:
        places = []

        if self.all_nodes_alocated:
          break

        if visited != None:
          places.extend(visited)

        if v in places:
          continue

        current_point = current
        max_price     = points
        if time is None:
          current_time = self.period[0]
        else:
          current_time = time

        time_to_place = 0
        driving_time  = 0

        if current_point != None:
          driving_time  = self.graph.getTimeTravel(current_point.id, v.id)

        time_to_place = current_time + timedelta(minutes=int(driving_time))
        time_to_leave = time_to_place + v.time_spend

        #check place is open and time to leave is before its closes.
        if time_to_leave <= self.period[1] and time_to_place >= v.start_hour and time_to_leave <= v.end_hour:
          places.append(v)
          current_point  = v
          max_price     += v.weight
          current_time   = time_to_leave

          self.tree(current_point, max_price, places, current_time)

    if (self.solution is None) or (points > self.solution[1]) or (points == self.solution[1] and len(visited) > len(self.solution[2])):
      self.solution = (visited[-1], points, visited, time)

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