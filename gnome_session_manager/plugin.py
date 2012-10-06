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

from plugin_base import PluginBase

import GnomeSessionIntegration

class Plugin(PluginBase):

    def __init__(self):
        PluginBase.__init__(self)
        self.integration = None

    def stop(self):
        '''stop the plugin'''
        self.integration = None

        return True

    def start(self, session):
        '''start the plugin'''
        self.integration = GnomeSessionIntegration.GnomeSessionIntegration(session)
        return True

    def config(self, session):
        '''config the plugin'''
        return True
