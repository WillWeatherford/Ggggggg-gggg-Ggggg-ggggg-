import re
import string

KEY_RE = re.compile(r'(^|\s)[A-Za-z]{1}\s[Gg]{2,}')
MIN_CODEBIT_LEN = 2
BIT = ('g', 'G')


class Node(object):
    def __init__(self):
        self.bits = ''
        self.parent = None

    def assign_bits(self):
        if not hasattr(self, 'children'):
            return
        for i, c in enumerate(self.children):
            c.bits = self.bits + BIT[i]
            c.assign_bits()

    def get_code(self):
        if not hasattr(self, 'children'):
            return {self.char: self.bits}
        else:
            code = {}
            for c in self.children:
                code.update(c.get_code())
            return code


class InnerNode(Node):
    def __init__(self, children):
        super(InnerNode, self).__init__()
        self.children = children
        for c in children:
            c.parent = self
        print('InnerNode created. children:\n\t{}'.format('\n\t'.join(
            [str(c) for c in self.children])))

    @property
    def count(self):
        return sum([c.count for c in self.children])


class CharNode(Node):
    def __init__(self, char, count):
        super(CharNode, self).__init__()
        self.char = char
        self.count = count

    def __str__(self):
        return 'Char "{}"; count: {}, bits: {}'.format(self.char, self.count,
                                                       self.bits)


def char_count(s):
    chars = list(set(string.ascii_letters) & set(s))
    chars = [CharNode(char, s.count(char)) for char in chars]
    return chars


def encode(s):
    # count num of used chars, i.e. minimum amount of codebits needed
    chars = char_count(s)
    queue = list(chars)
    while len(queue) > 1:
        print('Re-sorting queue...')
        queue = sorted(queue, key=lambda c: c.count)
        print('Queue re-sorted. Length: {}'.format(len(queue)))
        newnode = InnerNode((queue.pop(0), queue.pop(0)))  # get first 2 (lowest count) from queue
        queue.append(newnode)
    print('Exited while loop.')
    root = queue.pop()
    root.assign_bits()  # combine
    code = root.get_code()  # into one func
    print(code)
    keystring = ' '.join([' '.join(pair) for pair in code.items()])
    for char, codebit in code.items():
        s = s.replace(char, codebit)
    return '\n'.join((keystring, s))


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
