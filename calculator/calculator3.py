#!/usr/bin/env python3

import sys
import csv

parameter = ('-c', '-d', '-o')

class Args(object):
	def __init__(self):
		self.args = sys.argv[1:]

	def part(self):
		reslut = {}
		#parameter = ('-c', '-d', '-o')		
		try:
			for x in parameter:	
				index = self.args.index(x)
				filepath = self.args[index + 1]
				reslut[x] = filepath
			return reslut
		except:
			print("Parameter Error")

class Config(object):
	def __init__(self, dic):
		self.dic = dic
		self.config = self._read_config()

	def _read_config(self):
		config = {}
		try:
			for x in parameter:
				if x == '-o':
					continue
				elif x == '-c':
					c = {}
					with open(self.dic[x]) as f:
						for i in f:
							a = i.split("=")
							print(a[0].strip())
							print(a[1].strip())
			return self.dic
		except:
			print("222")

if __name__ == '__main__':
	a = Args()
	print(a.part())
	b = Config(a.part()).config
	print(b)