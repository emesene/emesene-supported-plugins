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
import gui

class Preferences(object):
    '''the preference basic window of the 'listening to' extension'''

    def __init__(self, session):
        '''constructor that uses the default dialog class to make the window'''

        self.session = session
        dialog = extension.get_default('dialog')
        entry_window = dialog.entry_window(
                        'Minutes until idle status',
                        str(self.session.config.i_idle_status_duration / 60),
                        self._on_accept,
                        'Idle status plug-in preferences')
        entry_window.show()

    def _on_accept(self, response, value):
        '''callback when accept is clicked'''
        if response == gui.stock.ACCEPT:
            self.session.config.i_idle_status_duration = int(value) * 60
