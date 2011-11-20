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
    '''the preference basic window of the last_said plugin'''

    def __init__(self, session):
        '''constructor that uses the default dialog class to make the window'''

        self.session = session
        dialog = extension.get_default('dialog')
        entry_window = dialog.entry_window(
                        '# messages to show (1-15)',
                        str(self.session.config.get_or_set('i_last_said_messages', 5)),
                        self._on_accept,
                        'Last Said plug-in preferences')
        entry_window.show()

    def _on_accept(self, response, value):
        '''callback when accept is clicked'''
        if response == gui.stock.ACCEPT:
            #more than 15 messages can delay conversation window for a long time
            self.session.config.i_last_said_messages = self.restrict (int(value), 1, 15)

    def restrict (self, val, minval, maxval):
        '''clamp an integer to some range'''
        if val < minval: return minval
        if val > maxval: return maxval
        return val
