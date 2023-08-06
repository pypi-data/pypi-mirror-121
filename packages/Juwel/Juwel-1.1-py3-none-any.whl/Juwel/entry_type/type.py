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
from abc import ABC, abstractmethod

from Juwel.validator import Validator
from Juwel.file_system import FileSystem


class Type(ABC):
    def create_init(self, key, json_object, parent):
        self.key = key
        self.json_object = json_object
        self.parent = parent
        return self

    @staticmethod
    @abstractmethod
    def create():
        pass

    @staticmethod
    @abstractmethod
    def validate(gui_object):
        pass

    def get_validate_variables(self, gui_object):
        self.variable = gui_object.variable
        if self.variable is not None:
            self.text = gui_object.variable.get()
        self.regex = Validator.get_regex(gui_object.json_object)
        self.required = Validator.is_required(gui_object.json_object)

    def is_required(self):
        is_required = tk.Checkbutton(self.parent, text="Required", command=self._popup_required)
        is_required.deselect()
        if ('required_field' in self.json_object and self.json_object['required_field']) \
                or 'required_field' not in self.json_object:
            is_required.select()

        is_required.grid(row=self.iter, column=1000)

    def read_value_from_disk(self):
        fs = FileSystem()
        path = fs.get_temp_path()
        path += f'/{self.key}.temp'
        if fs.exist_file(path):
            return fs.read_file(path)
