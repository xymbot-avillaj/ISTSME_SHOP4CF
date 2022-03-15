

import string
import random
import requests
from datetime import datetime
import json
from agents._packages.HTTP.BasicHttpAgent import *
from agents.Agent import Agent

from http.client import HTTPSConnection, HTTPConnection

import time




class OrionAgent(Agent):
	def __init__(self):
		super().__init__("OrionAgent")

		self.arg_config = self.parse_arguments()
		self.logger = self.get_logger()

		# connect to the sink over the socket
		self.sink_client = self.connect_sink_socket()
		
		self.http_client = BasicHttpAgent(self.config, self.http_receive_callback)
		#self.initializtion()

	def initializtion(self):
		machines = open('config.json')
		machine=json.load(machines)
		machine=json.dumps(machine)
		machine=json.loads(machine)
		headers={'Content-Type': 'application/json'}
		tx='/v2/entities'
		# self.post('/v2/entities', machine)
		rl = 'http://192.168.2.186:1026/orion'+tx
		#print (headers)
		try:
			x = requests.post(rl, headers=headers, json=machine)
			if x.text:
				pass
				# print('POST RES: {}'.format(x.text))
		except Exception as error:
			print('POST ERROR: {}'.format(error))
			exit()
		time.sleep(1)
		# SUBSCRIPTION_STR = '''{
		# 	"description": "Notify when machine ",
		# 	"subject": {
		# 		"entities": [
		# 			{
		# 			"idPattern": "Machine"
		# 		}
		# 		]
		# 	},
		# 	"notification": {
		# 		"http": {
		# 			"url": "http://quantumleap:8668/v2/notify"
		# 		}
		# 	}
		# }'''
		# tx='/v2/subscriptions/'
		# rl = 'http://192.168.2.186:1026/orion'+tx
		# print (rl)
		# #print (headers)
		# try:
		# 	x = requests.post(rl, headers=headers, json=json.loads(SUBSCRIPTION_STR))
		# 	if x.text:
		# 		print('POST RES: {}'.format(x.text))
		# except Exception as error:
		# 	print('POST ERROR: {}'.format(error))
		# 	exit()

		time.sleep(1)

	def http_receive_callback(self, msg):
		msg = json.loads(msg)
		self.logger.info(msg)

	def socket_receive_callback(self, msg):
		# received a message from FLINT (the MSSQL Agent)
		#msg = json.dumps(msg)
		#msg = json.load(msg)
		#device_ctrl = msg["device-ctrl"]["device-custom-ctrl"]
		print("Recieved tag: {0} from machine {1}".format(msg["device-ctrl"]["data"]["tag"],msg["device-ctrl"]["data"]["mach"]))
		self.initializtion()
	def do_PATCH(self, uri, msg):
		headers = { 'Content-type': "application/json" }
		self.http_client.set_headers(headers)
		res = self.http_client.send_message(uri, msg, "PATCH")
		return res[1]

	def do_GET(self, uri):
		headers = {}
		self.http_client.set_headers(headers)
		res = self.http_client.send_message(uri, "", "GET")

		if res[0] == 200:
			return res[1]
		else:
			return {}

	def do_POST(self, uri, msg):
		headers = { 'Content-type': "application/ld+json" }
		self.http_client.set_headers(headers)
		self.http_client.send_message(uri, msg, "POST")

	def make_json_ld_device(self, msg):
		return msg

	def post(pa, data, headers={'Content-Type': 'application/json'}):
		"""Hace una petición POST.
		Parámetros:
		path -- path a añadir a la url
		data -- cuerpo (body) de la petición
		headers -- objeto dict con la cabecera
		"""
		
if __name__ == "__main__":
	OrionAgent().run()