#!/usr/bin/env python3
"""tests for cc_encode.py"""

import os
import random
import re
import string
from subprocess import getstatusoutput, getoutput

prg = './cc_encode.py'
decode = '-d'
lower_case = '-l'
fox = './inputs/fox.txt'
encoded_fox = './inputs/encoded_fox.txt'
encoded_fox_lc = './inputs/encoded_fox_lower_case.txt'
bustle = './inputs/the-bustle.txt'
spiders = './inputs/spiders.txt'
encoded_spiders = './inputs/encoded_spiders.txt'


# --------------------------------------------------
def test_exists():
    """exists"""

    assert os.path.isfile(prg)


# --------------------------------------------------
def test_usage():
    """usage"""

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'{prg} {flag}')
        assert rv == 0
        assert re.match("usage", out, re.IGNORECASE)


# --------------------------------------------------
def test_bad_num():
    """test bad_num"""

    for n in [random.choice(r) for r in (range(-10, 0), range(94, 104))]:
        rv, out = getstatusoutput(f'{prg} -n {n} hello')
        assert rv != 0
        assert re.search(f'--num "{n}" must be between 1 and 93', out)


# --------------------------------------------------
def test_bad_num_lower_case():
    """test bad_num"""

    for n in [random.choice(r) for r in (range(-10, 0), range(26, 36))]:
        rv, out = getstatusoutput(f'{prg} {lower_case} -n {n} hello')
        assert rv != 0
        assert re.search(f'--num "{n}" must be between 1 and 25', out)


# --------------------------------------------------
def test_encode_text1():
    """Text"""

    out = getoutput(f'{prg} foobar')
    assert out.strip() == 'irredu'


# --------------------------------------------------
def test_decode_text1():
    """Text"""

    out = getoutput(f'{prg} {decode} irredu')
    assert out.strip() == 'foobar'


# --------------------------------------------------
def test_decode_fox_text_using_2():
    """Text"""

    text = 'Vjg1swkem1dtqyp1hqz1lworu1qxgt1vjg1ncBA1fqi:'
    expected = 'The quick brown fox jumps over the lazy dog.'
    out = getoutput(f'{prg} {decode} "{text}" -n 2')
    # assert out.strip() == expected
    assert out == expected


# --------------------------------------------------
def test_file_bustle():
    """File input"""

    expected = """
Wkh2exvwoh2lq2d2krxvh
Wkh2pruqlqj2diwhu2ghdwk
Lv2vrohpqhvw2ri2lqgxvwulhv
Hqdfwhg2xsrq2hduwk/::

Wkh2vzhhslqj2xs2wkh2khduw/
Dqg2sxwwlqj2oryh2dzdB
Zh2vkdoo2qrw2zdqw2wr2xvh2djdlq
Xqwlo2hwhuqlwB;
""".strip()

    out = getoutput(f'{prg} {bustle}')
    assert out.strip() == expected.strip()


# --------------------------------------------------
def test_decode_file_bustle():
    """File input"""

    text = """
Wkh2exvwoh2lq2d2krxvh
Wkh2pruqlqj2diwhu2ghdwk
Lv2vrohpqhvw2ri2lqgxvwulhv
Hqdfwhg2xsrq2hduwk/::

Wkh2vzhhslqj2xs2wkh2khduw/
Dqg2sxwwlqj2oryh2dzdB
Zh2vkdoo2qrw2zdqw2wr2xvh2djdlq
Xqwlo2hwhuqlwB;
""".strip()

    expected = """
The bustle in a house
The morning after death
Is solemnest of industries
Enacted upon earth,--

The sweeping up the heart,
And putting love away
We shall not want to use again
Until eternity.
""".strip()

    out = getoutput(f'{prg} {decode} "{text}"')
    assert out.strip() == expected.strip()


# --------------------------------------------------
def test_file_fox():
    """File input"""

    out = getoutput(f'{prg} --num 4 {fox}')
    assert out.strip() == 'Xli3uymgo3fvsAr3jsB3nyqtw3sziv3xli3peDC3hsk<'


# --------------------------------------------------
def test_decode_file_fox():
    """File input"""

    out = getoutput(f'{prg} {decode} --num 4 {encoded_fox}')
    assert out.strip() == 'The quick brown fox jumps over the lazy dog.'


def test_file_fox_lower_case():
    """File input"""

    out = getoutput(f'{prg} {lower_case} --num 4 {fox}')
    assert out.strip() == 'Tli uymgo fvsar jsb nyqtw sziv xli pedc hsk.'


# --------------------------------------------------
def test_decode_file_fox_lower_case():
    """File input"""

    out = getoutput(f'{prg} {decode} {lower_case} --num 4 {encoded_fox_lc}')
    assert out.strip() == 'The quick brown fox jumps over the lazy dog.'


# --------------------------------------------------
def test_file_spiders():
    """File input"""

    out = getoutput(f'{prg} --num 9 {spiders}')
    expected = """Mxw:C8FxAAH?8ByrmnAB?
R8tnny8qxDBn
ljBDjuuH["""
    assert out.strip() == expected


# --------------------------------------------------
def test_decode_file_spiders():
    """File input"""

    out = getoutput(f'{prg} {decode} --num 9 {encoded_spiders}')
    expected = "Don't worry, spiders,\nI keep house\ncasually."
    assert out.strip() == expected


# --------------------------------------------------
def random_string():
    """generate a random string"""

    k = random.randint(5, 10)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))


# --------------------------------------------------
def out_flag():
    """Either -o or --outfile"""

    return '-o' if random.randint(0, 1) else '--outfile'


# --------------------------------------------------
def test_text_outfile():
    """Test STDIN/outfile"""

    out_file = random_string()
    if os.path.isfile(out_file):
        os.remove(out_file)

    try:
        out = getoutput(f'{prg} {out_flag()} {out_file} "foo bar baz"')
        assert out.strip() == ''
        assert os.path.isfile(out_file)
        text = open(out_file).read().rstrip()
        assert text == 'irr2edu2edC'
    finally:
        if os.path.isfile(out_file):
            os.remove(out_file)


# --------------------------------------------------
def test_decode_text_outfile():
    """Test STDIN/outfile"""

    out_file = random_string()
    if os.path.isfile(out_file):
        os.remove(out_file)

    try:
        out = getoutput(
            f'{prg} {decode} {out_flag()} {out_file} "irr2edu2edC"')
        assert out.strip() == ''
        assert os.path.isfile(out_file)
        text = open(out_file).read().rstrip()
        assert text == 'foo bar baz'
    finally:
        if os.path.isfile(out_file):
            os.remove(out_file)


# --------------------------------------------------
def test_file():
    """Test file in/out"""

    for expected_file in os.listdir('test-encode-outs'):
        try:
            out_file = random_string()
            if os.path.isfile(out_file):
                os.remove(out_file)

            basename = os.path.basename(expected_file)
            in_file = os.path.join('./inputs', basename)
            out = getoutput(f'{prg} {out_flag()} {out_file} {in_file}')
            assert out.strip() == ''
            produced = open(out_file).read().rstrip()
            expected = open(os.path.join('test-encode-outs',
                                         expected_file)).read().strip()
            assert expected == produced
        finally:
            if os.path.isfile(out_file):
                os.remove(out_file)


# --------------------------------------------------
def test_decode_file():
    """Test file in/out"""

    for expected_file in os.listdir('test-decode-outs'):
        try:
            out_file = random_string()
            if os.path.isfile(out_file):
                os.remove(out_file)

            basename = os.path.basename(expected_file)
            in_file = os.path.join('./test-encode-outs', basename)
            out = getoutput(
                f'{prg} {decode} {out_flag()} {out_file} {in_file}')
            assert out.strip() == ''
            produced = open(out_file).read().rstrip()
            expected = open(os.path.join('test-decode-outs',
                                         expected_file)).read().strip()
            assert expected == produced
        finally:
            if os.path.isfile(out_file):
                os.remove(out_file)
