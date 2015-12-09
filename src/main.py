#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: Jordan Silva <@jordansilva>
# Created: December 09th 2015

import json
import os
import time
import sys
from graph import Graph

class Main:

  def __init__(self):
    read_folder = '../dataset/run/'
    output_folder = '../results/'
    self.graph = Graph(folder=read_folder, output=output_folder)
    self.graph.start()

  def execute(self):
    print '[ Graph loaded! ]'
    print '[ V %d' % len(self.graph.vertices)
    print '[ E %d' % len(self.graph.edges)
    print ''
    print self.graph.vertices[0].start_hour
    print self.graph.vertices[0].end_hour

if __name__ == '__main__':
  m = Main()
  m.execute()
