import sys
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
windows = QtWidgets.QWidget()

windows.resize(500,500)
windows.move(100,100)
windows.show()
sys.exit(app.exec_())

# class Spreadsheet(Gtk.Grid):
#     def __init__(self, dataframe):
#         # sizing the grid
#         for col in dataframe.columns:
#             self.insert_column()
#         for row in dataframe.index:
#             self.insert_row()
#         self.insert_row()



# class MainWindow(Gtk.Window):
#     def __init__(self):
#         super().__init__()
#         self.set_title("Survalyser")
#         self.set_default_size(width=1280, height=720)
#         self.connect("destroy", Gtk.main_quit)

#         self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
#                            halign=Gtk.Align.CENTER,
#                            valign=Gtk.Align.CENTER)
#         self.add(self.box)

#         self.title_label = Gtk.Label(label="Survalser")
#         self.box.add(self.title_label)

#         self.resumebtn = Gtk.Button(label="Resume")
#         self.box.add(self.resumebtn)

#         self.savedbtn = Gtk.Button(label="Saved Datasets")
#         self.box.add(self.savedbtn)

#         self.loadbtn = Gtk.Button(label="Load Dataset")
#         self.loadbtn.connect("clicked", self.on_loadbtn_clicked)
#         self.box.add(self.loadbtn)

#     def on_destroy():
#         Gtk.main_quit()

#     def on_resume_clicked(self, button):
#         # get most recent data
#         get_dataframe("most_recent_file")

#         # now, 

#     def on_saved_clicked(self, button):
#         pass

#     def on_load_clicked(self, button):
#         file_action = Gtk.FileChooserAction.OPEN
#         chooser = Gtk.FileChooserDialog(title="Open File")
#         chooser.show()

# def main():
#     win = MainWindow()
#     win.show_all()
#     Gtk.main()




