#!/usr/bin/env python

import glob
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import Gtk, Gdk, GdkPixbuf
import os
import json
import random
import subprocess
import sys
from xdg import DesktopEntry


class Freshest:
    def __init__(self, profile="default"):
        try:
            confdir = os.environ["XDG_CONFIG_HOME"]
        except KeyError:
            confdir = os.path.join(os.environ["HOME"], ".config")
        self.profiledir = os.path.join(confdir, "freshest", profile)
        self.appsdir = os.path.join(self.profiledir, "applications/")
        self.listfile = os.path.join(self.profiledir, "list.json")
        self.conffile = os.path.join(self.profiledir, "config.json")

        if not os.path.isdir(self.profiledir):
            self.create_profile(self.profiledir)

        self.__desktop_files = self.update_list()

        f = open(self.conffile, "r")
        config = json.load(f)
        f.close()

        wintitle = "Freshest"
        if profile != "default":
            wintitle += " (" + profile + ")"
        self.__window = Gtk.Window(title=wintitle)
        self.__window.set_default_size(config["width"], config["height"])
        self.__window.move(config["x"], config["y"])

        scrolledwindow = Gtk.ScrolledWindow()

        liststore = Gtk.ListStore(Pixbuf, str)
        self.__iconview = Gtk.IconView.new()
        self.__iconview.set_model(liststore)
        self.__iconview.set_pixbuf_column(0)
        self.__iconview.set_text_column(1)
        self.__iconview.set_item_width(config["columnwidth"])
        self.__iconview.set_activate_on_single_click(True)

        for f in self.__desktop_files:
            x = DesktopEntry.DesktopEntry(filename=f)
            try:
                pixbuf = Gtk.IconTheme.get_default().load_icon(
                    x.getIcon(), config["iconsize"], 0)
            except:
                try:
                    pixbuf = Pixbuf.new_from_file(x.getIcon())
                    pixbuf = pixbuf.scale_simple(
                        config["iconsize"], config["iconsize"],
                        GdkPixbuf.InterpType.NEAREST)
                except:
                    pixbuf = Gtk.IconTheme.get_default().load_icon(
                        "gtk-execute", config["iconsize"], 0)
            liststore.append([pixbuf, x.getName()])

        self.__iconview.connect("item-activated", self.on_item_activated)
        self.__window.connect("key_press_event", self.on_key_press)

        scrolledwindow.add(self.__iconview)

        self.__window.connect("destroy", lambda w: Gtk.main_quit())

        self.__window.add(scrolledwindow)
        self.__window.show_all()

    def create_profile(self, profile):
        os.makedirs(self.profiledir)
        os.mkdir(self.appsdir)
        f = open(self.listfile, "w")
        json.dump([], f)
        f.close()
        f = open(os.path.join(self.appsdir, "example.desktop"), "w")
        f.write("""[Desktop Entry]
Type=Application
Name=Add *.desktop files to """ + self.appsdir + """
Icon=gtk-info
Exec=true""")
        f.close()
        f = open(self.conffile, "w")
        config = {"x": 100, "y": 100,
                  "width": 640, "height": 480,
                  "columnwidth": 96, "iconsize": 96}
        json.dump(config, f, sort_keys=True, indent=4 * ' ')
        f.close()

    def update_list(self):
        # read from the list file, which is ordered but not necessarily
        # up-to-date
        f = open(self.listfile, 'r')
        old = json.load(f)
        f.close()

        # read actual files
        new = []
        actual_files = glob.glob(os.path.join(self.appsdir,
                                              "*.desktop"))
        for actual_file in actual_files:
            new.append(actual_file)

        # merge
        for olditem in old:
            if olditem not in new:
                old.remove(olditem)
        for newitem in new:
            if newitem not in old:
                old.append(newitem)

        # update file
        f = open(self.listfile, 'w')
        json.dump(old, f, indent=4 * ' ')
        f.close()

        return old

    def update_freshest(self, application):
        self.__desktop_files.remove(application)
        self.__desktop_files.insert(0, application)
        f = open(self.listfile, 'w')
        json.dump(self.__desktop_files, f, indent=4 * ' ')
        f.close()

    def on_item_activated(self, widget, item):
        selected_application = self.__desktop_files[int(item.to_string())]
        self.update_freshest(selected_application)

        # save position and size of the window
        f = open(self.conffile, "r")
        config = json.load(f)
        f.close()
        f = open(self.conffile, "w")
        winpos = self.__window.get_position()
        winsize = self.__window.get_size()
        config["x"] = winpos[0]
        config["y"] = winpos[1]
        config["width"] = winsize[0]
        config["height"] = winsize[1]
        json.dump(config, f, sort_keys=True, indent=4 * ' ')
        f.close()

        x = DesktopEntry.DesktopEntry(filename=selected_application)
        subprocess.Popen(x.getExec(), shell=True)
        quit()

    def on_key_press(self, widget, event):
        key = Gdk.keyval_name(event.keyval)
        if key == "r":
            x = Gtk.TreePath.new_from_string(
                str(random.randrange(len(self.__desktop_files))))
            self.__iconview.select_path(x)
            self.__iconview.set_cursor(x, None, False)
        elif key in ["Escape", "q", "Q", "F10"]:
            quit()

if len(sys.argv) == 2:
    Freshest(profile=sys.argv[1])
else:
    Freshest()
Gtk.main()
