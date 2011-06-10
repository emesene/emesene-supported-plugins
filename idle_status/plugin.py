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
import e3
import gobject
import os

from plugin_base import PluginBase

if os.name == "nt":
    import Windows

try:
    import Xlib
    HAS_XLIB = True
except Exception, e:
    HAS_XLIB = False
    
# I don't know if mac uses Xlib or something, I've found some reference to
# "HIDIdleTime" system property but I have no way to implement/test it

class Plugin(PluginBase):
    _description = _( 'Change status to idle after 5 minutes of inactivity.')
    _authors = { 'arielj' : 'arieljuod gmail com' }
    def __init__(self):
        PluginBase.__init__(self)

    def start(self, session):
        '''start the plugin'''
        #TODO: Add preferences
        self.idleAfter = 5*60 #5 minutes default
        self.session = session
        #TODO: Find a way to be independant of gobject
        self.timeout_id = gobject.timeout_add_seconds(4, self.idle_state)
        self.extensions_register()
        self.isIdle = self.session.contacts.me.status == e3.status.IDLE

    def stop(self):
        gobject.timeout_remove(self.timeout_id)

    def config(self):
        pass

    #check if user was idle enough time to change status
    def idle_state(self):
        #compare idle time with user's preferences
        timer = extension.get_and_instantiate('idle timer')
        idleTime = timer.get_idle_duration()
        if idleTime >= self.idleAfter:
            #if idle enough time and ONLINE, set idle status
            if self.session.contacts.me.status == e3.status.ONLINE:
                self.session.set_status(e3.status.IDLE)
                self.isIdle=True
        elif idleTime < self.idleAfter and self.isIdle:
            #if status is idle but the user moved something, set online
            self.session.set_status(e3.status.ONLINE)
            self.isIdle=False
        return True

    def extensions_register(self):
        if os.name == "nt":
            extension.category_register('idle timer', Windows.WindowsTimer)
        else: #TODO: add some unix extensions that works always
          if HAS_XLIB:
              extension.category_register('idle timer', Xlib.XlibTimer)
              #TODO: add some mac method too
