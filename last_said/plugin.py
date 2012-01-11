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
from plugin_base import PluginBase

import e3
import gui
import datetime
import Preferences
import Queue

class Plugin(PluginBase):
    _description = 'Show last messages sent or received from a contact'
    _authors = { 'Jose Rostagno' : 'pepeleproso gmail com' }

    def __init__(self):
        PluginBase.__init__(self)

    def start(self, session):
        self.session = session
        self.conversations = Queue.Queue()
        self.limit = self.session.config.get_or_set('i_last_said_messages', 5)
        self.session.conversation_start_locked = True
        self.session.signals.conv_started.subscribe(
            self._on_started_message)
        return True

    def stop(self):
        #disconect signals
        self.session.signals.conv_started.unsubscribe(
            self._on_started_message)
        self.session.conversation_start_locked = False
        self.session = None
        self.conversations = Queue.Queue()
        return False

    def config(self, session):
        '''config the plugin'''
        Preferences.Preferences(session)

    def configurable(self):
        '''this plugin is configurable'''
        return True

    def _on_started_message(self, cid, members):
        conversation = self.session.get_conversation(cid)
        self.conversations.put(conversation)
        if not (conversation.members[0] is None or conversation.is_group_chat):
            dest = self.session.contacts.me.account
            src = conversation.members[0]
            self.session.logger.get_chats(src, dest, self.limit, self._on_chats_ready)
        else:
            conversation.conv_status.clear()
            conversation.output.unlock ()

    def _on_chats_ready(self, results):
        '''called when the chat history is ready'''
        conversation = self.conversations.get(False)
        conversation.conv_status.clear()

        if not results:
            conversation.output.unlock ()
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
            message.style = conversation.cstyle

            if is_me:
                conversation.output_message(message, None)
            else:
                conversation.input_message(message, contact, None, None)

        conversation.conv_status.clear()
        conversation.output.unlock ()
