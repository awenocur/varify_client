#Read Me
This document should describe any tools included with the Varify client.

##fetchVcf
command line to launch fetchVcf:

`fetchVcf.py -s sample1 sample2 -r 1:1-100000,2:1-100000`

This can be used to combine multiple samples into a single VCF file, even if the source data are from different runs.

##Setup
*   Go to `http://yourvarifyinstance.chop.edu/admin/serrano/apitoken/`
*   Add API Token and your varify instance to the configuration file and name it varify.cfg (see the sample config included)
