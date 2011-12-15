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
'''module to define the TypingNotification class, used by plugin.py'''

import gtk
import gobject

import e3
import gui
from gui.base import Plus
import glib

class TypingNotification(gtk.Label):
    """Show a text notification when contact is typing, like old emesene 1.x."""
    NAME = 'Typing Notification'
    DESCRIPTION = 'Show a text notification when contact is typing, like old emesene 1.x'
    AUTHOR = 'Jose Rostagno'
    WEBSITE = 'www.emesene.org'

    def __init__(self, conversation, session):
        """constructor"""
        ##creo el label
        gtk.Label.__init__(self)
        self.conversation = conversation
        self.session = session
        self.active = False
        self.session.signals.user_typing.subscribe(
            self.on_user_typing)
        self.set_alignment(0.0, 0.5)
        self.show()

    def on_user_typing(self, cid, account, *args):
        """
        inform that the other user has started typing
        """
        if account in self.conversation.members:
            contact = self.session.contacts.get(account)
            if contact and not self.active:
                self.active = True #avoid many timeout
                display_name = Plus.msnplus_strip(contact.display_name)
                self.set_markup(_("%s is typing") % display_name)
                glib.timeout_add_seconds(3, self.update_label)

    def update_label(self):
        '''restart label'''
        self.active = False
        self.set_markup("")

