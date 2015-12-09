#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: Jordan Silva <@jordansilva>
# Created: December 09th 2015

import json
import os
import time
import sys
import math
import simplejson, urllib
from geopy.distance import vincenty
from datetime import timedelta, time
from operator import itemgetter

class Vertice:

  def __init__(self, item, time_spend):
    self.id          = item['id']
    self.name        = item['name']
    self.category    = item['category']
    self.lat         = item['lat']
    self.lng         = item['lng']
    self.weight      = item['weight']
    self.start_hour  = item['hours']['start']
    self.end_hour    = item['hours']['end']
    self.checkins    = item['checkins']
    self.rating      = 0
    if 'rating' in item:
      self.rating    = item['rating']
    self.time_spend  = time_spend


class TravelCity:

  def __init__(self, folder, output):
    self.read_folder = folder
    self.output_folder = output

  # Initializes venues collection
  def initVenues(self):
    self.venues = []
    self.venues_w = []

    fo = open(self.read_folder + '/venues_100.json', 'r')
    for line in fo:
      item = json.loads(line)
      self.venues.append(item)
      self.venues_w.append((item['id'], item['weight']))

    self.venues_w.sort(key=lambda tup: tup[1], reverse=True)
    return

  def initCategories(self):
    self.categories = {}
    
    fo = open(self.read_folder + '/categories.csv', 'r')
    for line in fo:
      c = line.split(';')
      if len(c) > 1:
        self.categories[c[0]] = int(c[1])
      else:
        print c
        raise Exception()

    return

  def initDistances(self):
    self.distances = {}

    fo = open(self.read_folder + '/edges.json')
    for line in fo:
      if line.startswith('from'):
        continue

      sline = line.split(';')
      if len(sline) < 4:
        print line
        raise Exception('Menos que quatro linhas')

      item = {}
      item['from'] = sline[0]
      item['to'] = sline[1]
      item['distance'] = sline[2]
      item['driving_time'] = sline[3]

      _id = '%s;%s' % (sline[0], sline[1])
      self.distances[_id] = item

    return

  def getTimeInCategory(self, category):
    category = category.encode('utf8')

    if category not in self.categories:
      raise Exception('Category not found')

    return self.categories[category]

  def getTimeTravel(self, place1, place2):
    _id1 = '%s;%s' % (place1['id'], place2['id'])
    _id2 = '%s;%s' % (place2['id'], place1['id'])
    
    if _id1 in self.distances:
      return self.distances[_id1]['driving_time']
    elif _id2 in self.distances:
      return self.distances[_id1]['driving_time']
    else:
      print place1['id']
      print place2['id']
      raise Exception('Driving Time not found!')

  def startVertices(self):
    self.vertices = []
    for v in self.venues:
      self.vertices.append(Vertice(v, self.getTimeInCategory(v['category'])))
    
    return

  def start(self):
    self.initVenues()
    self.initCategories()
    self.initDistances()

    self.startVertices()
    print len(self.vertices)


if __name__ == '__main__':
  read_folder = '../dataset/run/'
  output_folder = '../results/'

  travel = TravelCity(folder=read_folder, output=output_folder)
  travel.start()
