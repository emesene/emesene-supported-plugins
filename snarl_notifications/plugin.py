# -*- coding: utf-8 -*-

# This file is part of emesene.
#
# emesene is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# emesene is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with emesene; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

import extension
from plugin_base import PluginBase

import SnarlNotification 

class Plugin(PluginBase):
    _description = "Plugin for Snarl notifications"
    _authors = {"Shawn McTear": "syst3mfailur3@gmail.com"}

    def __init__(self):
        """Initialize plugin"""
        PluginBase.__init__(self)
        self.sn = SnarlNotification.sn

    def start(self, session):
        """Start plugin"""
        self.session = session
        self.sn.register('application/x-emesene2', 'emesene2')
        
    def stop(self):
        """Stop plugin"""
        self.sn.unregister('application/x-emesene2')

    def config(self, session):
        """Configurations for plugin"""
        pass

    def extension_register(self):
        """Register extention"""
        extension.register('notificationGUI', SnarlNotification.SnarlNotification)
