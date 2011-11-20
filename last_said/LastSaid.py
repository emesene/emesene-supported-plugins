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

'''module to define the last_said class, used by plugin.py'''
import e3
import gui
import datetime

class LastSaid():
    """Show last messages sent or received from a contact."""
    NAME = 'Last Said'
    DESCRIPTION = 'Show last messages sent or received from a contact.'
    AUTHOR = 'Jose Rostagno'
    WEBSITE = 'www.emesene.org'

    def __init__(self, session):
        '''init extension'''
        self.session = session
        self.conversation = None
        self.limit = self.session.config.get_or_set('i_last_said_messages', 5)

    def run(self, conversation):
        conversation.output.lock ()
        self.conversation = conversation
        if not (conversation.members[0] is None or conversation.is_group_chat):
            dest = self.session.contacts.me.account
            src = conversation.members[0]
            self.session.logger.get_chats(src, dest, self.limit, self._on_chats_ready)
        else:
            self.conversation.conv_status.clear()
            self.conversation.output.unlock ()

    def _on_chats_ready(self, results):
        '''called when the chat history is ready'''
        if not results:
            self.conversation.conv_status.clear()
            self.conversation.output.unlock ()
            return

        for stat, timestamp, msg_text, nick, account in results:
            is_me = self.session.contacts.me.account == account
            if is_me:
                contact = self.session.contacts.me
            else:
                contact = self.session.contacts.get(account)

            if contact == None:
                contact = e3.Contact(account, nick=nick)

            datetimestamp = datetime.datetime.utcfromtimestamp(timestamp)
            message = e3.Message(e3.Message.TYPE_OLDMSG, msg_text,
                        account, timestamp=datetimestamp)
            message.style = self.conversation.cstyle

            if is_me:
                self.conversation.output_message(message, None)
            else:
                self.conversation.input_message(message, contact, None, None)

        self.conversation.conv_status.clear()
        self.conversation.output.unlock ()

