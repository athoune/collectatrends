import httplib
from opensearch import Feed

class Collecta(object):
	"""
	http://developer.collecta.com/Transports/HttpApi/
	"""
	def __init__(self, key=None):
		self.conn = httplib.HTTPConnection("api.collecta.com")
	def query(self, q):
		self.conn.request("GET", "/search?rpp=25&q=%s" % q)
		res = self.conn.getresponse()
		if res.status != 200:
			raise Exception('http')
		return Feed(res)


if __name__ == '__main__':
	c = Collecta()
	results = c.query('python')
	print len(results)
	print list(results.keys())
	for result in results:
		print result.id
		print "\t", result.title
