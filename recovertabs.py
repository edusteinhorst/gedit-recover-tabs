import os
from gi.repository import GObject, GLib, Gtk, Gio, Gedit

SETTINGS_SCHEMA = "org.gnome.gedit.plugins.recovertabs"

class RecoverTabsWindowActivatable(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "RecoverTabsWindowActivatable"
    window = GObject.property(type=Gedit.Window)
    removeUntitled = False

    def __init__(self):
        GObject.Object.__init__(self)
        self._handlers = []
    
    def do_activate(self):
        """
        Connect signal handlers.
        """
        handlers = []        
        self._handlers.append(self.window.connect("active-tab-state-changed", self.on_tab_state_change))
        self._handlers.append(self.window.connect("tab-added", self.on_tab_added))
        self._handlers.append(self.window.connect("tab-removed", self.on_tab_removed))        
        
        # temporary handler to catch the first time a window is shown
        self._temp_handler = self.window.connect("show", self.on_window_show)  

    def do_deactivate(self):     
        """
        Disconect any signal handlers that were added in do_activate().
        """
        [self.window.disconnect(handler_id) for handler_id in self._handlers]
    
    def do_update_state(self):
        pass
        
    def is_first_window(self):
        """
        Return True if the window being added is the first window instance.
        """
        app = Gedit.App.get_default()
        if len(app.get_windows()) <= 1:
            return True
        else:
            return False

    def on_tab_state_change(self, window):
    	self.store_tabs_open()
    	return False
    
    def on_tab_added(self, window, tab):
    	if self.removeUntitled:
    	    if tab and tab.get_document().is_untitled(): 
                # This didn't work, causing seg fault for some reason :/
                # self.window.close_tab(tab)
                self.removeUntitled = False
                return False
    	self.store_tabs_open()
    	return False
    	
    def on_tab_removed(self, tab, window):
        self.store_tabs_open()
        return False
    
    def store_tabs_open(self):
        uris = []
        win = 1
        for window in Gedit.App.get_default().get_windows():
            for document in window.get_documents():
                gfile = document.get_file().get_location()
                if gfile:
                    uris.append(str(win) + " " + gfile.get_uri())
            win = win + 1
        settings = Gio.Settings.new(SETTINGS_SCHEMA)
        settings.set_value('uris', GLib.Variant("as", uris))
    
    def open_previous_windows(self):
        settings = Gio.Settings.new(SETTINGS_SCHEMA)
        uris = settings.get_value('uris')
        if uris:
            prevWin = uris[0].split()[0]
            winRef = self.window
            for uri in uris:
                win = uri.split()[0]
                location = Gio.file_new_for_uri(uri.split()[1])
                if win != prevWin:
                    prevWin = win
                    winRef = Gedit.App.get_default().create_window()
                winRef.create_tab_from_location(location, None, 0, 0, False, True)   
            self.removeUntitled = True  

    def on_window_show(self, window, data=None):
        """
        Only restore tabs if this window is the first Gedit window instance.
        """
        if self.is_first_window():
            self.open_previous_windows()
            self.window.disconnect(self._temp_handler)
