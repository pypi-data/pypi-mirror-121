from occson.downloader import Downloader
from occson.uploader import Uploader

class Document:
  def __init__(self, uri, access_token, passphrase):
    self.uri = self.__build_uri(uri)
    self.access_token = access_token
    self.passphrase = passphrase

  def upload(self, content, force = False):
    return Uploader(self.uri, content, self.access_token, self.passphrase, force).call()

  def download(self):
    return Downloader(self.uri, self.access_token, self.passphrase).call()

  def __build_uri(self, uri):
    return uri.replace('ccs://', 'https://api.occson.com/')
