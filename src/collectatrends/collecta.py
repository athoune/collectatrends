import httplib
import urllib
from opensearch import Feed

class Collecta(object):
	"""
	http://developer.collecta.com/Transports/HttpApi/
	"""
	def __init__(self, key=None):
		self.conn = httplib.HTTPConnection("api.collecta.com")
	def query(self, **args):
		self.conn.request("GET", "/search?%s" % urllib.urlencode(args))
		res = self.conn.getresponse()
		if res.status != 200:
			raise Exception('http')
		return Feed(res)


if __name__ == '__main__':
	c = Collecta()
	results = c.query(q='python', rpp=10)
	print len(results)
	#print list(results.keys())
	for result in results:
		print result.id
		print "\t", result.title, result.tags
