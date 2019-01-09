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

from sublime import Region

from NeoVintageous.nv.jumplist import jumplist_update
from NeoVintageous.nv.vi.utils import next_non_blank
from NeoVintageous.nv.vi.utils import regions_transformer
from NeoVintageous.nv.vim import INTERNAL_NORMAL
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.vim import VISUAL_LINE


def goto_line(view, line, mode):
    line = line if line > 0 else 1
    dest = view.text_point(line - 1, 0)

    def f(view, s):
        if mode == NORMAL:
            return Region(next_non_blank(view, dest))
        elif mode == INTERNAL_NORMAL:
            start_line = view.full_line(s.a)
            dest_line = view.full_line(dest)
            if start_line.a == dest_line.a:
                return dest_line
            elif start_line.a < dest_line.a:
                return Region(start_line.a, dest_line.b)
            else:
                return Region(start_line.b, dest_line.a)
        elif mode == VISUAL:
            dest_non_blank = next_non_blank(view, dest)
            if dest_non_blank < s.a and s.a < s.b:
                return Region(s.a + 1, dest_non_blank)
            elif dest_non_blank < s.a:
                return Region(s.a, dest_non_blank)
            elif dest_non_blank > s.b and s.a > s.b:
                return Region(s.a - 1, dest_non_blank + 1)
            return Region(s.a, dest_non_blank + 1)
        elif mode == VISUAL_LINE:
            if dest < s.a and s.a < s.b:
                return Region(view.full_line(s.a).b, dest)
            elif dest < s.a:
                return Region(s.a, dest)
            elif dest >= s.a and s.a > s.b:
                return Region(view.full_line(s.a - 1).a, view.full_line(dest).b)
            return Region(s.a, view.full_line(dest).b)
        return s

    jumplist_update(view)
    regions_transformer(view, f)
    jumplist_update(view)

    # FIXME: Bringing the selections into view will be undesirable in many cases. Maybe we
    # should have an optional .scroll_selections_into_view() step during command execution.
    view.show(view.sel()[0])
