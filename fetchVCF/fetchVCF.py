#!/usr/bin/python
from argparse import ArgumentParser
import ConfigParser
import urllib2

#The following is a Python 2.7+ implementation; use optparse for Python 2.6
argParser = ArgumentParser("fetch VCF representation of variant data")
argParser.add_argument('--sample', '-s', dest='sampleNames', nargs='+', type=str)
args = argParser.parse_args()

port = 80
host = '127.0.0.1'
protocol = 'http'
tokenQueryString = ''

config = ConfigParser.ConfigParser()
config.readfp(open('varify.cfg'))
if config.has_section('Connection'):
    if(config.has_option('Connection', 'host')):
        host = config.get('Connection', 'host')
    if(config.has_option('Connection', 'port')):
        port = config.getint('Connection', 'port')
    if(config.has_option('Connection', 'protocol')):
        protocol = config.get('Connection', 'protocol')
    if(config.has_option('Connection', 'token')):
        tokenQueryString = '?token=' + config.get('Connection', 'token')


sample_list = args.sampleNames

data = ''

for sample in sample_list:
    data = data + '\n' + sample

request = urllib2.Request(protocol + "://" + host + ":" + str(port) + "/api/data/export/vcf/" + tokenQueryString, data=data, headers={'Content-type': 'text/plain'})
try:
     print urllib2.urlopen(request).read()
except urllib2.HTTPError, e:
     print "HTTP error: %d" % e.code
except urllib2.URLError, e:
     print "Network error: %s" % e.reason.args[1]
