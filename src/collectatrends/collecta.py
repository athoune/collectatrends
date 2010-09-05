import urllib
from opensearch import OpenSearch

class Collecta(object):
	"""
	http://developer.collecta.com/Transports/HttpApi/
	"""
	def __init__(self, key=None):
		self.key = key
	def query(self, **args):
		if self.key != None:
			args['api_key'] = self.key
		self.opensearch = OpenSearch("api.collecta.com")
		return self.opensearch.query("/search?%s" % urllib.urlencode(args))

if __name__ == '__main__':
	c = Collecta()
	results = c.query(q='python language:fr', rpp=10)
	print len(results)
	print results.links['after']
	#print list(results.keys())
	for result in results:
		print result.id
		print "\t", result.title, result.tags
