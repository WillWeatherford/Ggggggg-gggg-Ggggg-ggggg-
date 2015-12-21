import re

KEY_RE = re.compile(r'[A-Za-z]\s[Gg]+')


def encode(s):
    return s


def decode(s):
    parts = s.split('\n')
    keys_part = parts.pop(0)
    s = ' '.join(parts)

    keys = dict([reversed(k.split(' ')) for k in KEY_RE.findall(keys_part)])
    keys_re = re.compile(r'' + '|'.join([k for k in keys.keys()]))

    letters = []
    while s:
        print s[0]
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
