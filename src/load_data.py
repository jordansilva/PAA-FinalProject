#!/usr/bin/python
# -*- coding: utf-8 -*-
# Trash
#	Just for Data Analysis
#
#
# Author: Jordan Silva <@jordansilva>
# Created: December 08th 2015

import json
import os
import time
import sys
import math
import simplejson, urllib
from geopy.distance import vincenty
from datetime import timedelta, time
from operator import itemgetter

class LoadData:

	def __init__(self, folder, output):
		self.read_folder = folder
		self.output_folder = output
		#diligencias AIzaSyA_9Rrjw1b2rpI3PW-Bfd1dejZMKwYlHRY
		#ufmg AIzaSyB1i5c7Iim3ykOmoJZ4y4TLTNbJxNI4tXY
		#ufmg2 AIzaSyDo3ypu8Vj0NHDkG8igvpEF9Q08riqgnWY
		self.key = 'AIzaSyDo3ypu8Vj0NHDkG8igvpEF9Q08riqgnWY'

	def cropVenues(self):
		self.venues = []

		touristic = ['Mercado Central', 'Praça da Liberdade', 'Lagoa da Pampulha', 'Praça da Bandeira', 'Palácio das Artes', 'Basílica Nossa Senhora de Lourdes', 'Rua do Amendoim', 'Parque das Mangabeiras', 'Fundação Zoo-Botânica de Belo Horizonte', 'Palácio da Liberdade', 'Parque Ecológico da Pampulha', 'Igreja Batista da Lagoinha', 'Igreja São José', 'Sesc Palladium', 'Parque Juscelino Kubitschek', 'Praça Diogo de Vasconcelos (Praça da Savassi)', 'Museu de Arte da Pampulha', 'Estádio Governador Magalhães Pinto (Mineirão)', 'Mirante do Mangabeiras', 'Expominas', 'Praça Sete de Setembro (Praça 7)', 'Bolão', 'Praça da Estação', 'Praça do Papa (Governador Israel Pinheiro)', 'Parque Municipal Américo Renné Giannetti', 'Edifício Arcangelo Maletta', 'Praça da Assembléia (Praça Carlos Chagas)', 'Feira de Artes e Artesanato de Belo Horizonte (Feira Hippie)', 'Cidade Administrativa Presidente Tancredo Neves']

		bigCheckins = []
		listVenues = {}
		fo = open(self.read_folder + '/venues.json', 'r')
		for line in fo:
			item = json.loads(line)

			if item['name'].encode('utf8') in touristic:
				self.venues.append(item)
			else:
				bigCheckins.append((item['id'], item['checkins']))
				listVenues[item['id']] = item

		bigCheckins.sort(key=lambda tup: tup[1], reverse=True)
		for item in bigCheckins:
			if len(self.venues) >= 100:
				break
			if item[0].encode('utf8') in listVenues and listVenues[item[0]] not in self.venues:
				self.venues.append(listVenues[item[0]])

		fw = open(self.output_folder + '/venues_crop.json', 'w')
		for item in self.venues:
			json.dump(item, fw, encoding='utf-8')
			fw.write('\n')
		fw.close()
		return

	def initVenues(self):
		self.venues = []

		fo = open(self.read_folder + '/venues_100.json', 'r')
		for line in fo:
			item = json.loads(line)
			self.venues.append(item)

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

	def processDistances(self):
		processed = []
		f = open(self.output_folder + '/edges_1.json', 'r')
		for line in f:
			if line.startswith('from'):
				continue
			
			lines = line.split(';')
			if len(lines) < 4:
				print line
				raise Exception('Menos que quatro linhas')

			processed.append(lines[0] + ';' + lines[1])


		fw = open(self.output_folder + '/edges.json', 'a', 10)
		fw.write('from;to;distance;driving_time\n')
		i = 0
		j = 0

		try:
			for i in xrange(0, len(self.venues)):
				place1 = self.venues[i]
				for j in xrange(0,len(self.venues)): #i+1
					place2 = self.venues[j]

					if (place1['id'] + ';' + place2['id']) in processed or place1['id'] == place2['id']:
						continue
						
					distance, driving_time = self.getTimeGoogleMaps(place1, place2)
					driving_time = math.ceil(driving_time / 60.0)

					result = '%s;%s;%d;%d' % (place1['id'], place2['id'], distance, driving_time)
					fw.write(result + '\n')
		except Exception, e:
			print e
			print "i: %d | j: %d" % (i, j)

		fw.close()

	def getTimeInCategory(self, category):
		category = category.encode('utf8')

		if category not in self.categories:
			raise Exception('Category not found')

		return self.categories[category]

	def getTimeTravel(self, place1, place2):
		p1 = (place1['lat'], place1['lng'])
		p2 = (place2['lat'], place2['lng'])
		return vincenty(p1, p2).meters


	def getTimeGoogleMaps(self, place1, place2):
		result = ''
		try:
			orig_coord = place1['lat'], place1['lng']
			dest_coord = place2['lat'], place2['lng']
			url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false&key={2}".format(str(orig_coord),str(dest_coord),self.key)
			
			result= simplejson.load(urllib.urlopen(url))

			distance = result['rows'][0]['elements'][0]['distance']['value']
			driving_time = result['rows'][0]['elements'][0]['duration']['value']
			return distance, driving_time
		except Exception, e:
			print e
			if 'REQUEST_DENIED' in result:
				return self.getTimeGoogleMaps(place1, place2)
			else:
				print result
				raise e

	def start(self):
		self.initVenues()
		#self.initCategories()

		#distances
		self.processDistances()


if __name__ == '__main__':
	read_folder = '../dataset/run/'
	output_folder = '../results/'

	loaddata = LoadData(folder=read_folder, output=output_folder)
	loaddata.start()
