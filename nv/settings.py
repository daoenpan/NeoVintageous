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


def get_setting(view, name):
    return view.settings().get('vintageous_%s' % name)


def set_setting(view, name, value):
    view.settings().set('vintageous_%s' % name)


def reset_setting(view, name):
    view.settings().erase('vintageous_%s' % name)


# DEPRECATED Refactor and use get_setting() instead
def get_setting_neo(view, name):
    return view.settings().get('neovintageous_%s' % name)
