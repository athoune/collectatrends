__author__ = "mathieu@garambrogne.net"

import urllib

from opensearch import OpenSearch

class Collecta(object):
	"""
	http://developer.collecta.com/Transports/HttpApi/
	"""
	def __init__(self, key=None, remember=False, cache_folder='~/.collecta'):
		self.key = key
		self.remember = remember
		self.cache_folder = cache_folder
	def query(self, **args):
		if self.key != None:
			args['api_key'] = self.key
		#args['rpp'] = 50
		self.opensearch = OpenSearch("api.collecta.com", cache_folder=self.cache_folder)
		return self.opensearch.query("/search?%s" % urllib.urlencode(args), self.remember)

if __name__ == '__main__':
	c = Collecta(remember=True)
	results = c.query(q='python language:fr', rpp=10)
	print len(results)
	print results.after_id
	#print list(results.keys())
	for result in results:
		print result['id']
		#print "\t", result['title'], result['tags']
