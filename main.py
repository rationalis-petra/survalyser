#!/bin/python

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk



def prn(x):
    print("hello, world!")


def load_data(x):
    builder = Gtk.Builder()
    builder.add_from_file("filedialog.glade")
    load_window = builder.get_object("main")
    load_window.present()

    #load_window.connect("destroy", lambda x : load_window.)
        


def main():
    builder = Gtk.Builder()
    try:
        builder.add_from_file("survalyser.glade")
    except:
        print("file not found")
        sys.exit()
    main_window = builder.get_object("main")
    main_window.show()
    main_window.connect("destroy", Gtk.main_quit)
  
    load_window = builder.get_object("load_window")
  
    load = builder.get_object("load_button")
    load.connect("clicked", load_data)
  
    saved = builder.get_object("saved_button")
  
    resume = builder.get_object("resume_button")
    resume.connect("clicked", prn)



    Gtk.main()



# perform some kind of analysis
def analyse():
    pass






