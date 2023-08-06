# python -m unittest tests.test_downloader

import unittest
import responses
from occson.downloader import Downloader

class TestDownloader(unittest.TestCase):

  @responses.activate
  def test_call(self):
    responses.add(responses.GET, 'https://api.occson.com/test.json', json = { 'encrypted_content': 'U2FsdGVkX1+h5SI8P5C04RYYhEBR2HzAVvG6poI6FQYcsr8ZaS7PrBjVxchsyjNU' }, status = 200)

    result = Downloader('https://api.occson.com/test.json', '<ACCESS_TOKEN>', '<PASSPHRASE>').call()

    self.assertEqual('<ENCRYPTED_CONTENT>', result)
