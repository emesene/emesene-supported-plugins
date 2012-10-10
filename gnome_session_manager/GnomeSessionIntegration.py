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

import e3

ROOT_NAME = 'org.freedesktop.DBus'
ROOT_PATH = '/org/freedesktop/DBus'

class GnomeSessionIntegration(object):

    def __init__(self, session):
        
        self.session = session
        self.iface_name = "org.gnome.SessionManager"
        self.iface_path = "/org/gnome/SessionManager/Presence"

        try:
            import dbus
            dbus_version = getattr(dbus, 'version', (0, 0, 0))
            from dbus.mainloop.glib import DBusGMainLoop
            DBusGMainLoop(set_as_default = True)
            dbus.SessionBus()
        except dbus.DBusException, error:
            print 'Unable to use D-Bus: %s' % str(error)

        # dbus session, this is set in reconnect.
        self.bus = None
        # dbus interface set in reconnect.
        self.iface = None
        self.module = dbus
        self.root = dbus.SessionBus().get_object(ROOT_NAME, ROOT_PATH)

        self.shellstats = {}
        self.shellstats[0] = e3.status.ONLINE
        self.shellstats[1] = e3.status.OFFLINE
        self.shellstats[2] = e3.status.BUSY
        self.shellstats[3] = e3.status.IDLE

        self.autocheck_bus()

    def autocheck_bus(self):
        '''monitor bus for connect/disconnect events'''
        session = self.module.SessionBus()
        def cb(conected):
            if conected: # may be empty
                self.start()
            else:
                self.stop()

        self.watch = session.watch_name_owner(self.iface_name, cb)

    def on_status_changed(self, status):
        '''set status according to gnome session status'''
        self.session.set_status(self.shellstats[status])

    def reconnect(self):
        '''method to attemp a reconnection, via dbus, this is only
        called if the bus object is not initialized'''
        self.bus = self.module.SessionBus()
        try:
            self.iface = self.bus.get_object(self.iface_name, self.iface_path)
            self.dbuspresiface = self.module.Interface(self.iface, 'org.gnome.SessionManager.Presence')
            self.dbuspresiface.connect_to_signal('StatusChanged', self.on_status_changed)
            return True
        except self.module.DBusException, error:
            self.iface = None
            print 'D-Bus error: %s' % str(error)
            return False

    def start(self):
        if self.is_name_active(self.iface_name):
            if self.iface is None:
                self.reconnect()
            return True
        else:
            self.stop()
            return False

    def stop(self):
        self.iface = None

    def is_name_active(self, name):
        '''return True if the name is active on dbus'''
        ''' You don't need to override this'''
        return bool(self.root.NameHasOwner(name))

