#!/usr/bin/env python

import pysnp
from gui.gtkui import Renderers
import logging
sn = pysnp.PySNP()
log = logging.getLogger('plugins.snarl_notifications.SnarlNotification')

NAME = 'Snarl Notifications'
DESCRIPTION = 'A plugin that uses Snarl to display notifications'
AUTHOR = 'Shawn McTear'
WEBSITE = 'n/a'
VERSION = '0.1'

def SnarlNotification(title, text, picture_path=None, const=None,
                      callback=None, tooltip=None):
    """emesene plugins - SnarlNotification"""
    title = Renderers.msnplus_to_plain_text(title)
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
        