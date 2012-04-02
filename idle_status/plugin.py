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
import glib
import os

from plugin_base import PluginBase

if os.name == "nt":
    import WindowsTimer

try:
    from XlibTimer import XlibTimer as LinuxTimer
except Exception, e:
    from xidletimer import XIdleTimer as LinuxTimer

import Preferences

# I don't know if mac uses Xlib or something, I've found some reference to
# "HIDIdleTime" system property but I have no way to implement/test it

class Plugin(PluginBase):
    _description = 'Change status to idle after 5 minutes of inactivity'
    _authors = { 'arielj' : 'arieljuod gmail com' }
    def __init__(self):
        PluginBase.__init__(self)

    def start(self, session):
        '''start the plugin'''
        self.session = session
        self.session.config.get_or_set('i_idle_status_duration', 5*60) #5 mins
        #TODO: Find a way to be independant of gobject
        self.timeout_id = glib.timeout_add_seconds(4, self.idle_state)
        self.is_idle = self.session.contacts.me.status == e3.status.IDLE
        self.timer = None

    def stop(self):
        glib.source_remove(self.timeout_id)

    def config(self, session):
        '''config the plugin'''
        Preferences.Preferences(self.session)

    def configurable(self):
        '''this plugin is configurable'''
        return True

    #check if user was idle enough time to change status
    def idle_state(self):
        #compare idle time with user's preferences
        self.timer = extension.get_and_instantiate('idle timer')
        idle_time = self.timer.get_idle_duration()
        if idle_time >= self.session.config.i_idle_status_duration:
            #if idle enough time and ONLINE, set idle status
            if self.session.contacts.me.status == e3.status.ONLINE:
                self.session.set_status(e3.status.IDLE)
                self.is_idle=True
        elif idle_time < self.session.config.i_idle_status_duration and self.is_idle:
            #if status is idle but the user moved something, set online
            self.session.set_status(e3.status.ONLINE)
            self.is_idle=False
        return True

    def category_register(self):
        if os.name == "nt":
            extension.category_register('idle timer', WindowsTimer.WindowsTimer,
                None, True)
        else:
            extension.category_register('idle timer', LinuxTimer,
                None, True)
        #TODO: add some mac method too
