from os.path import dirname, join
from unittest import TestCase
from hashlib import md5
import varify_client._fetchVCF as fetchVCF

enclosing_dir = dirname(__file__)
demo_vcf_response_path = join(enclosing_dir, "data/demoResponse")

class testFetchVcf(TestCase):

    def test_fetch(self):
        response = fetchVCF.fetchVcfPipe([], protocol='file', host='', port=None,
                                         custom_path=demo_vcf_response_path)
        hash = md5(response.read())
        self.assertEqual(hash.hexdigest(),"9d5e6d6f78ab23bac7335d4f5492745b")

    # TODO: populate the following tests for the fetchVCF module
    def test_url(self):
        pass

    def test_request(self):
        pass

    def test_config(self):
        pass