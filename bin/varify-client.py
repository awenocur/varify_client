import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from _fetchVCF import VariantVcfDownload

firstArg = os.path.split(sys.argv[0])
firstArg = firstArg[firstArg.__len__() - 1]
if(firstArg == "fetchVCF" or firstArg == "fetchVCF.py"):
    VariantVcfDownload.runCommandLine()