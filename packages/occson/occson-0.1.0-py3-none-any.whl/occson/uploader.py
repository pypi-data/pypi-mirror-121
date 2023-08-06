import requests
from AesEverywhere import aes256

class Uploader:
  def __init__(self, uri, content, access_token, passphrase, force):
    self.uri = uri
    self.content = content
    self.access_token = access_token
    self.passphrase = passphrase
    self.force = force

  def call(self):
    response = requests.post(url = self.uri, json = self.__data(), headers = self.__headers())
    return response.status_code == 200 or response.status_code == 201

  def __data(self):
    return {
      'encrypted_content': aes256.encrypt(self.content, self.passphrase),
      'force': 'true' if self.force else 'false'
    }

  def __headers(self):
    return {
      'Content-Type': 'application/json',
      'Authorization': 'Token token={0}'.format(self.access_token)
    }
