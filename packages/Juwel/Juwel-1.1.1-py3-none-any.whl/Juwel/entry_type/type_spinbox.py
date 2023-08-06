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
import sys

from Juwel.entry_type.type import Type
from Juwel.gui_object import GuiObject
from Juwel.validator import Validator

'''
    Document for Spinbox
    
   "someSpinbox":{
      "min":"-10",
      "max":"126",
      "increment":"5",
      "default":"0",
      "type":"spinbox",
      "required_field":false
   }
    
   *Keys marked with a star are required
   Systemmax value can differ between computers!
   
   min : Minimum value of the spinbox. Default min is -Systemmax around( -2^63 )
   max : Maximum value of the spinbox. Default max is Systemmax around ( 2^63-1 )
   increment : Value of the factor that the spinbox gets incremented. Default is 1
   default : Default value which the Spinbox has on Start. Default value is 0
   *type : "spinbox"
   required_field:  If it exist it can be either true or false
   regex : Contains ONE valid regex which will be checked on validation
   execute : Contains ONE path to a script which will be executed and later 
             saved into the start value
'''


class TypeSpinbox(Type):
    def create(self):
        min = -sys.maxsize-1
        max = sys.maxsize
        increment = 1
        start = tk.StringVar(self.parent)
        start.set('0')

        if 'min' in self.json_object:
            min = self.json_object['min']
        if 'max' in self.json_object:
            max = self.json_object['max']
        if 'increment' in self.json_object:
            increment = self.json_object['increment']
        if 'default' in self.json_object:
            start.set(self.json_object['default'])

        temp = self.read_value_from_disk()
        if temp is not None:
            start.set(temp)

        spinbox = tk.Spinbox(self.parent, from_=min, to=max,
                             increment=increment, textvariable=start)

        return GuiObject(self.key, self.json_object, spinbox, self.json_object['type'])

    def validate(self, gui_object):
        message = str()
        self.get_validate_variables(gui_object)
        if not Validator.validate_integer(gui_object.content.get()):
            message += f"Input at {gui_object.key} is not a valid number!"
        if self.regex:
            if not Validator.validate_regex(self.regex, gui_object.content.get()):
                message += f"Regex error at: {gui_object.key}! \n"
        return message
