import re
import string

KEY_RE = re.compile(r'(^|\s)[A-Za-z]{1}\s[Gg]{2,}')
MIN_CODEBIT_LEN = 2
BIT = ('g', 'G')


class InnerNode(object):
    def __init__(self, children):
        self.children = children
        self.bits = ''
        # print('InnerNode created. children:\n\t{}'.format('\n\t'.join(
        #     [str(c) for c in self.children])))

    @property
    def count(self):
        return sum([c.count for c in self.children])

    def get_code(self):
        code = {}
        children = sorted(self.children, key=lambda c: c.count, reverse=True)
        for i, c in enumerate(children):
            c.bits = self.bits + BIT[i]
            code.update(c.get_code())
        return code


class CharNode(object):
    def __init__(self, char, count):
        self.char = char
        self.count = count
        self.bits = ''

    def __str__(self):
        return 'Char "{}"; count: {}, bits: {}'.format(self.char, self.count,
                                                       self.bits)

    def get_code(self):
        return {self.char: self.bits}


def encode(s):
    chars = list(set(string.ascii_letters) & set(s))
    queue = [CharNode(char, s.count(char)) for char in chars]

    while len(queue) > 1:
        queue = sorted(queue, key=lambda c: c.count)
        newnode = InnerNode((queue.pop(0), queue.pop(0)))
        queue.append(newnode)
    root = queue.pop()
    code = root.get_code()

    keystring = ' '.join([' '.join(pair) for pair in code.items()])
    encoded = ''.join([code[c] if c.isalpha() else c for c in s])
    return '\n'.join((keystring, encoded))


def decode(s):
    matches = list(KEY_RE.finditer(s))

    keys = dict([reversed(m.group().strip(' \n').split(' ')) for m in matches])
    keys_re = re.compile(r'' + '|'.join([r'^' + k for k in keys.keys()]))

    last_match_end = matches[-1].end()
    s = s[last_match_end:].strip(' \n')

    letters = []
    while s:
        if s[0].isalpha():
            match = keys_re.match(s)
            if not match:
                raise TypeError('Unable to match a decode key pattern at start '
                                'of string. Decoded so far:\n{}'.format(
                                    ''.join(letters)))
            end_index = match.end()
        else:
            end_index = 1
        value = s[:end_index]
        value = keys.get(value, value)
        letters.append(value)
        s = s[end_index:]
    return ''.join(letters)
