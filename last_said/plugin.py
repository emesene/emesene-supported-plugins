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

import extension
from plugin_base import PluginBase

import LastSaid

import Preferences

class Plugin(PluginBase):
    _description = 'Show last messages sent or received from a contact'
    _authors = { 'Jose Rostagno' : 'pepeleproso gmail com' }

    def __init__(self):
        PluginBase.__init__(self)

    def start(self, session):
        self.extensions_register()
        return True

    def stop(self):
        #disconect signals
        return False

    def config(self, session):
        '''config the plugin'''
        Preferences.Preferences(session)

    def configurable(self):
        '''this plugin is configurable'''
        return True

    def extensions_register(self):
        extension.register('after_new_conversation', LastSaid.LastSaid)
