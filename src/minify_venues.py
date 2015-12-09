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
from datetime import timedelta, time
from operator import itemgetter

reload(sys)
sys.setdefaultencoding("utf-8")

original_folder = '../dataset/original/'
original_filename = "venues_content.json"
output_folder = '../dataset/output/'

def reduce_venues():
	f = open(original_folder + original_filename, 'r')
	fw = open(output_folder + 'venues.json', 'a', 10)

	for line in f:
		item = json.loads(line)
		if item['venue']['stats']['checkinsCount'] > 50:
			fw.write(line)

	f.close()
	fw.close()


touristic = ['Mercado Central', 'Praça da Liberdade', 'Lagoa da Pampulha', 'Praça da Bandeira', 'Palácio das Artes', 'Basílica Nossa Senhora de Lourdes', 'Rua do Amendoim', 'Parque das Mangabeiras', 'Fundação Zoo-Botânica de Belo Horizonte', 'Palácio da Liberdade', 'Parque Ecológico da Pampulha', 'Igreja Batista da Lagoinha', 'Igreja São José', 'Sesc Palladium', 'Parque Juscelino Kubitschek', 'Praça Diogo de Vasconcelos (Praça da Savassi)', 'Museu de Arte da Pampulha', 'Estádio Governador Magalhães Pinto (Mineirão)', 'Mirante do Mangabeiras', 'Expominas', 'Praça Sete de Setembro (Praça 7)', 'Bolão', 'Praça da Estação', 'Praça do Papa (Governador Israel Pinheiro)', 'Parque Municipal Américo Renné Giannetti', 'Edifício Arcangelo Maletta', 'Praça da Assembléia (Praça Carlos Chagas)', 'Feira de Artes e Artesanato de Belo Horizonte (Feira Hippie)', 'Cidade Administrativa Presidente Tancredo Neves']

def get_hour(venue):
	hour_start = timedelta(hours=0, minutes=0)
	hour_end = timedelta(hours=23, minutes=59)

	if 'hours' in venue:
		timeframes = venue['hours']['timeframes'][0]
		o = timeframes['open'][0]
		hours = o['renderedTime'].split('–')
		if len(hours) > 1:
			#START
			hour_start = hours[0].replace('AM', '').replace('PM', '').strip().split(':')
			if len(hour_start) > 1:
				hour_start = timedelta(hours=int(hour_start[0]), minutes=int(hour_start[1]))
			else:
				if 'Midnight' in hour_start[0]:
					hour_start = timedelta(hours=24, minutes=00)
				elif 'Noon' in hour_start[0]:
					hour_start = timedelta(hours=12, minutes=00)
				else:
					print 'Error'
					hour_start = timedelta(hours=int(hour_start[0]), minutes=int(hour_start[1]))

			#END
			hour_end = hours[1].replace('AM', '').replace('PM', '').strip().split(':')
			if len(hour_end) > 1:
				hour_end = timedelta(hours=int(hour_end[0]), minutes=int(hour_end[1]))
			else:
				if 'Midnight' in hour_end[0]:
					hour_end = timedelta(hours=24, minutes=00)
				elif 'Noon' in hour_end[0]:
					hour_end = timedelta(hours=12, minutes=00)
				else:
					print 'Error'
					hour_end = timedelta(hours=int(hour_end[0]), minutes=int(hour_end[1]))
			
			if 'PM' in hours[0]:
				hour_start = hour_start + timedelta(hours=12)
			if 'PM' in hours[1]:
				hour_end = hour_end + timedelta(hours=12)

	return { 'start': str(hour_start), 'end': str(hour_end) }

def minify_venues_weight():
	f = open(output_folder + 'venues.json', 'r')
	fw = open(output_folder + 'venues_weight_min.json', 'a', 10)

	for line in f:
		item = json.loads(line)
		venue = item['venue']
		name = venue['name']
		checkins = venue['stats']['checkinsCount']
		
		new_item = {}
		new_item['id'] = venue['id']
		new_item['name'] = name
		new_item['checkins'] = checkins
		try:
			new_item['category'] = venue['categories'][0]['name']
		except Exception, e:
			new_item['category'] = ''

		# new_item['categories'] = venue['categories']
		new_item['location'] = venue['location']
		new_item['lat'] = venue['location']['lat']
		new_item['lng'] = venue['location']['lng']
		try:
			new_item['hours'] = get_hour(venue)
		except Exception, e:
			print e
			print venue['id']
			raise e

		if 'rating' in venue:
			new_item['rating'] = venue['rating']
		
		#weight
		new_item['weight'] = math.log(checkins, 10)
		if name in touristic:
			new_item['weight'] = new_item['weight'] * 1.5
		new_item['weight'] = round(new_item['weight'], 3)
		
		#max value weight = 10
		if new_item['weight'] > 10:
			new_item['weight'] = 10.0

		json.dump(new_item, fw, encoding='utf-8')
		fw.write('\n')

	f.close()
	fw.close()

def summarize_categories():
	categories = {}
	f = open(output_folder + 'venues_weight_min.json', 'r')
	for line in f:
		item = json.loads(line)
		cat = item['category']
		if cat not in categories:
			categories[cat] = 0
		
		categories[cat] += 1

	f.close()

	fw = open(output_folder + 'summarize_cat.csv', 'a', 10)
	for c in categories:
		fw.write(c + ';' + str(categories[c]) + '\n')
	fw.close()


#start
summarize_categories()
#minify_venues_weight()