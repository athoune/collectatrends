__author__ = 'mathieu@garambrogne.net'

import anydbm
import json

import os
import os.path

def mkdir_p(path):
	folder = os.path.dirname(path)
	if not os.path.exists(folder):
		os.makedirs(folder)

class DbmStore(object):
	"""
	A simple persistance object.
	Persistance can be done in any object with __setitem__ and __len__
	More complex object can use mongodb or wathever
	"""
	def __init__(self, path):
		self.db = anydbm.open(path, 'c')
	def __setitem__(self, key, value):
		if type(value) not in [str, unicode]:
			value = json.dumps(value)
		self.db[key] = value
	def __len__(self):
		return len(self.db)

if __name__ == '__main__':
	d = DbmStore('test')
	d['beuha'] = 42
	print len(d)
