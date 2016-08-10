#!/usr/bin/python

import json
import os.path

from keystore import KeyStore

class Config(object):
    
    def __init__(self, name='config.txt'):
        self.name = name
        try:
            data = self._load_from_file()
            self.version = data['version']
            self.keyStore = KeyStore(data['keystore'])
        except IOError as e:
            self._generate_new()
        except ValueError as e:
            self._generate_new()
        
    def _load_from_file(self):
        with open(self.name) as f:
            data = json.loads(f.read())
            return {
                'version': data['version'],
                'keystore': data['keystore']
            }

    def _generate_new(self):
        self.version = 1
        self.keyStore = KeyStore()
        self.save()

    def save(self):
        with open(self.name, 'w') as f:
            f.write(str(self))

    def to_config(self):
        return {
            'version': self.version,
            'keystore': self.keyStore.to_config()
        }

    def __str__(self):
        return json.dumps(self.to_config()) 

def main():
    c = Config()
    print c

if __name__ == '__main__':
    main()
