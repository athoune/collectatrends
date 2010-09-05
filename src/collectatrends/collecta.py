import httplib
import json
from xml.etree.ElementTree import ElementTree

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
		return Response(res)

class Response(object):
	def __init__(self, raw):
		#print raw.read()
		self.tree = ElementTree()
		self.tree.parse(raw)
		# self.raw = raw
		# self.query = raw['query']
		# self.page = raw['page']
		# self.max_id = raw['max_id']
		# self.since_id = raw['since_id']
		# self.results = raw['results']
		"""
		next_page
		refresh_url
		results
		"""
	def __len__(self):
		return int(self.tree.find('{http://a9.com/-/spec/opensearch/1.1/}totalResults').text)
	def __iter__(self):
		for entry in self.tree.getiterator():#'{http://www.w3.org/2005/Atom}entry'):
			yield entry

class Result(object):
	def __init__(self, raw):
		self.raw = raw
		for attr in raw:
			n = Node(attr)
			print n
		
	def __repr__(self):
#		return "<Result %s>"
		return ''#str(self.raw)

if __name__ == '__main__':
	c = Collecta()
	results = c.query('python')
	print len(results)
	#for result in results:
		#pass
	#	print ' '
	#	print result.tag
