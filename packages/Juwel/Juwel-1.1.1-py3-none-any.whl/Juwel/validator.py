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
import re

from Juwel import entry_type


class Validator:
    @staticmethod
    def validate_email(email):
        if not re.match(r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])''', email.lower()):
            return False
        else:
            return True

    @staticmethod
    def validate_integer(input):
        if isinstance(input, (int, float)):
            return True
        elif isinstance(input, str) and input.isnumeric():
            return True
        else:
            try:
                float(input)
                return True
            except ValueError:
                return False

    @staticmethod
    def validate_regex(regex, input):
        if not re.match(regex, input):
            return False
        else:
            return True

    @staticmethod
    def isEmpty(input):
        if isinstance(input, str):
            if input and input.strip():
                return True
            else:
                return False
        else:
            raise NotImplementedError("Unexcpected non String in isEmpty")

    @staticmethod
    def get_regex(json_object):
        if 'regex' in json_object:
            return json_object['regex']
        else:
            return None

    @staticmethod
    def is_required(json_object):
        if 'required_field' in json_object:
            if json_object['required_field']:
                return True
        return False

    @staticmethod
    def validate(gui_object):
        action = entry_type.TypeFactory().validate_init(gui_object)
        return action.validate(gui_object)
