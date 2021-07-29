#!/bin/python

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk



class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Survalyser")
        self.set_default_size(width=1280, height=720)
        self.connect("destroy", Gtk.main_quit)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                           halign=Gtk.Align.CENTER,
                           valign=Gtk.Align.CENTER)
        self.add(self.box)

        self.title_label = Gtk.Label(label="Survalser")
        self.box.add(self.title_label)

        self.resumebtn = Gtk.Button(label="Resume")
        self.box.add(self.resumebtn)

        self.savedbtn = Gtk.Button(label="Saved Datasets")
        self.box.add(self.savedbtn)

        self.loadbtn = Gtk.Button(label="Load Dataset")
        self.loadbtn.connect("clicked", self.on_loadbtn_clicked)
        self.box.add(self.loadbtn)


    def on_loadbtn_clicked(self, widget):
        file_action = Gtk.FileChooserAction.OPEN
        chooser = Gtk.FileChooserDialog(title="Open File")
        chooser.show()

def main():
    win = MainWindow()
    win.show_all()
    Gtk.main()

# def prn(x):
#     print("hello, world!")



# def main():
#     builder = Gtk.Builder()
#     try:
#         builder.add_from_file("survalyser.glade")
#     except:
#         print("file not found")
#         sys.exit()
#     main_window = builder.get_object("main")
#     main_window.show()
#     main_window.connect("destroy", Gtk.main_quit)
  
#     load_window = builder.get_object("load_window")
  
#     load = builder.get_object("load_button")
#     load.connect("clicked", load_data)
  
#     saved = builder.get_object("saved_button")
  
#     resume = builder.get_object("resume_button")
#     resume.connect("clicked", prn)

#     Gtk.main()



# # perform some kind of analysis
# def analyse():
#     pass






