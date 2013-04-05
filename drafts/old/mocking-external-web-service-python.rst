:Date: 2009-11-25 11:20:59

Mocking an External Web Service in Python
=========================================

In [1]: import mock

In [2]: import urllib2

In [4]: mock = mock.Mock()

In [7]: mock.method.return\_value = "{'my\_sweet': 'json'}"

In [8]: mock.method() Out[8]: "{'my\_sweet': 'json'}"

In [9]: urllib2.urlopen = mock.method

In [10]: urllib2.urlopen('http://google.com/OMG\_API') Out[10]:
"{'my\_sweet': 'json'}"


