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

from Juwel.entry_type.type import Type
from Juwel.gui_object import GuiObject

'''
   "someCheckbox":{
      "value":["yes", "no", "maybe", "blue", "red", "yellow", "orange", "black"],
      "default": ["red", "orange"],
      "single_answer": true,
      "type":"checkbox",
      "required_field":true
   },
   
    "favorite_color":{
      "value":["yes", "no", "maybe", "blue", "red", "yellow", "orange", "black"],
      "default": ["orange"],
      "single_answer": false,
      "type":"checkbox",
      "required_field":true
   },


    *Keys marked with a star are required
    **Keys market with a double star are important
   
   *value : Must be a List of Strings which will be shown as options.
   default : Must be either a List of strings or empty/not existing. 
             Will automatically pre select fields (must be a subset of value).
   single_answer : Must be either true or false. Default is false 
                   On true it is only possible to select exactly one 1 answer not more nor less.
                   On false 0 or more field can be select.
   *type : "checkbox"
   required_field:  If it exist it can be either true or false
   **regex : This field do not have a regex option!
   execute : Contains ONE path to a script which will be executed.
             Which will be read in as value.

'''


class TypeCheckbox(Type):
    def create(self):
        single_answer = False
        if 'single_answer' in self.json_object:
            single_answer = self.json_object['single_answer']
        default = None
        if 'default' in self.json_object:
            if isinstance(self.json_object['default'], list):
                default = self.json_object['default']
        options = None
        if 'value' in self.json_object and isinstance(self.json_object['value'], list):
            options = self.json_object['value']
        else:
            raise ValueError(f"{self.key} is missing value!")

        temp = self.read_value_from_disk()
        if temp is not None:
            options = temp

        if options is not None:
            var_list = list()
            checkbox_list = list()
            value = 0
            if single_answer:
                var = tk.IntVar()
                for item in options:
                    checkbox = tk.Radiobutton(self.parent, text=item, variable=var, value=value)
                    for default_item in default:
                        if item == default_item:
                            checkbox.select()
                    checkbox_list.append(checkbox)
                    value += 1
                return GuiObject(self.key, self.json_object, checkbox_list,
                                 self.json_object['type'], var)
            else:
                for item in options:
                    isChecked = tk.IntVar()
                    checkbox = tk.Checkbutton(self.parent, text=item, variable=isChecked)
                    for default_item in default:
                        if item == default_item:
                            checkbox.select()
                    var_list.append(isChecked)
                    checkbox_list.append(checkbox)
                return GuiObject(self.key, self.json_object, checkbox_list,
                                 self.json_object['type'], var_list)

    def validate(self, gui_object):
        return str()
