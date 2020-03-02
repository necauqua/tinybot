#!/usr/bin/python

import keyword
import re
from collections import namedtuple
from html.parser import HTMLParser

import requests


class Node:

    def __init__(self, tag, attrs):
        self.tag = tag
        self.attrs = attrs
        self.parent = None
        self.idx = -1
        self.children = []

    def add_to_tree(self, parent):
        self.parent = parent
        self.idx = len(parent.children)
        parent.children.append(self)

    def get_sibling(self, offset=1):
        siblings = self.parent.children
        idx = self.idx + offset
        return siblings[idx] if 0 <= idx < len(siblings) else None

    def find_by_tag(self, tag, limit=-1):
        res = []
        if limit == 0:
            return res
        if self.tag == tag:
            res.append(self)
            if limit == 1:
                return res
        if limit == -1:
            for child in self.children:
                res.extend(child.find_by_tag(tag))
            return res
        for child in self.children:
            res.extend(child.find_by_tag(tag, limit - len(res)))
            if len(res) >= limit:
                break
        return res

    def get_text(self):
        if self.tag == 'br':
            return '\n'
        return ''.join(map(lambda child: child.get_text(), self.children))

    def prn(self):
        return "<{0}{1}>{2}</{0}>".format(
            self.tag,
            '' if len(self.attrs) == 0 else ' ' + ' '.join(map(lambda x: '{}="{}"'.format(*x), self.attrs)),
            ''.join(map(lambda x: x.prn(), self.children))
        )


class Text(Node):

    def __init__(self, text):
        super().__init__('', tuple())
        self.text = text

    def get_text(self):
        return self.text

    def prn(self):
        return self.text


class MyParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.stack = []
        self.root = None

    def handle_starttag(self, tag, attrs):
        self.stack.append(Node(tag, attrs))

        if tag == 'br' or tag == 'meta' or tag == 'link':
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if len(self.stack) == 1:
            self.root = self.stack[0]
        elif len(self.stack) > 1:
            parent, child = self.stack[-2:]
            child.add_to_tree(parent)
        self.stack.pop()

    def handle_data(self, data):
        if len(self.stack) != 0:
            node = self.stack[-1]
            data = data.strip() if node.tag != 'p' and node.tag != 'td' else data
            if data != '':
                Text(data).add_to_tree(self.stack[-1])

    def error(self, message):
        raise Exception('parse error: ' + message)


Param = namedtuple('Param', ('name', 'tpe', 'doc', 'optional'))
Entity = namedtuple('Entity', ('name', 'params', 'doc'))

primitive_mapping = {
    'Integer': 'int',
    'Float': 'float',
    'String': 'str',
    'Boolean': 'bool',
    'True': 'bool',
    'False': 'bool'
}


def parse_type(raw, optional=False):
    def parse_type_impl(s):
        if s.endswith(' number'):
            s = s[:-7]

        if s.startswith('Array of'):
            s = parse_type(s[9:])
            return 'List[' + s + ']'
        union = s.split(' or ')
        if len(union) > 1:
            return 'Union[' + ', '.join(map(parse_type_impl, union)) + ']'
        return primitive_mapping.get(s, s)

    raw = parse_type_impl(raw)
    return 'Optional[{}]'.format(raw) if optional else raw


def main():
    text = requests.get('https://core.telegram.org/bots/api').text

    parser = MyParser()
    parser.feed(text)

    types = []
    methods = []

    for found in parser.root.find_by_tag('h4'):
        entity = found.get_text()
        if ' ' in entity:
            continue
        doc = found.get_sibling(1).get_text()

        is_method = entity[0].islower()
        params = []

        table = found.get_sibling(2)
        if table and table.tag == 'table':
            tbody = table.children[1]

            for tr in tbody.children:
                name = tr.children[0].get_text()
                if is_method:
                    optional = tr.children[2].get_text() != 'Yes'
                    pdoc = tr.children[3].get_text()
                else:
                    pdoc = tr.children[2].get_text()
                    optional = pdoc.startswith('Optional. ')

                tpe = parse_type(tr.children[1].get_text(), optional)

                if keyword.iskeyword(name) or name in dir(__builtins__):
                    name = name + '_'

                params.append(Param(name, tpe, pdoc, optional))

        (methods if is_method else types).append(Entity(entity, params, doc))

    newline_fix = re.compile('(\n+)')

    def gen_docstring(content, indent):
        sindent = ' ' * indent
        if '\n' in content:
            content = '\n' + sindent + newline_fix.sub('\\1' + sindent, content) + '\n' + sindent
        return '{}"""{}"""'.format(sindent, content)

    def gen_params(ps):
        shifted = sorted(ps, key=lambda p: int(p.optional))
        typed = map(lambda p: ', ' + p.name + ': ' + p.tpe + (' = None' if p.optional else ''), shifted)
        return ''.join(typed)

    def gen_param_docs(ps):
        return '\n'.join(map(lambda p: ':param {}: {}'.format(p.name, p.doc), ps))

    prelude = 'from __future__ import annotations\n\n' \
              'from typing import *\n' \
              'from typing.io import *\n\n\n'

    init_template = '    def __init__(self{}):\n{}\n        {}\n\n'
    cls_template = 'class {}:\n{}\n\n'
    method_template = '    def {}(self{}):\n{}\n        ...\n\n'

    with open('tinybot/typez.py', 'w') as f:
        f.write(prelude)
        for tpe in types:
            if len(tpe.params) != 0:
                setters = '\n        '.join(map(lambda p: 'self.{0} = {0}'.format(p.name), tpe.params))
                docs = gen_param_docs(tpe.params)
                init = init_template.format(gen_params(tpe.params), gen_docstring(docs, 8), setters)
            else:
                init = ''

            f.write(cls_template.format(tpe.name, gen_docstring(tpe.doc, 4)) + init + '\n')

        with open('overrides.txt') as f2:
            f.write(f2.read())

    with open('tinybot/webapi.pyi', 'w') as f:
        f.write(prelude)
        f.write('from tinybot.types import *\n\n'
                'Response = Union[Awaitable[...], ...]\n\n')
        f.write('class TelegramAPI:\n\n')

        for method in methods:
            if len(method.params) != 0:
                docs = method.doc + '\n\n' + gen_param_docs(method.params)
            else:
                docs = method.doc

            name = re.sub('[a-z][A-Z]', lambda x: x[0][0] + '_' + x[0][1].lower(), method.name)
            f.write(method_template.format(name, gen_params(method.params), gen_docstring(docs, 8)))

    # print()
    # print()

    # for method in methods:
    #     print(method)


if __name__ == '__main__':
    main()
