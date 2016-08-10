#!/usr/bin/python

import argparse
import os.path
import struct

from config import Config

from Crypto.Cipher import AES

def main():
    parser = argparse.ArgumentParser(
        description='Decrypts a file. Requires a key config.'
    )

    parser.add_argument(
        'input',
        help='Input file'
    )
    parser.add_argument(
        'output',
        help='Output file'
    )
    parser.add_argument(
        'config',
        help='File containing the configuration',
        default='config.json'
    )
    parser.add_argument(
        '--buffsize',
        help='Size of the buffer to read',
        default=4096
    )

    args = parser.parse_args()
    c = Config(args.config)
   
    decryptor = AES.new(c.keyStore.key, AES.MODE_CBC, IV=c.keyStore.iv)

    with open(args.input, 'rb') as infile:
        with open(args.output, 'wb') as outfile:
            filesize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            while True:
                buff = infile.read(args.buffsize)
                l = len(buff)
                if l == 0:
                    break
                outfile.write(decryptor.decrypt(buff))
            outfile.truncate(filesize)

if __name__ == '__main__':
    main()

