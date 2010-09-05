from xml.etree.ElementTree import ElementTree

class Feed(object):
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
	
class Entry(object):
	def __init__(self, raw):
		pass