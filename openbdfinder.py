import json
import gi
import pprint
import urllib.request
import urllib3
import ssl

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

# PEP 476 -- Enabling certificate verification by default for stdlib http clients
ssl._create_default_https_context = ssl._create_unverified_context


class OpenBDFinder(Gtk.Window):
    url_openbd = 'https://api.openbd.jp/v1/get?isbn='

    def __init__(self):
        Gtk.Window.__init__(self, title="OpenBD Finder")
        self.set_border_width(5)
        self.set_default_size(600, 700)

        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        self.add(grid)

        lab00 = Gtk.Label(label="ISBN13")
        lab00.set_xalign(1.0)
        ent10 = Gtk.Entry()
        ent10.set_hexpand(True)
        ent10.set_text('9784047914742')
        but20 = Gtk.Button(label="書籍情報取得")
        but20.connect("clicked", self.on_button_clicked, ent10)

        lab01 = Gtk.Label(label="書影")
        lab01.set_xalign(1.0)
        self.img11 = Gtk.Image()
        self.img11.set_halign(Gtk.Align.START)
        lab02 = Gtk.Label(label="書籍名")
        lab02.set_xalign(1.0)
        self.ent12 = Gtk.Entry()
        self.ent12.set_hexpand(True)

        lab03 = Gtk.Label(label="出版社")
        lab03.set_xalign(1.0)
        self.ent13 = Gtk.Entry()
        self.ent13.set_hexpand(True)

        lab04 = Gtk.Label(label="巻")
        lab04.set_xalign(1.0)
        self.ent14 = Gtk.Entry()
        self.ent14.set_hexpand(True)

        lab05 = Gtk.Label(label="シリーズ")
        lab05.set_xalign(1.0)
        self.ent15 = Gtk.Entry()
        self.ent15.set_hexpand(True)

        lab06 = Gtk.Label(label="著者")
        lab06.set_xalign(1.0)
        self.ent16 = Gtk.Entry()
        self.ent16.set_hexpand(True)

        lab07 = Gtk.Label(label="出版日")
        lab07.set_xalign(1.0)
        self.ent17 = Gtk.Entry()
        self.ent17.set_hexpand(True)

        lab08 = Gtk.Label(label="サムネールURI")
        lab08.set_xalign(1.0)
        self.ent18 = Gtk.Entry()
        self.ent18.set_hexpand(True)

        lab09 = Gtk.Label(label="詳細")
        lab09.set_xalign(1.0)
        scr19 = Gtk.ScrolledWindow()
        self.dscrpt = Gtk.TextView()
        self.dscrpt.set_wrap_mode(wrap_mode=Gtk.WrapMode.WORD)
        scr19.add(self.dscrpt)
        scr19.set_hexpand(True)
        scr19.set_vexpand(True)

        grid.attach(lab00, 0, 0, 1, 1)
        grid.attach(ent10, 1, 0, 1, 1)
        grid.attach(but20, 2, 0, 1, 1)

        grid.attach(lab01, 0, 1, 1, 1)
        grid.attach(self.img11, 1, 1, 2, 1)

        grid.attach(lab02, 0, 2, 1, 1)
        grid.attach(self.ent12, 1, 2, 2, 1)

        grid.attach(lab03, 0, 3, 1, 1)
        grid.attach(self.ent13, 1, 3, 2, 1)

        grid.attach(lab04, 0, 4, 1, 1)
        grid.attach(self.ent14, 1, 4, 2, 1)

        grid.attach(lab05, 0, 5, 1, 1)
        grid.attach(self.ent15, 1, 5, 2, 1)

        grid.attach(lab06, 0, 6, 1, 1)
        grid.attach(self.ent16, 1, 6, 2, 1)

        grid.attach(lab07, 0, 7, 1, 1)
        grid.attach(self.ent17, 1, 7, 2, 1)

        grid.attach(lab08, 0, 8, 1, 1)
        grid.attach(self.ent18, 1, 8, 2, 1)

        grid.attach(lab09, 0, 9, 1, 1)
        grid.attach(scr19, 1, 9, 2, 1)

    def on_button_clicked(self, button, entry):
        isbn = entry.get_text().strip()
        query = self.url_openbd + isbn
        with urllib.request.urlopen(query) as response:
            html = (response.read())
            jason_data = json.loads(html)

        self.ent12.set_text(jason_data[0]['summary']['title'])
        self.ent13.set_text(jason_data[0]['summary']['publisher'])
        self.ent14.set_text(jason_data[0]['summary']['volume'])
        self.ent15.set_text(jason_data[0]['summary']['series'])
        self.ent16.set_text(jason_data[0]['summary']['author'])
        self.ent17.set_text(jason_data[0]['summary']['pubdate'])
        self.ent18.set_text(jason_data[0]['summary']['cover'])

        msg = Gtk.TextBuffer()
        msg.set_text(jason_data[0]['onix']['CollateralDetail']['TextContent'][0]['Text'])
        self.dscrpt.set_buffer(msg)

        uri = jason_data[0]['summary']['cover']
        r = urllib.request.urlopen(uri)
        loader = GdkPixbuf.PixbufLoader()
        loader.write(r.read())
        loader.close()
        img = loader.get_pixbuf()
        self.img11.set_from_pixbuf(img)


win = OpenBDFinder()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
