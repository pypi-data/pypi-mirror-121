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
    Document for E-Mails
   "blue":{
      "value":"a@b.com",
      "type":"email",
      "required_field":false,
      "regex":"[^@]+@[^@]+\\.[^@]+",
      "execute":"ping.sh"
   }   
   *Keys marked with a star are required
   
   *value: Must be either a valid EMail or empty string
   *type : "email"
   required_field:  If it exist it can be either true or false
   regex : Contains ONE valid regex which will be checked on validation. 
           This application already has a validator for a E-Mail address
   execute : Contains ONE path to a script which will be executed  
             This Script needs to save a file in temp folder and named key.temp. 
             If everything is correct this application will read the content of this file.
             
    Document for textfield
    "author":{
      "value":"",
      "type":"textfield",
      "required_field":true
   } 
   *value: Must be either a valid EMail or empty string.
   *type : "textfield"
   required_field:  If it exist it can be either true or false.
   regex : Contains ONE valid regex which will be checked on validation. 
   execute: same as above.

'''


class TypeTextfield(Type):
    def create(self):
        text = tk.StringVar()

        if 'value' in self.json_object:
            text.set(self.json_object['value'])

        temp = self.read_value_from_disk()
        if temp is not None:
            text.set(temp)

        input = tk.Entry(self.parent, textvariable=text)

        return GuiObject(self.key, self.json_object, input, self.json_object['type'], text)

    def validate(self, gui_object):
        message = str()
        self.get_validate_variables(gui_object)

        if not Validator.isEmpty(self.text):
            if self.required:
                message += f"Input at {gui_object.key} is Empty! \n"
        else:
            if gui_object.type == 'email':
                if not Validator.validate_email(self.text):
                    message += f"Input at {gui_object.key} is not a valid E-Mail! \n"
            if self.regex:
                if not Validator.validate_regex(self.regex, self.text):
                    message += f"Regex error at: {gui_object.key}! \n"
        return message
