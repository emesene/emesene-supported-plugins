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

# code from http://www.narf.ssji.net/~shtrom/wiki/projets/gnomescreensavernosession

import time
import os
import ctypes

class XScreenSaverInfo(ctypes.Structure):
  """ typedef struct { ... } XScreenSaverInfo; """
  _fields_ = [('window',      ctypes.c_ulong), # screen saver window
    ('state',       ctypes.c_int),   # off,on,disabled
    ('kind',        ctypes.c_int),   # blanked,internal,external
    ('since',       ctypes.c_ulong), # milliseconds
    ('idle',        ctypes.c_ulong), # milliseconds
    ('event_mask',  ctypes.c_ulong)] # events

class XIdleTimer(object):
    def __init__(self):
        self.xlib       = ctypes.cdll.LoadLibrary('libX11.so')
        self.dpy        = self.xlib.XOpenDisplay(os.environ['DISPLAY'])
        self.root       = self.xlib.XDefaultRootWindow(self.dpy)
        self.xss        = ctypes.cdll.LoadLibrary('libXss.so')
        self.xss.XScreenSaverAllocInfo.restype \
                = ctypes.POINTER(XScreenSaverInfo)

    def get_idle_duration(self):
        xss_info = self.xss.XScreenSaverAllocInfo()
        self.xss.XScreenSaverQueryInfo(self.dpy, self.root, xss_info)
        idle = xss_info.contents.idle/1000
        return idle
