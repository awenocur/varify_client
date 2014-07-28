#!/usr/bin/python
from argparse import ArgumentParser
import urllib2
import vcf
from config import connectionConfig, updateConfigPath, readConfig
import json
import re
from util import chromRange
from sys import stderr

# The following function generates a request for fetching a VCF file.
def vcfFetchRequest(data, host=None, port=None, protocol=None,
                    token=None, custom_path=None):
    tokenQueryString = ''
    if host == None:
        host = connectionConfig.host
    if port == None:
        port = connectionConfig.port
    if protocol == None:
        protocol = connectionConfig.protocol
    if token == None:
        token = connectionConfig.token

    if token:
        tokenQueryString = '?token=' + token

    port_string = ""
    if port:
        port_string = ":" + str(port)

    path_string = "/api/data/export/vcf/"
    if custom_path:
        path_string = custom_path

    request = urllib2.Request(protocol + "://" + host + port_string +
        path_string + tokenQueryString, data=data,
        headers={'Content-type': 'application/json'})
    return request

# The following function generates the JSON to send to Harvest to fetch a VCF
# file.
def vcfFetchData(sample_list, ranges=None):
    for_export = {}

    if ranges:
        rangesForExport = []
        for range in ranges:
            rangesForExport.append(range.dict())
        for_export['ranges'] = rangesForExport

    for_export['samples'] = sample_list

    data = json.dumps(for_export)

    return data

def fetchVcfPipe(sample_list, ranges=None, **vargs):

    data = vcfFetchData(sample_list, ranges)

    request = vcfFetchRequest(data, **vargs)

    return urllib2.urlopen(request)


def fetchVcf(*args, **kwargs):
    pipe = fetchVcfPipe(*args, **kwargs)
    reader = vcf.Reader(fsock=pipe)
    return reader


def runCommandLine():
    #The following is a Python 2.7+ implementation; use optparse for Python 2.6
    argParser = ArgumentParser("fetch VCF representation of variant data")
    argParser.add_argument('--sample', '-s', dest='sampleNames', nargs='+', type=str)
    argParser.add_argument('--range', '-r', dest='ranges', nargs='+', type=str)
    argParser.add_argument('--config', '-c', dest='configPath')
    args = argParser.parse_args()

    if args.sampleNames == None:
        print "no sample labels provided!"
        return

    ranges = []
    rangeStrings = args.ranges
    rangePattern = re.compile(r"(?P<chr>.*?):(?P<begin>.*?)-(?P<end>.*?)$")
    if rangeStrings != None:
        for string in rangeStrings:
            rangeProps = rangePattern.match(string)
            try:
                newRange = chromRange(
                    rangeProps.group("chr"),
                    int(rangeProps.group("begin")),
                    int(rangeProps.group("end"))
                )
                ranges.append(newRange)
            except AttributeError, e:
                print >> stderr, "ignoring range \"" + string + "\": improperly formatted"


    if args.configPath != None:
        updateConfigPath(args.configPath)
    readConfig()

    try:
        vcfStream = fetchVcfPipe(args.sampleNames, ranges=ranges)
        print vcfStream.read()[:-1]
    except urllib2.HTTPError, e:
        print >> stderr, "HTTP error: %d" % e.code
    except urllib2.URLError, e:
        print >> stderr, "Network error: %s" % e.reason.args[1]
