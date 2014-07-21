import unittest
from test import fetchVCF

loader = unittest.TestLoader()
suite = loader.loadTestsFromTestCase(fetchVCF.testFetchVcf)
unittest.TextTestRunner().run(suite)