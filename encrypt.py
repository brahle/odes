#!/usr/bin/python

import argparse
import os.path
import struct

from config import Config

from Crypto.Cipher import AES

def main():
    parser = argparse.ArgumentParser(
        description='Encrypts a file. Uses either an existing key or generates a new one'
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
        '--config',
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
   
    encryptor = AES.new(c.keyStore.key, AES.MODE_CBC, IV=c.keyStore.iv)
    filesize = os.path.getsize(args.input)

    with open(args.input, 'rb') as infile:
        with open(args.output, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            while True:
                buff = infile.read(args.buffsize)
                l = len(buff)
                if l == 0:
                    break
                if l % 16 != 0:
                    buff += 'B' * (16 - l % 16)
                outfile.write(encryptor.encrypt(buff))

if __name__ == '__main__':
    main()

