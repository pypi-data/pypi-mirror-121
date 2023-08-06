#!/usr/bin/env python3
'''
    Juwel - This program is supposed to create sidecar file to artificially create
    meta data.
    Copyright (C) 2021 - Marco Tenderra

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import tkinter as tk
from Juwel.form_generator import FormGenerator


# main.py "nothing"/./file_name.dataType timeout=true/false
# main.py empty string result in newst file in CWD
# main.py . results in loading config for folder
# main.py file_name.dataType results in loading config for data Type
# main.py true or false results in activating or deactivating timeout for scripts default is true
# example
# main.py myPDF.pdf

def main():
    root = tk.Tk()
    app = FormGenerator(root)
    app.mainloop()
