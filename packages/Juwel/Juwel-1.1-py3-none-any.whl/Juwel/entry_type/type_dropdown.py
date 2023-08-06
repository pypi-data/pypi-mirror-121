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
from Juwel.validator import Validator
'''
"pizza_topics":{
      "value":[
         "salami",
         "tomato"
      ],
      "type":"dropdown",
   }
   
   *Keys marked with a star are required
   
   *value: Must be a list of strings.
   *type : "datefield"
   required_field:  If it exist it can be either true or false
   regex : Contains ONE valid regex which will be checked on validation
   execute : Contains ONE path to a script which will be executed and later saved into options
   
   
'''


class TypeDropdown(Type):
    def create(self):
        options = list()
        if 'value' in self.json_object:
            if isinstance(self.json_object['value'], list):
                options = self.json_object['value']

        temp = self.read_value_from_disk()
        if temp is not None:
            options = temp

        variable = tk.StringVar(self.parent)
        variable.set(options[0])
        dropdown = tk.OptionMenu(self.parent, variable, *options)

        return GuiObject(self.key, self. json_object, dropdown, self.json_object['type'], variable)

    def validate(self, gui_object):
        message = str()
        self.get_validate_variables(gui_object)
        if not Validator.isEmpty(self.variable.get()):
            message += f"Input at {gui_object.key} is Empty!"
        if self.regex:
            if not Validator.validate_regex(self.regex, self.variable.get()):
                message += f"Regex error at: {gui_object.key}! \n"
        return message
