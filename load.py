

# load data from file for processing 
def open_response(dialog, response):
    if response == Gtk.ResponseType.ACCEPT:
        file = dialog.get_file()
        print(file)
    dialog.close()
  

def load_data(x):
    file_action = Gtk.FileChooserAction.OPEN
    chooser = Gtk.FileChooserDialog(title="Open File",
                                    
                                    action=file_action)
    chooser.connect("response", open_response)
    chooser.show()
    #load_window.connect("destroy", lambda x : load_window.)
        
