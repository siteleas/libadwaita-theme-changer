#!/bin/python3

############################################
#
# Libadwaita Theme Changer
# created by OdzioM
# script filename: libadwaita-tc-gtk-2.py
#
############################################

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio
import os
import subprocess as sp
import json
from gi.repository import Gtk, Gio, Gdk


class ThemeChanger(Gtk.Application):
    def __init__(self, application_id, flags):
        super().__init__(application_id=application_id, flags=flags)
        self.home_dir = os.getenv('HOME')
        self.config_dir = "/.config"
        self.themes_dir = "/.themes"
        self.load_settings()
        self.themes = self.get_themes()

    def do_activate(self):
        # Load the CSS file
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('styles.css')
        self.window.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.window = Gtk.ApplicationWindow(application=self)
        self.window.set_title("Libadwaita Theme Changer")
        self.check_directories()
        if self.themes:
            self.create_widgets()
        self.create_menu()
        self.window.present()

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
        for widget in self.window.get_content_area().get_children():
            self.window.get_content_area().remove(widget)
        label = Gtk.Label(label="Change LibAdwaita Theme")
        label.set_margin_top(20)
        label.set_margin_bottom(10)
        self.window.get_content_area().append(label)
        label = Gtk.Label(label="Choose theme to activate:")
        self.window.get_content_area().append(label)
        theme_store = Gtk.StringListStore()
        for theme in self.themes:
            theme_store.append([theme])
        theme_combo = Gtk.ComboBox(model=theme_store, expression=Gtk.PropertyExpression.new(Gtk.StringObject, "string"))
        theme_combo.set_selected(0)
        self.window.get_content_area().append(theme_combo)
        button = Gtk.Button(label="Activate")
        button.connect("clicked", self.apply_theme, theme_combo)
        self.window.get_content_area().append(button)

    def create_menu(self):
        menubar = Gtk.MenuBar()
        self.window.get_content_area().append(menubar)
        file_menu = Gtk.Menu()
        menubar.append(Gtk.MenuButton(label="File", menu=file_menu))
        file_menu.append(Gtk.MenuItem(label="Exit", action_name="app.quit"))
        options_menu = Gtk.Menu()
        menubar.append(Gtk.MenuButton(label="Options", menu=options_menu))
        options_menu.append(Gtk.MenuItem(label="Settings", action_name="app.settings"))

    def apply_theme(self, button, combo):
        try:
            theme = combo.get_selected_item().get_string(0)
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
            dialog = Gtk.MessageDialog(transient_for=self.window, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK, text=str(e))
            dialog.present()

    def check_directories(self):
        if not os.path.exists(self.home_dir + self.config_dir):
            self.settings_screen("Config directory does not exist. Please provide the correct directory.")
        elif not os.path.exists(self.home_dir + self.themes_dir):
            self.settings_screen("Themes directory does not exist. Please provide the correct directory.")

    def settings_screen(self, error_message=None):
        settings_window = Gtk.Window(transient_for=self.window)
        settings_window.set_title("Settings")
        settings_window.set_modal(True)
        if error_message:
            label = Gtk.Label(label=error_message)
            label.get_style_context().add_class("error")
            settings_window.get_content_area().append(label)
        label = Gtk.Label(label="Config Dir:")
        settings_window.get_content_area().append(label)
        config_dir_entry = Gtk.Entry()
        config_dir_entry.set_text(self.config_dir)
        settings_window.get_content_area().append(config_dir_entry)
        label = Gtk.Label(label="Themes Dir:")
        settings_window.get_content_area().append(label)
        themes_dir_entry = Gtk.Entry()
        themes_dir_entry.set_text(self.themes_dir)
        settings_window.get_content_area().append(themes_dir_entry)
        def save_settings():
            self.config_dir = config_dir_entry.get_text()
            self.themes_dir = themes_dir_entry.get_text()
            self.save_settings()
            settings_window.destroy()
            self.themes = self.get_themes()
            if self.themes:
                self.create_widgets()
        button = Gtk.Button(label="Save")
        button.connect("clicked", save_settings)
        settings_window.get_content_area().append(button)
        button = Gtk.Button(label="Cancel")
        button.connect("clicked", settings_window.destroy)
        settings_window.get_content_area().append(button)
        settings_window.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate_action(self, action, param):
        if action.name == "settings":
            self.settings_screen()

if __name__ == "__main__":
    app = ThemeChanger("com.example.ThemeChanger", Gio.ApplicationFlags.FLAGS_NONE)
    app.run()

