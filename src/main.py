#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: Jordan Silva <@jordansilva>
# Created: December 09th 2015

import json
import os
import time
import sys
from datetime import timedelta
from graph import Graph
from algorithm.baseline import Baseline

class Main:

  def __init__(self):
    read_folder = '../dataset/run/'
    output_folder = '../results/'
    self.graph = Graph(folder=read_folder, output=output_folder)
    self.graph.start()

  def execute(self, period):
    #Baseline
    start_time = time.time()

    self.graph.vertices = self.graph.vertices[0:30]


    print '[ Graph loaded! ]'
    print '[ V %d  E %d ]' % (len(self.graph.vertices), len(self.graph.edges))

    baseline = Baseline(self.graph)
    baseline.execute(period)

    elapsed_time = time.time() - start_time
    print elapsed_time

if __name__ == '__main__':
  period_start = timedelta(hours=8, minutes=00)
  period_end   = timedelta(hours=12, minutes=30)
  period       = (period_start, period_end)

  m = Main()
  m.execute(period)
