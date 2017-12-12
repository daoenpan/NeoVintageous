import re
from unittest import TestCase

from NeoVintageous.lib.cmds.vi_actions import _vi_gx as command

URL_REGEX = re.compile(command.URL_REGEX)


class Test_gx(TestCase):

    def assertMatch(self, expected, text):
        self.assertEqual(expected, command._url(URL_REGEX, text))

    def test_invalid(self):
        self.assertMatch(None, '')
        self.assertMatch(None, 'http')
        self.assertMatch(None, 'http://.com')

    def test_basic(self):
        self.assertMatch('http://example.com', 'http://example.com')
        self.assertMatch('https://example.com', 'https://example.com')

        self.assertMatch('http://EXAMPLE.COM', 'http://EXAMPLE.COM _xxx_')
        self.assertMatch('http://www.example.com', 'http://www.example.com _xxx_')
        self.assertMatch('http://sub.example.com', 'http://sub.example.com _xxx_')
        self.assertMatch('http://sub.sub.example.com', 'http://sub.sub.example.com _xxx_')

        self.assertMatch('http://example.com/x/y', 'http://example.com/x/y _xxx_')
        self.assertMatch('http://example.com/x/y.html', 'http://example.com/x/y.html _xxx_')
        self.assertMatch('http://example.com/x/y.html#x', 'http://example.com/x/y.html#x _xxx_')
        self.assertMatch('http://example.com/x/y.html#x-y', 'http://example.com/x/y.html#x-y _xxx_')
        self.assertMatch('http://example.com/x/y?a=b&c=42', 'http://example.com/x/y?a=b&c=42 _xxx_')
        self.assertMatch('http://example.com/x/y?a=b&c=42', 'http://example.com/x/y?a=b&c=42 _xxx_')

    def test_trailing_stop_is_ignored(self):
        self.assertMatch('http://example.com', 'http://example.com.')

    def test_trailing_parens_are_ignored(self):
        self.assertMatch('http://example.com', 'http://example.com)')
        self.assertMatch('http://example.com', 'http://example.com).')

    def test_markdown_links(self):
        # basic
        self.assertMatch('http://example.com', '[title](http://example.com)')
        # image
        self.assertMatch('https://example.com', '[![Alt](https://example.com)]')
