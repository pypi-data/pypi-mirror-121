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

import tkcalendar
from datetime import datetime

from Juwel.entry_type.type import Type
from Juwel.gui_object import GuiObject
from Juwel.validator import Validator

'''    
   "expire":{
      "value":"2020-12-02", 
      "type":"datefield",
      "required_field":true,
      "execute":"wc.sh"
   }
   *Keys marked with a star are required
   
   *value: Must be either a valid datetime with format yyyy-mm-dd or empty string
   *type : "datefield"
   required_field:  If it exist it can be either true or false
   regex : Contains ONE valid regex which will be checked on validation
   execute : Contains ONE path to a script which will be executed and later saved into date
'''


class TypeDatefield(Type):
    def create(self):
        try:
            date = datetime.strptime(self.json_object['value'], '%Y-%m-%d')
        except (ValueError, KeyError):
            date = datetime.now()

        try:
            temp = self.read_value_from_disk()
            if temp is not None:
                date = datetime.strptime(temp, '%Y-%m-%d')
        except (ValueError, KeyError):
            date = datetime.now()

        calendar = tkcalendar.Calendar(self.parent, selectmode="day", day=date.day,
                                       month=date.month, year=date.year, date_pattern='yyyy-mm-dd')

        return GuiObject(self.key, self.json_object, calendar, self.json_object['type'])

    def validate(self, gui_object):
        message = str()
        self.get_validate_variables(gui_object)
        selected_date = gui_object.content.get_date()

        if not selected_date:
            if self.required:
                message += f"No date selected at: {gui_object.key}! \n"
        else:
            try:
                datetime.strptime(selected_date, '%Y-%m-%d')
            except ValueError:
                message += f"No valid Datetime entered at: {gui_object.key}! \n"

            if self.regex:
                if not Validator.validate_regex(self.regex, str(selected_date)):
                    message += f"Regex error at: {gui_object.key}! \n"
        return message
