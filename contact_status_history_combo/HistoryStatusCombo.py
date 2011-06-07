'''module to define the HistoryStatusCombo class, used by plugin.py'''
import gtk
import gobject

import e3
import gui
from gui.gtkui import utils
from gui.gtkui import Renderers
from time import *

class HistoryStatusCombo(gtk.ComboBox):
    """a widget to show a list with the history of online/offline events of every contact with a timestamp."""
    NAME = 'Contact History Status Combo'
    DESCRIPTION = 'Show a list with the history of online/offline events of every contact with a timestamp.'
    AUTHOR = 'Jose Rostagno'
    WEBSITE = 'www.emesene.org'

    def __init__(self, main_window):
        """constructor"""
        self.model = gtk.ListStore(gobject.TYPE_STRING, gtk.gdk.Pixbuf, \
                      gobject.TYPE_INT, gobject.TYPE_STRING)

        gtk.ComboBox.__init__(self, self.model)
        self.main_window = main_window
        self.status = None

        status_timespan_cell = gtk.CellRendererText()
        status_pixbuf_cell = gtk.CellRendererPixbuf()
        status_text_cell = gtk.CellRendererText()
        self.pack_start(status_timespan_cell, False)
        self.pack_start(status_pixbuf_cell, False)
        self.pack_start(status_text_cell, False)
        status_pixbuf_cell.set_property('xalign', 0.0)
        status_pixbuf_cell.set_property('xpad', 5)
        status_text_cell.set_property('xalign', 0.0)
        status_text_cell.set_property('xpad', 5)
        status_text_cell.set_property('width', 158)
        self.add_attribute(status_timespan_cell, 'text', 0)
        self.add_attribute(status_pixbuf_cell, 'pixbuf', 1)
        self.add_attribute(status_text_cell, 'text', 3)
        self.set_resize_mode(0)
        self.set_wrap_width(1)
        self.set_active(0)

        main_window.session.signals.contact_attr_changed.subscribe(
                self._on_contact_change_something)

    def _on_contact_change_something(self, *args):
        """
        update the menu when contacts change something
        """
        if len(args) == 3:
            account, type_change, value_change = args
        elif len(args) == 4:
            account, type_change, value_change, do_notify = args

        if type_change == 'status':
            contact =  self.main_window.session.contacts.get(account)
            if not contact:
                return
            time = strftime('[%H:%M:%S]', localtime())
            stat = e3.status.STATUS[contact.status]
            pixbuf = utils.safe_gtk_pixbuf_load(gui.theme.get_image_theme().status_icons[contact.status])
            pixbuf.scale_simple(20, 20, gtk.gdk.INTERP_BILINEAR)
            display_name = Renderers.msnplus_to_plain_text(contact.display_name)
            self.model.prepend([time, pixbuf, contact.status, display_name])
            self.set_active(0)

    def on_stop():
        main_window.session.signals.contact_attr_changed.unsubscribe(
                self._on_contact_change_something)

