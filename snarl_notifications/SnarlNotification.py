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

import pysnp
from gui.base import Plus
import logging
sn = pysnp.PySNP()
log = logging.getLogger('plugins.snarl_notifications.SnarlNotification')

NAME = 'Snarl Notifications'
DESCRIPTION = 'A plugin that uses Snarl to display notifications'
AUTHOR = 'Shawn McTear'
WEBSITE = 'n/a'
VERSION = '0.2'

def SnarlNotification(title, text, picture_path=None, const=None,
                      callback=None, tooltip=None):
    """emesene plugins - SnarlNotification"""
    title = Plus.msnplus_strip(title)
    if const == 'mail-received':
        app_uid = 'mail'
    elif const == 'file-transf-completed':
        app_uid = 'file'
    elif const == 'file-transf-canceled':
        app_uid = 'file'
    elif const == 'message-im':
        app_uid = title +'-message'

    if picture_path == 'notification-message-im':
        sn.notify('application/x-emesene2', title, text, uid=app_uid)
    else:
        picture_path = picture_path.replace( "file://", "" ).replace('\\', '/')
        sn.notify('application/x-emesene2', title, text, uid=app_uid,
                       icon=picture_path)
        
