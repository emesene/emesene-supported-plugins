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


import os
import ctypes
user = ctypes.windll.user32

import songretriever

class WindowsPlayerHandler( songretriever.BaseMusicHandler ):
    '''This is the base for most Windows players'''
    '''It takes the title of the window as shown by windows's window manager and strip
        the title from there, too hacky, but the only way for most players'''
    NAME = 'WindowsHandler'
    DESCRIPTION = 'Handler for basic windows music player (NOT! Windows Media Player)'
    AUTHOR = 'Ariel Juodziukynas'
    WEBSITE = 'www.emesene.org'
    def __init__(self, main_window = None):
        songretriever.BaseMusicHandler.__init__( self, main_window )
        self.window = None
        self.windowClass = None
        self.currentSong = None
        self.isRunning()
        self.shellUser = user

    def splitStr(self, string):
        '''Split the title, remove the unneeded part of the string and leave only the song'''
        raise NotImplementedError("Not implemented")

    def isPlaying( self ):
        '''Some windows accept commands, other only change it's title, implement that
            according to the player'''
        raise NotImplementedError("Not implemented")

    def getWindowTitle( self ):
        '''Returns the title of the window'''
        if self.window is not None:
            st = ctypes.create_unicode_buffer(100)
            user.GetWindowTextW(self.window, st, 100)
            return st.value
        else:
            return ""

    def isRunning( self ):
        '''Check for a window with the specified title'''
        try:
            winampClassName = ctypes.c_wchar_p(self.windowClass)
            self.window = user.FindWindowW(winampClassName, None)
            return self.window != 0
        except: 
            return False

    def get_current_song(self):
        '''returns the current song or None if no song is playing'''
        if not self.isRunning(): 
            self.currentSong = None
            return self.currentSong
        if self.isPlaying():
            st = ctypes.create_unicode_buffer(100)
            user.GetWindowTextW(self.window, st, 100)
            newCurrentSong = self.splitStr(st.value)
        else:
            newCurrentSong = None

        if self.currentSong != newCurrentSong:
            self.currentSong = newCurrentSong
            return self.currentSong
            
        return self.currentSong
