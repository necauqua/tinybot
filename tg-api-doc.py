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

    def render(self):
        return "<{0}{1}>{2}</{0}>".format(
            self.tag,
            '' if len(self.attrs) == 0 else ' ' + ' '.join(map(lambda x: '{}="{}"'.format(*x), self.attrs)),
            ''.join(map(lambda x: x.render(), self.children))
        )


class Text(Node):

    def __init__(self, text):
        super().__init__('', tuple())
        self.text = text

    def get_text(self):
        return self.text

    def render(self):
        return self.text


class Parser(HTMLParser):
    INLINE_TAGS = {'p', 'td'}

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
            data = data.strip() if node.tag not in Parser.INLINE_TAGS else data
            if data != '':
                Text(data).add_to_tree(self.stack[-1])

    def error(self, message):
        raise Exception('parse error: ' + message)


Param = namedtuple('Param', ('name', 'tpe', 'doc', 'optional'))
Entity = namedtuple('Entity', ('name', 'params', 'doc', 'ret'))

primitive_mapping = {
    'Integer': 'int',
    'Float': 'float',
    'String': 'str',
    'Boolean': 'bool',
    'True': 'bool',
    'False': 'bool',
    'true': 'bool',
    'false': 'bool'
}


def parse_type(raw, optional=False, default=None):
    if raw is None:
        return 'None', optional

    def parse_type_impl(s):
        # fixup for that one 'Float number' instead of a 'Float' type that telegram has
        if s.endswith(' number'):
            s = s[:-7]

        if s.startswith('Array of'):
            s, _ = parse_type(s[9:])
            return 'List[' + s + ']'
        union = s.split(' or ')
        if len(union) > 1:
            return 'Union[' + ', '.join(map(parse_type_impl, union)) + ']'
        return primitive_mapping.get(s, s)

    raw = parse_type_impl(raw)
    if default:
        return '{} = {}'.format(raw, default), False
    if optional:
        if raw == 'bool':  # all optional booleans default to false
            return 'bool = False', False
        return 'Optional[{}] = None'.format(raw), True
    return raw, optional


def main():
    text = requests.get('https://core.telegram.org/bots/api').text

    parser = Parser()
    parser.feed(text)

    types = []
    methods = []

    parents = {}

    for found in parser.root.find_by_tag('h4'):
        entity = found.get_text()
        if ' ' in entity:
            continue

        doc_elem = found.get_sibling(1)

        if not doc_elem:
            continue

        doc = doc_elem.get_text()
        is_method = entity[0].islower()

        ret = None
        if is_method:
            for em in doc_elem.find_by_tag('em'):
                txt = em.get_text()
                if txt == 'True':
                    ret = 'Boolean'
                elif txt.startswith('Int'):
                    ret = 'Integer'

            # in a couple of places Trues are not em'd
            if 'True is returned' in doc:
                ret = 'True'

            if not ret:
                for a in reversed(doc_elem.find_by_tag('a')):
                    txt = a.get_text()
                    if txt[0].isupper():
                        ret = txt
                        break

            if ret and re.search('[Aa]rray of', doc) is not None:
                ret = 'Array of ' + ret.rstrip('s')

        params = []

        table = found.get_sibling(2)
        while table.tag != 'h4':
            if table.tag == 'table':
                tbody = table.children[1]

                for tr in tbody.children:
                    name = tr.children[0].get_text()
                    if is_method:
                        optional = tr.children[2].get_text() != 'Yes'
                        pdoc = tr.children[3].get_text()
                    else:
                        pdoc = tr.children[2].get_text()
                        optional = pdoc.startswith('Optional. ')

                    default = re.search('[Dd]efaults to ([^ ]*?)(?:[.,]|$)', pdoc)
                    if default is not None:
                        default = default.group(1) \
                            .replace('true', 'True') \
                            .replace('false', 'False') \
                            .replace('“', '\'') \
                            .replace('”', '\'')

                    tpe, optional = parse_type(tr.children[1].get_text(), optional, default)

                    if keyword.iskeyword(name):
                        name = name + '_'

                    params.append(Param(name, tpe, pdoc, optional))

                break
            elif table.tag == 'ul':
                for li in table.children:
                    parents[li.get_text()] = entity
                break
            else:
                table = table.get_sibling()

        (methods if is_method else types).append(Entity(entity, params, doc, parse_type(ret)[0]))

    newline_fix = re.compile('(\n+)')

    def fix_param(n):
        return n + '_' if n in dir(__builtins__) else n

    def gen_docstring(content, indent):
        sindent = ' ' * indent
        if '\n' in content:
            content = '\n' + sindent + newline_fix.sub('\\1' + sindent, content) + '\n' + sindent
        return '{}"""{}"""'.format(sindent, content)

    def gen_params(ps):
        shifted = sorted(ps, key=lambda p: 2 if p.optional else 1 if p.tpe.startswith('bool') else 0)
        typed = map(lambda p: ', ' + fix_param(p.name) + ': ' + p.tpe, shifted)
        return ''.join(typed)

    def gen_param_docs(ps):
        return '\n'.join(map(lambda p: ':param {}: {}'.format(fix_param(p.name), re.sub('\n+\\s*', ' ', p.doc)), ps))

    init_template = '    def __init__(self{}):\n{}\n        {}\n\n'
    cls_template = 'class {}({}__Dynamic):\n{}\n\n    __params = ({})\n\n{}\n'
    method_template = '    def {}(self{}) -> {}:\n{}\n        ...\n\n'

    with open('tinybot/gen/__init__.py', 'w') as f:
        f.write('#\n'
                '# THIS CODE IS AUTOGENERATED\n'
                '# REPEATING DOCS FOR PARAMS AND INSTANCE FIELDS ARE INTENDED\n'
                '#\n'
                '\n'
                'from __future__ import annotations\n'
                '\n'
                'from typing import *\n'
                'from typing.io import *\n'
                'from tinybot.webapi import DynamicDictObject\n'
                '\n'
                '\n'
                'class __Dynamic:\n'
                '\n'
                '    def __new__(cls, *args, **kwargs):\n'
                '        params = getattr(cls, \'_{}__params\'.format(cls.__name__))\n'
                '        return DynamicDictObject({**{k: v for k, v in zip(params, args)}, **kwargs})\n'
                '\n'
                '\n')

        for tpe in types:
            if len(tpe.params) != 0:

                def gen_setter(p):
                    return 'self.{} = {}\n{}'.format(p.name, fix_param(p.name), gen_docstring(p.doc, 8))

                setters = '\n        '.join(map(gen_setter, tpe.params))

                docs = gen_param_docs(tpe.params)
                init = init_template.format(gen_params(tpe.params), gen_docstring(docs, 8), setters)
            else:
                init = ''

            parent = parents.get(tpe.name)
            parent = parent + ', ' if parent else ''

            params = ', '.join(map(lambda p: '\'' + p.name + '\'', tpe.params))
            f.write(cls_template.format(tpe.name, parent, gen_docstring(tpe.doc, 4), params, init))

        with open('overrides.txt') as f2:
            f.write(f2.read())

    with open('tinybot/webapi.pyi', 'w') as f:
        f.write('#\n'
                '# THIS CODE IS AUTOGENERATED\n'
                '# IDENTICAL BLOCKING AND NON-BLOCKING APIS ARE INTENDED\n'
                '#\n'
                '\n'
                'from tinybot.gen import *\n'
                '\n'
                '\n'
                'class DynamicDictObject:\n'
                '\n'
                '    def __init__(self, peer: Union[list, dict, Any], name: str = \'\'):'
                '\n'
                '        ...\n'
                '\n'
                '\n')

        f.write('class TelegramAPI:\n\n')

        for method in methods:
            if len(method.params) != 0:
                docs = method.doc + '\n\n' + gen_param_docs(method.params)
            else:
                docs = method.doc

            name = re.sub('[a-z][A-Z]', lambda x: x[0][0] + '_' + x[0][1].lower(), method.name)

            aret = 'Awaitable[{0}]'.format(method.ret)

            f.write(method_template.format(name, gen_params(method.params), aret, gen_docstring(docs, 8)))

        f.write('\n# .. AND MAKE IT DOUBLE, HAHAHA\n\n\nclass BlockingTelegramAPI:\n\n')

        for method in methods:
            if len(method.params) != 0:
                docs = method.doc + '\n\n' + gen_param_docs(method.params)
            else:
                docs = method.doc

            name = re.sub('[a-z][A-Z]', lambda x: x[0][0] + '_' + x[0][1].lower(), method.name)

            f.write(method_template.format(name, gen_params(method.params), method.ret, gen_docstring(docs, 8)))

    # print()
    # print()

    # for method in methods:
    #     print(method)


if __name__ == '__main__':
    main()
