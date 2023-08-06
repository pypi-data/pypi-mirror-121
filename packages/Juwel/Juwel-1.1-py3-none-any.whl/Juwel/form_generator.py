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
import subprocess, sys

import tkinter as tk

from Juwel.entry_type.type_factory import TypeFactory
from Juwel.json_manager import JsonManager
from Juwel.file_system import FileSystem
from Juwel.validator import Validator


class FormGenerator(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root

        fs = FileSystem()
        self.root.geometry(fs.read_geometry())
        self.root.wm_title("Config Generator")
        self.root.bind("<Configure>", self.save_size)

        self.frame1 = tk.Frame(self.root)
        self.frame1.pack(side=tk.TOP, fill=tk.X)
        self.frame2 = tk.Frame(self.root)
        self.frame2.pack(side=tk.TOP, fill=tk.X)
        self.frame3 = tk.Frame(self.root)
        self.frame3.pack(side=tk.BOTTOM, fill=tk.X)

        self.isChecked = tk.IntVar()
        self.is_filter = tk.Checkbutton(self.frame1, text="", variable=self.isChecked).pack()

        self.btn_filter = tk.Button(self.frame1)
        self.btn_filter.pack(side="top")
        self.btn_filter['text'] = "Filter required only"
        self.btn_filter['command'] = self.refresh

        self.btn_print = tk.Button(self.frame3)
        self.btn_print.pack(side="bottom")
        self.btn_print['text'] = "Save to Json"
        self.btn_print['command'] = self.save_to_json

        self.gui_list = list()

        self.file = None
        if len(sys.argv) > 1:
            if sys.argv[1].lower() != "true" and sys.argv[1].lower() != "false":
                self.file = sys.argv[1]

        try:
            jm = JsonManager()
            self.json_object = jm.read_json(self.file)
            fs.execute_scripts(self.json_object)
        except (FileNotFoundError, RuntimeError, OSError) as ex:
            self.popup("Critical Error", ex, kill_app=True)
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as ex:
            self.popup("Script Error", ex)
        self.generate()

    def save_size(self, event):
        fs = FileSystem()
        fs.save_file(self.root.geometry(), fs.get_package_path()+"/display_size.config")

    def is_filtered(self):
        if self.isChecked.get():
            return True
        else:
            return False

    def refresh(self):
        self.column = 0
        self.row = 0
        if self.frame2 is not None:
            self.frame2.destroy()
        self.frame2 = tk.Frame(self.root)
        self.frame2.pack(side=tk.TOP, fill=tk.X)
        self.gui_list = list()
        self.generate()

    def make_space(self):
        self.row += 1
        space = tk.Label(self.frame2, text=" ")
        space.grid(row=self.row, column=1)
        self.row += 1

    def make_label(self, gui_object):
        if ('required_field' in gui_object.json_object and
                gui_object.json_object['required_field']) or \
                'required_field' not in self.json_object:
            lable = tk.Label(self.frame2, text=f"*{gui_object.key}")
        else:
            lable = tk.Label(self.frame2, text=gui_object.key)
        lable.grid(row=self.row, column=self.column)
        self.column += 1

    def make_grid(self, gui_object):
        self.make_label(gui_object)
        overlay_object = gui_object.content
        if isinstance(overlay_object, list):
            for item in overlay_object:
                item.grid(row=self.row, column=self.column)
                self.column += 1
        else:
            overlay_object.grid(row=self.row, column=self.column)
            self.column += 1

    def generate(self):
        self.column = 0
        self.row = 0
        try:
            for key, value in self.json_object.items():
                if isinstance(value, dict):
                    if self.is_filtered():
                        if 'required_field' not in value or value['required_field']:
                            action = TypeFactory().create_init(key, value, self.frame2)
                    else:
                        action = TypeFactory().create_init(key, value, self.frame2)

                    if not self.is_filtered() or 'required_field' not in value or\
                            ('required_field' in value and value['required_field']):
                        self.gui_list.append(action.create())
                        if "layout" in self.gui_list[-1].json_object and \
                                self.gui_list[-1].json_object["layout"] == "new_line":
                            self.row += 1
                            self.column = 0
                            self.make_space()
                            self.make_grid(self.gui_list[-1])
                        else:
                            self.make_grid(self.gui_list[-1])

        except NotImplementedError as ex:
            self.popup("Critical Error", "UI Generation Failed!\n"+str(ex), kill_app=True)

    def save_to_json(self):
        if self.validate():
            fs = FileSystem()
            cwd = fs.get_dir_cwd()
            print(self.file)
            if self.file is not None and self.file != ".":
                save_path = cwd+"/"+self.file+".meta"
            else:
                file_name = cwd.split("/")[-1]
                save_path = cwd+"/"+file_name+".meta"
            try:
                JsonManager.write_json(self.gui_list, save_path)
                self.popup("Success!", "Meta data saved!")
            except (ValueError, FileExistsError, NotImplementedError, OSError) as ex:
                    self.popup('Error', ex)

    def validate(self):
        success = True
        try:
            for items in self.gui_list:
                result = Validator().validate(items)
                if result:
                    success = False
                    self.popup('Error', result)
        except NotImplementedError as ex:
            self.popup("Critical Error", "Validation Failed!\n" + str(ex), kill_app=True)

        return success

    def popup(self, title, message, kill_app=False):
        window = tk.Toplevel(self.root)
        window.wm_title(title)
        # Not working with more than 1 screen
        self.root.eval(f'tk::PlaceWindow {str(window)} center')

        label = tk.Label(window, text=message)
        label.pack()

        if kill_app:
            var = tk.IntVar()
            button = tk.Button(window, text="Okay", command=lambda: var.set(1))
            button.pack()
            button.wait_variable(var)
            exit(1)
        else:
            button = tk.Button(window, text="Okay", command=window.destroy)
            button.pack()
