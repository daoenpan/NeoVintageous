# Copyright (C) 2018 The NeoVintageous Team (NeoVintageous).
#
# This file is part of NeoVintageous.
#
# NeoVintageous is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NeoVintageous is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NeoVintageous.  If not, see <https://www.gnu.org/licenses/>.

from NeoVintageous.tests import unittest

from NeoVintageous.nv.ex.parser.nodes import CommandLineNode
from NeoVintageous.nv.ex.parser.nodes import RangeNode
from NeoVintageous.nv.ex.parser.scanner_command_substitute import TokenCommandSubstitute
from NeoVintageous.nv.ex.parser.tokens import TokenDigits
from NeoVintageous.nv.ex.parser.tokens import TokenMark
from NeoVintageous.nv.ex.parser.tokens import TokenOffset
from NeoVintageous.nv.ex.parser.tokens import TokenPercent
from NeoVintageous.nv.ex.parser.tokens import TokenSearchBackward
from NeoVintageous.nv.ex.parser.tokens import TokenSearchForward


class TestRangeNode(unittest.TestCase):

    def test_can_instantiate(self):
        node = RangeNode('foo', 'bar', ';')
        node.start_offset = [10]
        node.end_offset = [10]
        self.assertEqual(node.start, 'foo')
        self.assertEqual(node.end, 'bar')
        self.assertEqual(node.start_offset, [10])
        self.assertEqual(node.end_offset, [10])
        self.assertEqual(node.separator, ';')

    def test_can_detect_if_its_empty(self):
        node = RangeNode()
        self.assertTrue(node.is_empty)


class TestCommandLineNode(unittest.TestCase):

    def test_can_instantiate(self):
        range_node = RangeNode("foo", "bar", False)
        range_node.start_offset = [10]
        range_node.end_offset = [10]
        command = TokenCommandSubstitute({})
        node = CommandLineNode(range_node, command)
        self.assertEqual(range_node, node.line_range)
        self.assertEqual(command, node.command)


class TestRangeNodeResolveNotation(unittest.ViewTestCase):

    def test_returs_current_line_if_range_is_empty(self):
        self.write('''aaa aaa
bbb bbb
ccc ccc
''')
        self.select(8)
        region = RangeNode().resolve(self.view)
        self._assertRegionsEqual(self.Region(8, 16), region)

    def test_returs_current_line_if_range_is_empty2(self):
        self.write('''aaa aaa
bbb bbb
ccc ccc
''')
        self.select(0)
        region = RangeNode().resolve(self.view)
        self._assertRegionsEqual(self.Region(0, 8), region)

    def test_returs_current_line_if_range_is_empty_and_adds_offset(self):
        self.write('''aaa aaa
bbb bbb
ccc ccc
ddd ddd
''')
        self.select(0)
        region = RangeNode(start=[TokenOffset([1, 1])]).resolve(self.view)
        self._assertRegionsEqual(self.Region(16, 24), region)

    def test_returs_current_line_if_range_is_empty_and_adds_offsets(self):
        self.write('''aaa aaa
bbb bbb
ccc ccc
ddd ddd
''')
        self.select(0)
        region = RangeNode(start=[TokenOffset([2])]).resolve(self.view)
        self._assertRegionsEqual(self.Region(16, 24), region)

    def test_returs_requested_start_line_number(self):
        self.write('''aaa aaa
bbb bbb
ccc ccc
ddd ddd
''')
        self.select(0)
        region = RangeNode(start=[TokenDigits('2')]).resolve(self.view)

        self._assertRegionsEqual(self.Region(8, 16), region)

    def test_returs_requested_start_line_number_and_adds_offset(self):
        self.write('''aaa aaa
bbb bbb
ccc ccc
ddd ddd
''')
        self.select(0)
        region = RangeNode(start=[TokenDigits('2'), TokenOffset([2])]).resolve(self.view)
        self._assertRegionsEqual(self.Region(24, 32), region)

    def test_returs_requested_start_line_number_and_adds_offset2(self):
        self.write('''aaa aaa
bbb bbb
ccc ccc
ddd ddd
''')
        self.select(0)
        region = RangeNode(start=[TokenDigits('2'), TokenOffset([1])]).resolve(self.view)
        self._assertRegionsEqual(self.Region(16, 24), region)

    def test_returs_whole_buffer_if_percent_requested(self):
        self.write('''aaa aaa
bbb bbb
ccc ccc
ddd ddd
''')
        self.select(0)
        region = RangeNode(start=[TokenPercent()]).resolve(self.view)
        self._assertRegionsEqual(self.Region(0, 32), region)


class Tests_SearchForward(unittest.ViewTestCase):

    def test_can_search_forward(self):
        self.write('''aaa aaa
bbb bbb
ccc cat
ddd cat
''')
        self.select(0)
        region = RangeNode(start=[TokenSearchForward('cat')]).resolve(self.view)
        self._assertRegionsEqual(self.Region(16, 24), region)

    def test_can_search_forward_with_offset(self):
        self.write('''aaa aaa
bbb bbb
ccc cat
ddd ddd
''')
        self.select(0)
        region = RangeNode(start=[TokenSearchForward('cat'), TokenOffset([1])]).resolve(self.view)
        self._assertRegionsEqual(self.Region(24, 32), region)

    def test_failed_search_throws(self):
        self.write('''aaa aaa
bbb bbb
ccc cat
ddd cat
''')
        self.select(0)
        line_range = RangeNode(start=[TokenSearchForward('dog')])
        self.assertRaises(ValueError, line_range.resolve, self.view)

    def test_can_search_multiple_times_forward(self):
        self.write('''aaa aaa
bbb bbb
ccc cat
ddd ddd
eee eee
fff cat
''')
        self.select(0)
        region = RangeNode(start=[TokenSearchForward('cat'), TokenSearchForward('cat')]).resolve(self.view)
        self._assertRegionsEqual(self.Region(40, 48), region)


class Tests_SearchBackward(unittest.ViewTestCase):

    def test_can_search_backward(self):
        self.write('''aaa aaa
bbb bbb
ccc cat
ddd ddd
xxx xxx
''')
        self.select(self.view.size())
        region = RangeNode(start=[TokenSearchBackward('cat')]).resolve(self.view)
        self._assertRegionsEqual(self.Region(16, 24), region)

    def test_can_search_backward_with_offset(self):
        self.write('''aaa aaa
bbb bbb
ccc cat
ddd ddd
xxx xxx
''')
        self.select(self.view.size())
        region = RangeNode(start=[TokenSearchBackward('cat'), TokenOffset([1])]).resolve(self.view)
        self._assertRegionsEqual(self.Region(24, 32), region)

    def test_failed_search_throws(self):
        self.write('''aaa aaa
bbb bbb
ccc cat
ddd cat
''')
        self.select(self.view.size())
        line_range = RangeNode(start=[TokenSearchBackward('dog')])
        self.assertRaises(ValueError, line_range.resolve, self.view)

    def test_can_search_multiple_times_backward(self):
        self.write('''aaa aaa
bbb bbb
ccc cat
ddd cat
eee eee
fff fff
''')
        self.select(self.view.size())
        region = RangeNode(start=[TokenSearchBackward('cat'), TokenSearchBackward('cat')]).resolve(self.view)
        self._assertRegionsEqual(self.Region(16, 24), region)


class Tests_Line0(unittest.ViewTestCase):

    def test_can_calculate_visual_start(self):
        self.write('''xxx xxx
aaa aaa
xxx xxx
bbb bbb
''')
        self.select((8, 10))
        region = RangeNode(start=[TokenDigits('0')]).resolve(self.view)
        self._assertRegionsEqual(self.Region(-1, -1), region)


class Tests_Marks(unittest.ViewTestCase):

    def test_can_calculate_visual_start(self):
        self.write('''xxx xxx
aaa aaa
xxx xxx
bbb bbb
''')
        self.select((8, 10))
        region = RangeNode(start=[TokenMark("<")]).resolve(self.view)
        self._assertRegionsEqual(self.Region(8, 16), region)

    def test_can_calculate_visual_start_with_multiple_sels(self):
        self.write('''xxx xxx
aaa aaa
xxx xxx
bbb bbb
xxx xxx
ccc ccc
''')
        self.select([(8, 10), (24, 27)])
        region = RangeNode(start=[TokenMark("<")]).resolve(self.view)
        self._assertRegionsEqual(self.Region(8, 16), region)

    def test_can_calculate_visual_end(self):
        self.write('''xxx xxx
aaa aaa
xxx xxx
bbb bbb
''')
        self.select((8, 10))
        region = RangeNode(start=[TokenMark(">")]).resolve(self.view)
        self._assertRegionsEqual(self.Region(8, 16), region)

    def test_can_calculate_visual_end_with_multiple_sels(self):
        self.write('''xxx xxx
aaa aaa
xxx xxx
bbb bbb
xxx xxx
ccc ccc
''')
        self.select((8, 10))
        region = RangeNode(start=[TokenMark("<"), TokenMark(">")]).resolve(self.view)
        self._assertRegionsEqual(self.Region(8, 16), region)
