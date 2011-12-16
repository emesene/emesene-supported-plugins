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

import songretriever
import DBusBase

class Mpris2Base(DBusBase.DBusBase):
    def __init__(self, main_window, iface_name, iface_path):
        DBusBase.DBusBase.__init__(self, main_window, iface_name, iface_path)
        self.dbuspropiface = None

    def reconnect(self):
        '''method to attemp a reconnection, via dbus, this is only
        called if the bus object is not initialized'''
        if DBusBase.DBusBase.reconnect(self):
            self.dbuspropiface = self.module.Interface(self.iface,dbus_interface='org.freedesktop.DBus.Properties')
            return True

        return False

    def is_playing(self):
        '''Returns True if a song is being played'''
        if self.is_running():
            status = self.dbuspropiface.Get("org.mpris.MediaPlayer2.Player","PlaybackStatus")
            return status == "Playing"

        return False

    def get_current_song(self):
        '''Returns the current song in the correct format'''
        if self.is_playing():
            metadata_dict=self.dbuspropiface.Get("org.mpris.MediaPlayer2.Player","Metadata")
            return songretriever.Song(metadata_dict.get(self.module.String(u'xesam:artist'))[0], 
                                      metadata_dict.get(self.module.String(u'xesam:album')),
                                      metadata_dict.get(self.module.String(u'xesam:title')))

class PraghaHandler(Mpris2Base):
    '''Handler for Pragha'''
    NAME = 'Pragha'
    DESCRIPTION = 'Music handler for Pragha'
    AUTHOR = 'Mariano Guerra'
    WEBSITE = 'www.emesene.org'

    def __init__(self, main_window=None,
                 iface_name = 'org.mpris.MediaPlayer2.pragha',
                 iface_path = '/org/mpris/MediaPlayer2'):
        Mpris2Base.__init__(self, main_window, iface_name, iface_path)

class RhythmboxHandler(Mpris2Base):
    '''Handler for Rhythmbox 3'''
    NAME = 'Rhythmbox 3'
    DESCRIPTION = 'Music handler for Rhythmbox 3'
    AUTHOR = 'Mariano Guerra'
    WEBSITE = 'www.emesene.org'

    def __init__(self, main_window=None,
                 iface_name = 'org.mpris.MediaPlayer2.rhythmbox',
                 iface_path = '/org/mpris/MediaPlayer2'):
        Mpris2Base.__init__(self, main_window, iface_name, iface_path)

