import re

KEY_RE = re.compile(r'(^|\s)[A-Za-z]{1}\s[Gg]+')


def encode(s):
    return s


def decode(s):
    matches = list(KEY_RE.finditer(s))
    assert matches, 'Unable to match decoding key regular expression.'

    keys = dict([reversed(m.group().strip(' \n').split(' ')) for m in matches])
    assert keys, 'Unable to create decoding keys.'
    keys_re = re.compile(r'' + '|'.join([r'^' + k for k in keys.keys()]))

    last_match_end = matches[-1].end()
    s = s[last_match_end:].replace('\n', ' ').strip()

    letters = []
    while s:
        # print s[0]
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
