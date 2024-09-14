#!/bin/python3

############################################
#
# Libadwaita Theme Changer
# created by OdzioM
# script filename: libadwaita-tc-gtk-6.py
#
############################################

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import subprocess as sp
import json
import sys

class ThemeChanger(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.home_dir = os.getenv('HOME')
        self.config_dir = "/.config"
        self.themes_dir = "/.themes"
        self.load_settings()
        self.check_directories()
        self.themes = self.get_themes()
        self.create_widgets()
        self.create_menu()

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.config_dir = settings['config_dir']
                self.themes_dir = settings['themes_dir']
        except FileNotFoundError:
            pass

    def save_settings(self):
        settings = {
            'config_dir': self.config_dir,
            'themes_dir': self.themes_dir
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    def get_themes(self):
        try:
            return str(sp.run(["ls", f'{self.home_dir}{self.themes_dir}/'], stdout=sp.PIPE).stdout.decode("UTF-8")).split()
        except Exception as e:
            return []

    def create_widgets(self):
        self.set_title("Libadwaita Theme Changer")
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.box.set_margin_start(40)
        self.box.set_margin_end(40)
        self.box.set_margin_bottom(25)
        self.add(self.box)
        label = Gtk.Label(label="Change LibAdwaita Theme")
        self.box.pack_start(label, True, True, 0)
        self.theme_combo = Gtk.ComboBoxText()
        for theme in self.themes:
            self.theme_combo.append_text(theme)
        self.theme_combo.set_active(0)
        self.box.pack_start(self.theme_combo, True, True, 0)
        button = Gtk.Button(label="Activate")
        button.connect("clicked", self.apply_theme)
        self.box.pack_start(button, True, True, 0)

    def create_menu(self):
        menubar = Gtk.MenuBar()
        menubar.set_hexpand(True)
        self.box.pack_start(menubar, False, False, 0)
        file_menu = Gtk.Menu()
        file_item = Gtk.MenuItem(label="File")
        file_item.set_submenu(file_menu)
        menubar.append(file_item)
        exit_item = Gtk.MenuItem(label="Exit")
        exit_item.connect("activate", self.on_exit)
        file_menu.append(exit_item)
        options_menu = Gtk.Menu()
        options_item = Gtk.MenuItem(label="Options")
        options_item.set_submenu(options_menu)
        menubar.append(options_item)
        settings_item = Gtk.MenuItem(label="Settings")
        settings_item.connect("activate", self.settings_screen)
        options_menu.append(settings_item)

    def apply_theme(self, button):
        try:
            theme = self.theme_combo.get_active_text()
            print(f'\n***\nChoosed {theme}\n***\n')
            print("Removing previous theme...")
            sp.run(["rm", f'{self.home_dir}{self.config_dir}/gtk-4.0/gtk.css'])
            sp.run(["rm", f'{self.home_dir}{self.config_dir}/gtk-4.0/gtk-dark.css'])
            sp.run(["rm", f'{self.home_dir}{self.config_dir}/gtk-4.0/assets'])
            sp.run(["rm", f'{self.home_dir}{self.config_dir}/assets'])
            print("Installing new theme...")
            sp.run(["ln", "-s", f'{self.home_dir}{self.themes_dir}/{theme}/gtk-4.0/gtk.css', f'{self.home_dir}{self.config_dir}/gtk-4.0/gtk.css'])
            sp.run(["ln", "-s", f'{self.home_dir}{self.themes_dir}/{theme}/gtk-4.0/gtk-dark.css', f'{self.home_dir}{self.config_dir}/gtk-4.0/gtk-dark.css'])
            sp.run(["ln", "-s", f'{self.home_dir}{self.themes_dir}/{theme}/gtk-4.0/assets', f'{self.home_dir}{self.config_dir}/gtk-4.0/assets'])
            sp.run(["ln", "-s", f'{self.home_dir}{self.themes_dir}/{theme}/assets', f'{self.home_dir}{self.config_dir}/assets'])
            print("Done.")
        except Exception as e:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, str(e))
            dialog.run()
            dialog.destroy()

    def check_directories(self):
        if not os.path.exists(self.home_dir + self.config_dir):
            self.settings_screen("Config directory does not exist. Please provide the correct directory.")
        elif not os.path.exists(self.home_dir + self.themes_dir):
            self.settings_screen("Themes directory does not exist. Please provide the correct directory.")

    def settings_screen(self, error_message=None):
        settings_window = Gtk.Window()
        settings_window.set_title("Settings")
        settings_window.set_transient_for(self)
        settings_window.set_modal(True)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_margin_start(40)
        box.set_margin_end(40)
        box.set_margin_bottom(25)
        settings_window.add(box)
        if error_message:
            label = Gtk.Label(label=error_message)
            label.set_markup(f'<span color="red">{error_message}</span>')
            box.pack_start(label, True, True, 0)
        label = Gtk.Label(label="Config Dir:")
        box.pack_start(label, True, True, 0)
        config_dir_entry = Gtk.Entry()
        config_dir_entry.set_text(self.config_dir)
        box.pack_start(config_dir_entry, True, True, 0)
        label = Gtk.Label(label="Themes Dir:")
        box.pack_start(label, True, True, 0)
        themes_dir_entry = Gtk.Entry()
        themes_dir_entry.set_text(self.themes_dir)
        box.pack_start(themes_dir_entry, True, True, 0)
        def save_settings(button):
            self.config_dir = config_dir_entry.get_text()
            self.themes_dir = themes_dir_entry.get_text()
            self.save_settings()
            settings_window.destroy()
            self.themes = self.get_themes()
            self.theme_combo.remove_all()
            for theme in self.themes:
                self.theme_combo.append_text(theme)
            self.theme_combo.set_active(0)
        button = Gtk.Button(label="Save")
        button.connect("clicked", save_settings)
        box.pack_start(button, True, True, 0)
        button = Gtk.Button(label="Cancel")
        button.connect("clicked", lambda button: settings_window.destroy())
        box.pack_start(button, True, True, 0)
        settings_window.show_all()

    def on_exit(self, item):
        Gtk.main_quit()
        sys.exit(0)

window = ThemeChanger()
window.show_all()
Gtk.main()
