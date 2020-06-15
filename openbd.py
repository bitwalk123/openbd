import json
import gi
from io import BytesIO
import pprint
import urllib.request
import urllib3
import ssl

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
#from gi.repository import WebKit2

# PEP 476 -- Enabling certificate verification by default for stdlib http clients
ssl._create_default_https_context = ssl._create_unverified_context

class OpenBD(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="OpenBD")
        self.set_default_size(0, 0)

        grid = Gtk.Grid()
        self.add(grid)

        lab00 = Gtk.Label(label="ISBN13")
        lab00.set_xalign(1.0)
        self.ent10 = Gtk.Entry()
        but20 = Gtk.Button(label="書籍情報取得")
        but20.connect("clicked", self.on_button_clicked)

        lab01 = Gtk.Label(label="書影")
        lab01.set_xalign(1.0)
        self.ent11 = Gtk.Entry()

        lab02 = Gtk.Label(label="書籍名")
        lab02.set_xalign(1.0)
        self.ent12 = Gtk.Entry()

        lab03 = Gtk.Label(label="出版社")
        lab03.set_xalign(1.0)
        self.ent13 = Gtk.Entry()

        lab04 = Gtk.Label(label="巻")
        lab04.set_xalign(1.0)
        self.ent14 = Gtk.Entry()

        lab05 = Gtk.Label(label="シリーズ")
        lab05.set_xalign(1.0)
        self.ent15 = Gtk.Entry()

        lab06 = Gtk.Label(label="著者")
        lab06.set_xalign(1.0)
        self.ent16 = Gtk.Entry()

        lab07 = Gtk.Label(label="出版日")
        lab07.set_xalign(1.0)
        self.ent17 = Gtk.Entry()

        lab08 = Gtk.Label(label="サムネールURI")
        lab08.set_xalign(1.0)
        self.ent18 = Gtk.Entry()

        lab09 = Gtk.Label(label="詳細")
        lab09.set_xalign(1.0)
        #self.ent19 = Gtk.Entry()
        scr19 = Gtk.ScrolledWindow()
        self.dscrpt = Gtk.TextView()
        self.dscrpt.set_wrap_mode(wrap_mode=Gtk.WrapMode.WORD)
        scr19.add(self.dscrpt)

        grid.attach(lab00, 0, 0, 1, 1)
        grid.attach(self.ent10, 1, 0, 1, 1)
        grid.attach(but20, 2, 0, 1, 1)

        grid.attach(lab01, 0, 1, 1, 1)
        grid.attach(self.ent11, 1, 1, 2, 1)

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

    def on_button_clicked(self, button):
        with urllib.request.urlopen('https://api.openbd.jp/v1/get?isbn=9784047914742') as response:
            html = (response.read())
            jason_data = json.loads(html)
            pprint.pprint(jason_data, width=40)
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

            #http = urllib3.PoolManager()
            #r = http.request('GET', jason_data[0]['summary']['cover'])
            uri = jason_data[0]['summary']['cover']
            print(uri)
            r = urllib.request.urlopen(uri)
            print(r.read())
            #jpgdata = r.read()
            #file_jpgdata = BytesIO(jpgdata)
            #img = Gtk.Image.new_from_file(file_jpgdata)
            loader = GdkPixbuf.PixbufLoader()
            loader.write(r.read())
            loader.close()
            #p = GdkPixbuf.Pixbuf.new_from_bytes(file_jpgdata)
            #self.image.set_from_pixbuf(loader.get_pixbuf())
            #webview = WebKit.WebView()
            #webview.load_uri(jason_data[0]['summary']['cover'])

win = OpenBD()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()