# Copyright (C) 2010 Elijah Rutschman <elijahr@gmail.com>, GPL v3

import gedit
import gtk
import os
import urllib
import subprocess
import os
import sys
      
class SudoReopenPlugin(gedit.Plugin):

    line_tools_str = """
        <ui>
            <menubar name="MenuBar">
                <menu name="FileMenu" action="File">
                    <placeholder name="FileOps_1">
	                    <menuitem action="SudoReopen"/>
                    </placeholder>
                </menu>
            </menubar>
        </ui>
        """
    bookmarks = {}
    
    def __init__(self):
        gedit.Plugin.__init__(self)
        
    def activate(self, window):
        actions = [
            ('SudoReopen', None, 'S_udo Reopen File', '<Alt><Control>o', 
             'Re-open current file as root.', 
             self.sudo_reopen_current_file),
        ]
        windowdata = dict()
        window.set_data("SudoReopenPluginWindowDataKey", windowdata)
        windowdata["action_group"] = gtk.ActionGroup(
            "GeditSudoReopenPluginActions")

        windowdata["action_group"].add_actions(actions, window)
        manager = window.get_ui_manager()
        manager.insert_action_group(windowdata["action_group"], -1)
        windowdata["ui_id"] = manager.add_ui_from_string(self.line_tools_str)
        window.set_data("SudoReopenPluginInfo", windowdata)
        
    def deactivate(self, window):
        windowdata = window.get_data("SudoReopenPluginWindowDataKey")
        manager = window.get_ui_manager()
        manager.remove_ui(windowdata["ui_id"])
        manager.remove_action_group(windowdata["action_group"])

    def update_ui(self, window):
        view = window.get_active_view()
        windowdata = window.get_data("SudoReopenPluginWindowDataKey")
        windowdata["action_group"].set_sensitive(bool(view and view.get_editable()))

    def sudo_reopen_current_file(self, action, window):
        document = window.get_active_document()
        document_uri = document.get_uri()
        if document_uri:
            cmd = ['gksudo', 'gedit', document_uri]
            print cmd
            subprocess.Popen(cmd)
        
#        dialog = gtk.FileChooserDialog("Rename current file as...", None,
#                gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
#                gtk.STOCK_SAVE, gtk.RESPONSE_OK))
#        dialog.set_uri(old_uri)

#        if dialog.run() == gtk.RESPONSE_OK:
#            new_uri = dialog.get_uri()
#            encoding = document.get_encoding()
#            document.save_as(new_uri, encoding, gedit.DOCUMENT_SAVE_PRESERVE_BACKUP)
#            # a lil hack to convert the uri to a path.  what if uri is not a fs path? 
#            # whats the better way?
#            if old_uri:
#                path = old_uri.replace('file://', '')
#                path = urllib.url2pathname(path)
#                os.remove(path)

#        dialog.destroy()

