#!/usr/bin/python

import base64
import json
import os.path

class KeyStore(object):

    def __init__(self, keyConfig=None):
        if keyConfig is None:
            self.generate_new()
        else:
            self.key = base64.urlsafe_b64decode(keyConfig['key'].encode('ascii'))
            self.iv = base64.urlsafe_b64decode(keyConfig['iv'].encode('ascii'))

    def generate_new(self):
        self.key = self._generate_new_key()
        self.iv = self._generate_new_iv()

    def _generate_new_key(self):
        return os.urandom(32)
    
    def _generate_new_iv(self):
        return os.urandom(16)
    
    def to_config(self):
        return {
            'key': base64.urlsafe_b64encode(self.key),
            'iv': base64.urlsafe_b64encode(self.iv)
        }

    def __str__(self):
        return json.dumps(self.to_config())

def main():
    k = KeyStore()
    print k

if __name__ == '__main__':
    main()

