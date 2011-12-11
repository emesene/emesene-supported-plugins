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
                self.active = True
                self.set_markup(_("%s is typing") % contact.display_name)
                glib.timeout_add_seconds(3, self.update_label)

    def update_label(self):
        '''restart label'''
        self.active = False
        self.set_markup("")

