import requests
from AesEverywhere import aes256

class Downloader:
  def __init__(self, uri, access_token, passphrase):
    self.uri = uri
    self.access_token = access_token
    self.passphrase = passphrase

  def call(self):
    response = requests.get(url = self.uri, headers = self.__headers())
    return aes256.decrypt(response.json()['encrypted_content'], self.passphrase)

  def __headers(self):
    return {
      'Content-Type': 'application/json',
      'Authorization': 'Token token={0}'.format(self.access_token)
    }
