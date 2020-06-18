import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf


class row_first(Gtk.Entry):
    def __init__(self, grid, label1, label2):
        Gtk.Entry.__init__(self)
        self.set_hexpand(True)
        # self.set_text('9784047914742')

        lab = Gtk.Label(label=label1)
        lab.set_xalign(1.0)
        self.but = Gtk.Button(label=label2)

        grid.attach(lab, 0, 0, 1, 1)
        grid.attach(self, 1, 0, 1, 1)
        grid.attach(self.but, 2, 0, 1, 1)

    def get_button(self):
        return self.but


class row_second(Gtk.Image):
    def __init__(self, grid, label):
        Gtk.Image.__init__(self)
        self.set_halign(Gtk.Align.START)

        lab = Gtk.Label(label=label)
        lab.set_xalign(1.0)
        lab.set_valign(Gtk.Align.START)

        grid.attach(lab, 0, 1, 1, 1)
        grid.attach(self, 1, 1, 2, 1)


class row_typical(Gtk.Entry):
    def __init__(self, grid, row, label):
        Gtk.Entry.__init__(self)
        self.set_editable(False)
        self.set_can_focus(False)
        self.set_hexpand(True)

        lab = Gtk.Label(label=label)
        lab.set_xalign(1.0)

        grid.attach(lab, 0, row, 1, 1)
        grid.attach(self, 1, row, 2, 1)


class row_last(Gtk.TextView):
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
