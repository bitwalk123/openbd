import json
import gi
import urllib.request

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class OpenBD(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="OpenBD")
        self.set_default_size(0, 0)

        grid = Gtk.Grid()
        self.add(grid)

        lab00 = Gtk.Label(label="ISBN13")
        lab00.set_xalign(1.0)
        ent10 = Gtk.Entry()
        but20 = Gtk.Button(label="書籍情報取得")
        but20.connect("clicked", self.on_button_clicked)

        lab01 = Gtk.Label(label="書影")
        lab01.set_xalign(1.0)
        ent11 = Gtk.Entry()

        lab02 = Gtk.Label(label="書籍名")
        lab02.set_xalign(1.0)
        ent12 = Gtk.Entry()

        lab03 = Gtk.Label(label="出版社")
        lab03.set_xalign(1.0)
        ent13 = Gtk.Entry()

        lab04 = Gtk.Label(label="巻")
        lab04.set_xalign(1.0)
        ent14 = Gtk.Entry()

        lab05 = Gtk.Label(label="シリーズ")
        lab05.set_xalign(1.0)
        ent15 = Gtk.Entry()

        lab06 = Gtk.Label(label="著者")
        lab06.set_xalign(1.0)
        ent16 = Gtk.Entry()

        lab07 = Gtk.Label(label="出版日")
        lab07.set_xalign(1.0)
        ent17 = Gtk.Entry()

        lab08 = Gtk.Label(label="サムネールURI")
        lab08.set_xalign(1.0)
        ent18 = Gtk.Entry()

        lab09 = Gtk.Label(label="詳細")
        lab09.set_xalign(1.0)
        ent19 = Gtk.Entry()

        grid.attach(lab00, 0, 0, 1, 1)
        grid.attach(ent10, 1, 0, 1, 1)
        grid.attach(but20, 2, 0, 1, 1)

        grid.attach(lab01, 0, 1, 1, 1)
        grid.attach(ent11, 1, 1, 2, 1)

        grid.attach(lab02, 0, 2, 1, 1)
        grid.attach(ent12, 1, 2, 2, 1)

        grid.attach(lab03, 0, 3, 1, 1)
        grid.attach(ent13, 1, 3, 2, 1)

        grid.attach(lab04, 0, 4, 1, 1)
        grid.attach(ent14, 1, 4, 2, 1)

        grid.attach(lab05, 0, 5, 1, 1)
        grid.attach(ent15, 1, 5, 2, 1)

        grid.attach(lab06, 0, 6, 1, 1)
        grid.attach(ent16, 1, 6, 2, 1)

        grid.attach(lab07, 0, 7, 1, 1)
        grid.attach(ent17, 1, 7, 2, 1)

        grid.attach(lab08, 0, 8, 1, 1)
        grid.attach(ent18, 1, 8, 2, 1)

        grid.attach(lab09, 0, 9, 1, 1)
        grid.attach(ent19, 1, 9, 2, 1)

    def on_button_clicked(self, button):
        with urllib.request.urlopen('https://api.openbd.jp/v1/get?isbn=9784047914742') as response:
            html = (response.read()).decode('utf-8')
            #print(json.dumps(html))
            print(html)

win = OpenBD()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()