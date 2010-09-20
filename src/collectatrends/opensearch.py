"""
Opensearch response object with collecta and other extensions
"""

__author__ = "mathieu@garambrogne.net"

import httplib
from urlparse import urlparse, parse_qs
from urllib import urlencode
from xml.etree.ElementTree import ElementTree
import json
import hashlib
import os.path
import math
import time

def cache_name(query):
	sha1 = hashlib.sha1()
	sha1.update(query)
	return sha1.hexdigest() + '.json'

def mkdir_p(path):
	folder = os.path.dirname(path)
	if not os.path.exists(folder):
		os.makedirs(folder)

def Entry(raw):
	e = {}
	e['id'] = raw.find('{http://www.w3.org/2005/Atom}id').text
	e['title'] = raw.find('{http://www.w3.org/2005/Atom}title').text
	e['link'] = raw.find('{http://www.w3.org/2005/Atom}link').text
	e['language'] = raw.find('{http://api.collecta.com/ns/search-0#results}language').text
	e['category'] = raw.find('{http://api.collecta.com/ns/search-0#results}category').text
	e['site'] = raw.find('{http://api.collecta.com/ns/search-0#results}site').text
	e['abstract'] = raw.find('{http://api.collecta.com/ns/search-0#results}abstract').text
	e['tags'] = []
	for tag in raw.getiterator('{http://www.w3.org/2005/Atom}tags'):
		e['tags'].append(tag.attrib['term'])
	return e

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
				cache = "%s/%s" % (self.opensearch.cache_folder, cache_name(p['q'][0]))
				mkdir_p(cache)
				json.dump({'q': p['q'][0], 'after_id' : self.after_id, 'total' : len(self)}, open(cache, 'w+'))
	def keys(self):
		for entry in self.tree.getiterator('*'):
			yield entry.tag
	def __len__(self):
		return int(self.tree.find('{http://a9.com/-/spec/opensearch/1.1/}totalResults').text)
	def __iter__(self):
		for entry in self.tree.getiterator('{http://www.w3.org/2005/Atom}entry'):
			yield self.opensearch.entry(entry)
		if self.next_url != None:
			items_per_page = int(self.tree.find('{http://a9.com/-/spec/opensearch/1.1/}itemsPerPage').text)
			t = ElementTree()
			a = urlparse(self.next_url)
			p = parse_qs(a.query)
			p['q'] = p['q'][0]
			#print "pages:", len(self), 2, int(math.ceil(len(self) / items_per_page))+1
			for page in range(2, int(math.ceil(len(self) / items_per_page)) +1):
				if page % 5 == 0:
					time.sleep(10)
					print "pause"
				p['page'] = page
				url = '%s?%s' % (a.path, urlencode(p))
				t.parse(self.opensearch.raw_query(url))
				for entry in t.getiterator('{http://www.w3.org/2005/Atom}entry'):
					yield self.opensearch.entry(entry)

class TooManyQuestion(Exception):
	pass
class OpenSearch(object):
	def __init__(self, domain, feed=Feed, entry = Entry, cache_folder='~/.openserach'):
		self.feed = feed
		self.entry = entry
		self.cache_folder = os.path.expanduser(cache_folder)
		self.conn = httplib.HTTPConnection(domain)
	def raw_query(self, path):
		self.conn.request("GET", path)
		res = self.conn.getresponse()
		if res.status == 401:
			raise TooManyQuestion()
		if res.status != 200:
			raise Exception('http', "%s: %s" % (res.status, path))
		return res
	def query(self, path, remember=False):
		if remember:
			p = parse_qs(urlparse(path).query)
			cache = cache_name(p['q'][0])
			if os.path.exists(cache) and not p.has_key('since_id'):
				path += '&since_id=%s' % json.load(open(cache, 'r'))['after_id']
		return self.feed(self, self.raw_query(path), remember)

