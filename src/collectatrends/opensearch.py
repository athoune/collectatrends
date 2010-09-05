"""
Opensearch response object with collecta and other extensions
"""

import httplib
from xml.etree.ElementTree import ElementTree

class Entry(object):
	def __init__(self, raw):
		self.raw = raw
		self.id = raw.find('{http://www.w3.org/2005/Atom}id').text
		self.title = raw.find('{http://www.w3.org/2005/Atom}title').text
		self.link = raw.find('{http://www.w3.org/2005/Atom}link').text
		self.language = raw.find('{http://api.collecta.com/ns/search-0#results}language').text
		self.category = raw.find('{http://api.collecta.com/ns/search-0#results}category').text
		self.site = raw.find('{http://api.collecta.com/ns/search-0#results}site').text
		self.abstract = raw.find('{http://api.collecta.com/ns/search-0#results}abstract').text
		self.tags = []
		for tag in raw.getiterator('{http://www.w3.org/2005/Atom}tags'):
			self.tags.append(tag.attrib['term'])

class Feed(object):
	def __init__(self, opensearch, raw):
		#print raw.read()
		self.opensearch = opensearch
		self.tree = ElementTree()
		self.tree.parse(raw)
		self.links = {}
		for link in self.tree.getiterator('{http://www.w3.org/2005/Atom}link'):
			self.links[link.attrib['rel']] = link.attrib['href']
	def keys(self):
		for entry in self.tree.getiterator('*'):
			yield entry.tag
	def __len__(self):
		return int(self.tree.find('{http://a9.com/-/spec/opensearch/1.1/}totalResults').text)
	def __iter__(self):
		#[TODO] iter over pages
		for entry in self.tree.getiterator('{http://www.w3.org/2005/Atom}entry'):
			yield self.opensearch.entry(entry)


class OpenSearch(object):
	def __init__(self, domain, feed=Feed, entry = Entry):
		self.feed = feed
		self.entry = entry
		self.conn = httplib.HTTPConnection(domain)
	def query(self, path):
		self.conn.request("GET", path)
		res = self.conn.getresponse()
		if res.status != 200:
			raise Exception('http')
		return self.feed(self, res)

