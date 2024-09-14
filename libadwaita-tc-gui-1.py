#!/bin/python3

############################################
#
# Libadwaita Theme Changer
# created by OdzioM
# script filename: libadwaita-tc-gui-1.py
#
############################################

import os
import subprocess as sp
import tkinter as tk
from tkinter import filedialog, messagebox

class ThemeChanger:
    def __init__(self):
        self.home_dir = os.getenv('HOME')
        self.config_dir = "/.config"
        self.themes_dir = "/.themes"
        self.root = tk.Tk()
        self.root.title("Libadwaita Theme Changer")
        self.themes = self.get_themes()
        self.theme_var = tk.StringVar()
        self.theme_var.set(self.themes[0])
        self.create_widgets()

    def get_themes(self):
        try:
            return str(sp.run(["ls", f'{self.home_dir}{self.themes_dir}/'], stdout=sp.PIPE).stdout.decode("UTF-8")).split()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []

    def create_widgets(self):
        tk.Label(self.root, text="Select theme:").pack()
        theme_menu = tk.OptionMenu(self.root, self.theme_var, *self.themes)
        theme_menu.pack()
        tk.Button(self.root, text="Apply", command=self.apply_theme).pack()
        tk.Button(self.root, text="Reset", command=self.reset_theme).pack()
        tk.Button(self.root, text="Exit", command=self.root.destroy).pack()

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

    def reset_theme(self):
        try:
            print(f'\n***\nResetting theme to default!\n***\n')
            sp.run(["rm", f'{self.home_dir}{self.config_dir}/gtk-4.0/gtk.css'])
            sp.run(["rm", f'{self.home_dir}{self.config_dir}/gtk-4.0/gtk-dark.css'])
            sp.run(["rm", f'{self.home_dir}{self.config_dir}/gtk-4.0/assets'])
            sp.run(["rm", f'{self.home_dir}{self.config_dir}/assets'])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ThemeChanger()
    app.run()
