from gui.gtkui.Preferences import BaseTable


class DownloadExtension(BaseTable):
    """the panel to download extensions
    """

    def __init__(self, session):
        """constructor
        """
        BaseTable.__init__(self, 4, 1)
        self.set_border_width(5)
        self.session = session
        self.append_markup('<b>Download plugin</b>')
        self.show_all()
