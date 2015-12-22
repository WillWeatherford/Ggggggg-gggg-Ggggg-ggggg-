import re
import string

KEY_RE = re.compile(r'(^|\s)[A-Za-z]{1}\s[Gg]{2,}')
MIN_CODEBIT_LEN = 2
BIT = ('g', 'G')


def encode(s):
    # count num of used chars, i.e. minimum amount of codebits needed
    chars = list(set(string.ascii_letters) & set(s))
    num_chars = len(chars)
    codebits = generate_codebits(num_chars)
    assert len(chars) == len(codebits)
    code = dict(zip(chars, codebits))
    keystring = ' '.join([' '.join(pair) for pair in code.items()])
    for char, codebit in code.items():
        s = s.replace(char, codebit)
    return '\n'.join((keystring, s))


def generate_codebits(n, all_codebits=None, prev_codebits=None):
    if all_codebits is None or prev_codebits is None:
        all_codebits, prev_codebits = [], list(BIT)

    new_codebits = [c + b for c in prev_codebits for b in BIT]

    delta = n - len(all_codebits)
    all_codebits.extend(new_codebits[:delta])

    if len(all_codebits) == n:
        return all_codebits
    return generate_codebits(n, all_codebits, new_codebits)


def decode(s):
    matches = list(KEY_RE.finditer(s))
    assert matches, 'Unable to match decoding key regular expression.'

    keys = dict([reversed(m.group().strip(' \n').split(' ')) for m in matches])
    assert keys, 'Unable to create decoding keys.'
    keys_re = re.compile(r'' + '|'.join([r'^' + k for k in keys.keys()]))

    last_match_end = matches[-1].end()
    s = s[last_match_end:].strip(' \n')

    letters = []
    while s:
        if s[0].isalpha():
            match = keys_re.match(s)
            if not match:
                raise TypeError('Unable to match a decode key pattern at start of string.')
            end_index = match.end()
        else:
            end_index = 1
        value = s[:end_index]
        value = keys.get(value, value)
        letters.append(value)
        s = s[end_index:]
    return ''.join(letters)
