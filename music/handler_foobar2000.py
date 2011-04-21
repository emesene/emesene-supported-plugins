# -*- coding: utf-8 -*-

#   This file is part of emesene.
#
#    Emesene is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
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

import base_windows_handler

import os
from ctypes import *
from ctypes.wintypes import *
user = windll.user32

_window = None

WNDENUMPROC=WINFUNCTYPE(BOOL, HWND, LPARAM)

@WNDENUMPROC
def EnumWindowsCallbackFunc(hwnd,lParam):
    global _window
    st = create_unicode_buffer(100)
    user.GetClassNameW(hwnd,st,100)
    user.GetWindowTextW(hwnd,st,100)
    if st.value.find("foobar2000") != -1:
        _window = hwnd
    return True #Allow windows to keep enumerating

class Foobar2000Handler( base_windows_handler.WindowsPlayerHandler ):
    NAME = 'Foobar2000'
    DESCRIPTION = 'Handler for Foobar2000'
    AUTHOR = 'Ariel Juodziukynas'
    WEBSITE = 'www.emesene.org'
    def __init__(self, main_window = None):
        base_windows_handler.WindowsPlayerHandler.__init__( self, main_window )
        self.windowClass = "foobar2000"
        self.isRunning()

    def splitStr(self, string):
        index = string.rfind("foobar2000")
        # stadard ui adds "  [foobar2000 v1.0.3]" at the end
        # columns ui adds " - foobar2000" at the end, that's the -3 for
        return string[:index-3]
        
    def isPlaying( self ):
        title = self.getWindowTitle()
        return not title.startswith("foobar2000")

    def isRunning( self ):
        global _window
        user.EnumWindows(EnumWindowsCallbackFunc,0)
        if _window is not None:
            self.window = _window
            return True
        else:
            return False
