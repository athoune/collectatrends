"""
Opensearch response object with collecta and other extensions
"""

__author__ = "mathieu@garambrogne.net"

import httplib
from urlparse import urlparse, parse_qs
from xml.etree.ElementTree import ElementTree
import json
import hashlib
import os.path

def cache_name(query):
	sha1 = hashlib.sha1()
	sha1.update(query)
	return sha1.hexdigest() + '.json'

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
	def __init__(self, opensearch, raw, remember=False):
		#print raw.read()
		self.opensearch = opensearch
		self.tree = ElementTree()
		self.tree.parse(raw)
		self.links = {}
		for link in self.tree.getiterator('{http://www.w3.org/2005/Atom}link'):
			if link.attrib.has_key('rel'):
				self.links[link.attrib['rel']] = link.attrib['href']
		self.after_id = None
		self.next_url = None
		if self.links.has_key('next'):
			a = urlparse(self.links['next'])
			self.next_url = '%s?%s' % (a.path, a.query)
		if self.links.has_key('after'):
			a = urlparse(self.links['after'])
			p = parse_qs(a.query)
			self.after_id = p.get('after_id', None)[0]
			if remember:
				json.dump({'q': p['q'][0], 'after_id' : self.after_id}, open(cache_name(p['q'][0]), 'w+'))
	def keys(self):
		for entry in self.tree.getiterator('*'):
			yield entry.tag
	def __len__(self):
		return int(self.tree.find('{http://a9.com/-/spec/opensearch/1.1/}totalResults').text)
	def __iter__(self):
		for entry in self.tree.getiterator('{http://www.w3.org/2005/Atom}entry'):
			yield self.opensearch.entry(entry)
		if self.next_url != None:
			#[TODO] Don't use recursivity, iter over pages
			f = self.opensearch.query(self.next_url)
			for entry in f:
				yield entry


class OpenSearch(object):
	def __init__(self, domain, feed=Feed, entry = Entry):
		self.feed = feed
		self.entry = entry
		self.conn = httplib.HTTPConnection(domain)
	def query(self, path, remember=False):
		if remember:
			p = parse_qs(urlparse(path).query)
			cache = cache_name(p['q'][0])
			if os.path.exists(cache) and not p.has_key('since_id'):
				path += '&since_id=%s' % json.load(open(cache, 'r'))['after_id']
		self.conn.request("GET", path)
		res = self.conn.getresponse()
		if res.status != 200:
			raise Exception('http', "%s: %s" % (res.status, path))
		return self.feed(self, res, remember)

