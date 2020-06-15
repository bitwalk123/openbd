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

        # r = 0
        str_label1 = 'ISBN13'
        str_label2 = '書籍情報取得'
        ent10 = RowFirst(grid, str_label1, str_label2)
        (ent10.get_button()).connect("clicked", self.on_button_clicked, ent10)

        # r = 1
        str_label = '書影'
        self.img11 = RowSecond(grid, str_label)

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
        self.dscrpt = RowLast(grid, r, str_label)

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
        if len(isbn) == 0:
            return

        query = self.url_openbd + isbn
        with urllib.request.urlopen(query) as response:
            html = (response.read())
            jason_data = json.loads(html)

        if jason_data[0] is None:
            print("データが見つかりません")
            dialog = Gtk.MessageDialog(parent=self,
                                       flags=0,
                                       message_type=Gtk.MessageType.WARNING,
                                       buttons=Gtk.ButtonsType.OK,
                                       text="データが見つかりません。")
            dialog.run()
            dialog.destroy()
            return

        # handling of book cover picture
        uri = (jason_data[0]['summary']['cover']).strip()
        if len(uri) > 0:
            r = urllib.request.urlopen(uri)
            loader = GdkPixbuf.PixbufLoader()
            loader.write(r.read())
            loader.close()
            img_cover = loader.get_pixbuf()
            self.img11.set_from_pixbuf(img_cover)
        else:
            self.img11.clear()

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


class RowFirst(Gtk.Entry):
    def __init__(self, grid, label1, label2):
        Gtk.Entry.__init__(self)
        self.set_hexpand(True)
        self.set_text('9784047914742')

        lab = Gtk.Label(label=label1)
        lab.set_xalign(1.0)
        self.but = Gtk.Button(label=label2)

        grid.attach(lab, 0, 0, 1, 1)
        grid.attach(self, 1, 0, 1, 1)
        grid.attach(self.but, 2, 0, 1, 1)

    def get_button(self):
        return self.but


class RowSecond(Gtk.Image):
    def __init__(self, grid, label):
        Gtk.Image.__init__(self)
        self.set_halign(Gtk.Align.START)

        lab = Gtk.Label(label=label)
        lab.set_xalign(1.0)

        grid.attach(lab, 0, 1, 1, 1)
        grid.attach(self, 1, 1, 2, 1)


class RowTypical(Gtk.Entry):
    def __init__(self, grid, row, label):
        Gtk.Entry.__init__(self)
        self.set_editable(False)
        self.set_can_focus(False)
        self.set_hexpand(True)

        lab = Gtk.Label(label=label)
        lab.set_xalign(1.0)

        grid.attach(lab, 0, row, 1, 1)
        grid.attach(self, 1, row, 2, 1)


class RowLast(Gtk.TextView):
    def __init__(self, grid, row, label):
        Gtk.TextView.__init__(self)
        self.set_editable(False)
        self.set_can_focus(False)
        self.set_wrap_mode(wrap_mode=Gtk.WrapMode.WORD)

        lab = Gtk.Label(label=label)
        lab.set_xalign(1.0)
        lab.set_valign(Gtk.Align.START)

        scr = Gtk.ScrolledWindow()
        scr.add(self)
        scr.set_hexpand(True)
        scr.set_vexpand(True)

        grid.attach(lab, 0, row, 1, 1)
        grid.attach(scr, 1, row, 2, 1)


win = OpenBDFinder()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
