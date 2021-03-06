#!/usr/bin/env python3
"""
Author : Brad Fulton
Date   : 03 June 2020
Purpose: Encoding and decoding text using the Caesar Cipher
"""

import argparse
import os
import string
import sys


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Encoding and decoding text using the Caesar Cipher',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('text', metavar='text', help='Input text or file')

    parser.add_argument('-n',
                        '--num',
                        help='Shift this many spaces',
                        metavar='int',
                        type=int,
                        default=3)

    parser.add_argument('-o',
                        '--outfile',
                        help='Output filename',
                        metavar='str',
                        type=str,
                        default='')

    parser.add_argument('-d',
                        '--decode',
                        help='Decode text',
                        action='store_true')

    args = parser.parse_args()
    num = args.num
    text = args.text

    if not 1 <= num <= 93:
        parser.error(f'--num "{num}" must be between 1 and 93')

    if os.path.isfile(text):
        args.text = open(text).read().rstrip()

    return args


# --------------------------------------------------
def caesar_cipher_encode(n, text):
    """
    Returns a string where the characters in text are shifted right n number of spaces.

    Ex.  str = 'abc12'
         n = 3

         returns - 'def45'

    Notes:

    p = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'

    str.maketrans returns a translation table that replaces items in p with items in p[n:] + p[:n],
    which is just the string p shifted to the right n units.

    my_str.translate(lookup_table) returns a copy of my_str using the lookup table.
    """
    p = string.printable.strip(string.whitespace)
    lookup_table = str.maketrans(p, p[n:] + p[:n])

    return text.translate(lookup_table)


# --------------------------------------------------
def caesar_cipher_decode(n, text):
    """
    Returns a string where the characters in text are shifted left n number of spaces.

    Ex.  str = 'def45'
         n = 3

         returns - 'abc12'

    Notes:

    p = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'

    str.maketrans returns a translation table that replaces items in p with items in p[-n:] + p[:-n],
    which is just the string p shifted to the left n units.

    my_str.translate(lookup_table) returns a copy of my_str using the lookup table.
    """
    p = string.printable.strip(string.whitespace)
    lookup_table = str.maketrans(p, p[-n:] + p[:-n])

    return text.translate(lookup_table)


# --------------------------------------------------
def main():
    """Encode and decode text using the command-line."""

    args = get_args()
    text = args.text
    n = args.num
    outfile = args.outfile
    decode = args.decode

    out_fh = open(outfile, 'wt') if outfile else sys.stdout
    out_fh.write(caesar_cipher_decode(n, text)) if decode else out_fh.write(
        caesar_cipher_encode(n, text))
    out_fh.write('\n')
    out_fh.close()


# --------------------------------------------------
if __name__ == '__main__':
    main()
