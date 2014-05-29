#!/usr/bin/python
from argparse import ArgumentParser
import ConfigParser
import urllib2
import vcf
import os

class VariantVcfDownload:
    @staticmethod
    def fetchVcfPipe(sample_list, host=None, port=None, protocol=None, token=None):
        tokenQueryString = ''

        configPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../varify.cfg')

        config = ConfigParser.ConfigParser()
        config.readfp(open(configPath))
        if config.has_section('Connection'):
            if host == None and config.has_option('Connection', 'host'):
               host = config.get('Connection', 'host')
            if port == None and config.has_option('Connection', 'port'):
               port = config.getint('Connection', 'port')
            if protocol == None and config.has_option('Connection', 'protocol'):
               protocol = config.get('Connection', 'protocol')
            if token == None and config.has_option('Connection', 'token'):
               token = config.get('Connection', 'token')

            if token != None:
               tokenQueryString = '?token=' + token

        if (port == None): port = 80
        if (host == None): host = '127.0.0.1'
        if (protocol == None): protocol = 'http'

        data = ''

        for sample in sample_list:
            data = data + sample + '\n'

        request = urllib2.Request(protocol + "://" + host + ":" + str(port) + "/api/data/export/vcf/" + tokenQueryString, data=data, headers={'Content-type': 'text/plain'})
        return urllib2.urlopen(request)

    @staticmethod
    def fetchVcf(*args, **kwargs):
        pipe = VariantVcfDownload.fetchVcfPipe(*args, **kwargs)
        reader = vcf.Reader(fsock=pipe)
        return reader

#The following is a Python 2.7+ implementation; use optparse for Python 2.6
argParser = ArgumentParser("fetch VCF representation of variant data")
argParser.add_argument('--sample', '-s', dest='sampleNames', nargs='+', type=str)
args = argParser.parse_args()

try:
     vcfStream = VariantVcfDownload.fetchVcfPipe(args.sampleNames)
     print vcfStream.read()
except urllib2.HTTPError, e:
     print "HTTP error: %d" % e.code
except urllib2.URLError, e:
     print "Network error: %s" % e.reason.args[1]
