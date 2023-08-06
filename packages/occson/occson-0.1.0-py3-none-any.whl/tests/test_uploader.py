# python -m unittest tests.test_uploader

import unittest
import responses
from occson.uploader import Uploader

class TestUploader(unittest.TestCase):

  @responses.activate
  def test_call(self):
    responses.add(responses.POST, 'https://api.occson.com/test.json', json = {}, status = 201)

    result = Uploader('https://api.occson.com/test.json', '<ENCRYPTED_CONTENT>', '<ACCESS_TOKEN>', '<PASSPHRASE>', False).call()

    self.assertEqual(True, result)
