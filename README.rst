Collecta Trends
===============

Building rrd graph from collecta query to watch evolution.

Tools
-----

The elementree library is used, and classical python tools.

Using it
--------

The api is a wrapper of the `collecta http api`_ ::

	c = Collecta()
	results = c.query(q='python language:fr', rpp=10)

It's a plain object, with attributes::

	print len(results)
	print results.updated

You can iterate over results::

	for result in results:
		print result.id
		print "\t", result.title, result.tags


.. _`collecta http api`: http://developer.collecta.com/Transports/HttpApi/
