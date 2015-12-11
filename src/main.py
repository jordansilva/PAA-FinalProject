#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: Jordan Silva <@jordansilva
# Created: December 09th 2015

import json
import os
import time
import sys
import networkx as nx
import matplotlib.pyplot as plt
from datetime import timedelta
from graph import Graph
from algorithm.baseline import Baseline
from algorithm.random_tour import RandomTour
from algorithm.random_tour_d import RandomTourD

class Main:

  def __init__(self):
    read_folder = '../dataset/run/'
    output_folder = '../results/'
    self.graph = Graph(folder=read_folder, output=output_folder)
    self.graph.start()

  def execute(self, period):
    #Baseline

    limits = [10, 20, 30]#, 40, 50, 60, 70, 80, 90, 100]
    for i in limits:
      read_folder = '../dataset/run/'
      output_folder = '../results/'
      self.graph = Graph(folder=read_folder, output=output_folder)
      self.graph.start()
      self.graph.vertices = self.graph.vertices[0:i]

      print '[ Graph loaded! ]'
      print '[ V %d  E %d ]' % (len(self.graph.vertices), len(self.graph.edges))

      ## Random Tour
      # start_time = time.time()
      # random_tour = RandomTour(self.graph)
      # random_tour.execute(period)
      # elapsed_time = time.time() - start_time
      # print elapsed_time

      ## Random Tour D
      # start_time = time.time()
      # random_tour = RandomTourD(self.graph)
      # random_tour.execute(period)
      # elapsed_time = time.time() - start_time
      # print elapsed_time
      

      ## Baseline
      start_time = time.time()
      baseline = Baseline(self.graph)
      baseline.execute(period)
      elapsed_time = time.time() - start_time
      print elapsed_time
      print '\n\n'

  def createGraph(self):
    G = nx.DiGraph()
    self.graph.vertices = self.graph.vertices[0:10]

    for v in self.graph.vertices:
      G.add_node(v.id, name=v.name, category=v.category, lat=v.lat, lng=v.lng, weight=v.weight, start_hour=v.start_hour, end_hour=v.end_hour, checkins=v.checkins, rating=v.rating, time_spend=v.time_spend)

    for e in self.graph.edges:
      ed = self.graph.edges[e]
      if ed.point1 in G.nodes() and ed.point2 in G.nodes():
        G.add_edge(ed.point1, ed.point2, distance=int(ed.distance), driving_time=int(ed.driving_time))

    self.save_graph(G, 'graph.png')

  def save_graph(self, graph,file_name):

    # pos = nx.spring_layout(G)

    # edge_labels=dict([((u,v,),d['driving_time']) for u,v,d in G.edges(data=True)])
    # nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
    
    # node_labels = {node:G.node[node]['name'] for node in G.nodes()}; 
    # nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=6)

    # nx.draw(G, pos, node_size=200, edge_size=100)
    # plt.savefig("graph.png")
    # plt.close()

    #initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph,pos)
    nx.draw_networkx_edges(graph,pos)
    nx.draw_networkx_labels(graph,pos)

    cut = 0.05
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig(file_name, bbox_inches="tight")
    plt.close()
    del fig


if __name__ == '__main__':
  period_start = timedelta(hours=8, minutes=00)
  period_end   = timedelta(hours=22, minutes=30)
  period       = (period_start, period_end)

  m = Main()
  m.createGraph()
  #m.execute(period)
