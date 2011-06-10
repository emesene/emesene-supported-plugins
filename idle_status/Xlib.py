# -*- coding: utf-8 -*-

#    This file is part of emesene.
#
#    emesene is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    emesene is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with emesene; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from Xlib import display

def XlibTimer(object):
    def __init__(self):
        self.display = Xlib.display.Display()
        self.screen = self.display.screen()
        self.last_x = -1
        self.last_y = -1

    def get_idle_duration(self):
        #check mouse movement
        x = self.screen.root.query_pointer()._data["root_x"]
        y = self.screen.root.query_pointer()._data["root_y"]
        if self.last_x == x and self.last_y == y:
            #if mouse didn't move, check pressed keys (not the best, but should work...)
            #it's really ugly, but I tryied with keypress/release events
            #and I can't/don't know how to make them work...
            keymap = self.display.query_keymap()
            for key in keymap:
                if not key == 0:
                    self.resetLastActivity(None,None)
        else:
            self.last_x = x
            self.last_y = y
            self.resetLastActivity(None,None)
        return time.time() - self.lastActivity
