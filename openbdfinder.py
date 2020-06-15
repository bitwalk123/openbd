import json
import gi
import urllib.request
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

        # ------
        #  GUI
        # ------
        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        self.add(grid)

        r = 0
        str_label1 = 'ISBN13'
        str_label2 = '書籍情報取得'
        lab00 = Gtk.Label(label=str_label1)
        lab00.set_xalign(1.0)
        ent10 = Gtk.Entry()
        ent10.set_hexpand(True)
        ent10.set_text('9784047914742')
        but20 = Gtk.Button(label=str_label2)
        but20.connect("clicked", self.on_button_clicked, ent10)

        grid.attach(lab00, 0, r, 1, 1)
        grid.attach(ent10, 1, r, 1, 1)
        grid.attach(but20, 2, r, 1, 1)

        r = 1
        str_label = '書影'
        lab01 = Gtk.Label(label=str_label)
        lab01.set_xalign(1.0)
        self.img11 = Gtk.Image()
        self.img11.set_halign(Gtk.Align.START)

        grid.attach(lab01, 0, r, 1, 1)
        grid.attach(self.img11, 1, r, 2, 1)

        r = 2
        str_label = '書籍名'
        self.ent12 = RowTypical(grid, r, str_label)

        r = 3
        str_label = '出版社'
        self.ent13 = RowTypical(grid, r, str_label)

        r = 4
        str_label = '巻'
        self.ent14 = RowTypical(grid, r, str_label)

        r = 5
        str_label = 'シリーズ'
        self.ent15 = RowTypical(grid, r, str_label)

        r = 6
        str_label = '著者'
        self.ent16 = RowTypical(grid, r, str_label)

        r = 7
        str_label = '出版日'
        self.ent17 = RowTypical(grid, r, str_label)

        r = 8
        str_label = 'サムネールURI'
        self.ent18 = RowTypical(grid, r, str_label)

        r = 9
        str_label = '詳細'
        lab09 = Gtk.Label(label=str_label)
        lab09.set_xalign(1.0)
        lab09.set_valign(Gtk.Align.START)
        scr19 = Gtk.ScrolledWindow()
        self.dscrpt = Gtk.TextView()
        self.dscrpt.set_editable(False)
        self.dscrpt.set_can_focus(False)
        self.dscrpt.set_wrap_mode(wrap_mode=Gtk.WrapMode.WORD)
        scr19.add(self.dscrpt)
        scr19.set_hexpand(True)
        scr19.set_vexpand(True)

        grid.attach(lab09, 0, r, 1, 1)
        grid.attach(scr19, 1, r, 2, 1)

    # -------------------------------------------------------------------------
    #  on_button_clicked
    #  click event for ISBN serach
    #
    #  arguments
    #    button : instance of clicked button
    #    entry  : instance of entry with ISBN number
    # -------------------------------------------------------------------------
    def on_button_clicked(self, button, entry):
        isbn = entry.get_text().strip()
        query = self.url_openbd + isbn
        with urllib.request.urlopen(query) as response:
            html = (response.read())
            jason_data = json.loads(html)

        # update information related to the ISBN
        self.ent12.set_text(jason_data[0]['summary']['title'])
        self.ent13.set_text(jason_data[0]['summary']['publisher'])
        self.ent14.set_text(jason_data[0]['summary']['volume'])
        self.ent15.set_text(jason_data[0]['summary']['series'])
        self.ent16.set_text(jason_data[0]['summary']['author'])
        self.ent17.set_text(jason_data[0]['summary']['pubdate'])
        self.ent18.set_text(jason_data[0]['summary']['cover'])

        # text context for collateral of the book with the ISBN
        msg = Gtk.TextBuffer()
        msg.set_text(jason_data[0]['onix']['CollateralDetail']['TextContent'][0]['Text'])
        self.dscrpt.set_buffer(msg)

        # handling of book cover picture
        uri = (jason_data[0]['summary']['cover']).strip()
        r = urllib.request.urlopen(uri)
        loader = GdkPixbuf.PixbufLoader()
        loader.write(r.read())
        loader.close()
        img = loader.get_pixbuf()
        self.img11.set_from_pixbuf(img)


class RowTypical(Gtk.Entry):
    def __init__(self, grid, row, label):
        Gtk.Entry.__init__(self)
        lab = Gtk.Label(label=label)
        lab.set_xalign(1.0)
        self.set_editable(False)
        self.set_can_focus(False)
        self.set_hexpand(True)

        grid.attach(lab, 0, row, 1, 1)
        grid.attach(self, 1, row, 2, 1)


win = OpenBDFinder()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
