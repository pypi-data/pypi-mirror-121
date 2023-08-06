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

from Juwel.entry_type.type import Type
from Juwel import entry_type


class TypeFactory(Type):
    def create_init(self, key, json_object, parent):
        if 'textfield' == json_object['type']:
            self.action = entry_type.TypeTextfield().create_init(key, json_object, parent)
        elif 'checkbox' == json_object['type']:
            self.action = entry_type.TypeCheckbox().create_init(key, json_object, parent)
        elif 'datefield' == json_object['type']:
            self.action = entry_type.TypeDatefield().create_init(key, json_object, parent)
        elif 'email' == json_object['type']:
            self.action = entry_type.TypeTextfield().create_init(key, json_object, parent)
        elif 'dropdown' == json_object['type']:
            self.action = entry_type.TypeDropdown().create_init(key, json_object, parent)
        elif 'spinbox' == json_object['type']:
            self.action = entry_type.TypeSpinbox().create_init(key, json_object, parent)
        else:
            raise NotImplementedError(f"The argument: {json_object['type']} "
                                      "is not accepted! \nOnly type "
                                      "textfield/checkbox/datefield/email/dropdown/spinbox/ "
                                      "allowed!")
        return self

    def validate_init(self, gui_object):
        if 'textfield' == gui_object.type:
            self.action = entry_type.TypeTextfield()
        elif 'checkbox' == gui_object.type:
            self.action = entry_type.TypeCheckbox()
        elif 'datefield' == gui_object.type:
            self.action = entry_type.TypeDatefield()
        elif 'email' == gui_object.type:
            self.action = entry_type.TypeTextfield()
        elif 'dropdown' == gui_object.type:
            self.action = entry_type.TypeDropdown()
        elif 'spinbox' == gui_object.type:
            self.action = entry_type.TypeSpinbox()
        else:
            raise NotImplementedError(f"The argument: {gui_object.json_object['type']} "
                                      "is not accepted! \nOnly type "
                                      "textfield/checkbox/datefield/email/dropdown/spinbox/ "
                                      "allowed!")
        return self

    def create(self):
        return self.action.create()

    def validate(self, gui_object):
        return self.action.validate(gui_object)
