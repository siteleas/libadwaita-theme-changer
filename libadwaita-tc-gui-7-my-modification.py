#!/bin/python3

############################################
#
# Libadwaita Theme Changer
# created by OdzioM
# script filename: libadwaita-tc-gui-5.py
#
############################################

import os
import subprocess as sp
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import json

class ThemeChanger:
    def __init__(self):
        self.home_dir = os.getenv('HOME')
        self.config_dir = "/.config"
        self.themes_dir = "/.themes"
        self.load_settings()
        self.root = tk.Tk()
        self.root.title("Libadwaita Theme Changer")
        self.check_directories()
        self.themes = self.get_themes()
        if self.themes:
            self.theme_var = tk.StringVar()
            self.theme_var.set(self.themes[0])
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
        tk.Label(self.root, text="Select theme:").pack()
        theme_menu = tk.OptionMenu(self.root, self.theme_var, *self.themes)
        theme_menu.pack()
        tk.Button(self.root, text="Apply", command=self.apply_theme).pack()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="&File", menu=file_menu)
        file_menu.add_command(label="E&xit", command=self.root.destroy)
        options_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="&Options", menu=options_menu)
        options_menu.add_command(label="S&ettings", command=self.settings_screen)

    def apply_theme(self):
        try:
            theme = self.theme_var.get()
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
            messagebox.showerror("Error", str(e))

    def check_directories(self):
        if not os.path.exists(self.home_dir + self.config_dir):
            self.settings_screen("Config directory does not exist. Please provide the correct directory.")
        elif not os.path.exists(self.home_dir + self.themes_dir):
            self.settings_screen("Themes directory does not exist. Please provide the correct directory.")

    def settings_screen(self, error_message=None):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.transient(self.root)  # Make it a modal window
        settings_window.grab_set()  # Make it stay on top
        frame = tk.Frame(settings_window, highlightbackground="black", highlightthickness=0)
        frame.pack(padx=40, pady=25)  # Add a margin around the frame
        if error_message:
            tk.Label(frame, text=error_message, fg="red").pack()
        tk.Label(frame, text="Config Dir:", anchor="w").pack(fill="x")  # Make the label left aligned
        config_dir_entry = tk.Entry(frame)
        config_dir_entry.insert(0, self.config_dir)
        config_dir_entry.pack(fill="x")
        tk.Label(frame, text="Themes Dir:", anchor="w").pack(fill="x")  # Make the label left aligned
        themes_dir_entry = tk.Entry(frame)
        themes_dir_entry.insert(0, self.themes_dir)
        themes_dir_entry.pack(fill="x")
        def save_settings():
            self.config_dir = config_dir_entry.get()
            self.themes_dir = themes_dir_entry.get()
            self.save_settings()
            settings_window.destroy()
            self.themes = self.get_themes()
            if self.themes:
                self.theme_var = tk.StringVar()
                self.theme_var.set(self.themes[0])
                self.create_widgets()
        tk.Button(frame, text="&Save", command=save_settings).pack(fill="x")
        tk.Button(frame, text="C&ancel", command=settings_window.destroy).pack(fill="x")
        self.root.wait_window(settings_window)  # Wait for the settings window to close


    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ThemeChanger()
    app.run()

