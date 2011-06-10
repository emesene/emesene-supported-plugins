import gtk

class HelloWorldWidget(gtk.Label):
    """a label to display 'Hello World' below the user panel"""
    NAME = 'HelloWorld Label'
    DESCRIPTION = 'plugin how to'
    AUTHOR = 'Ariel Juodziukynas'
    WEBSITE = 'www.arieljuod.com.ar'

    #you can use something like grep to see where is this extension instantiated and check the parameters 
    def __init__(self, main_window):
        gtk.Label.__init__(self)
        self.set_text("Hello World")