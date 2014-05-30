#!/usr/bin/python
from argparse import ArgumentParser
import urllib2
import vcf
from config import connectionConfig

class VariantVcfDownload:
    @staticmethod
    def fetchVcfPipe(sample_list, host=None, port=None, protocol=None, token=None):
        tokenQueryString = ''

        if host == None:
           host = connectionConfig.host
        if port == None:
           port = connectionConfig.port
        if protocol == None:
           protocol = connectionConfig.protocol
        if token == None:
           token = connectionConfig.token

        if token != None:
           tokenQueryString = '?token=' + token

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
