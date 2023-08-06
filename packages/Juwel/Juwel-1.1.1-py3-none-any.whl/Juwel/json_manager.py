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
import json
import os.path

from Juwel.file_system import FileSystem


class JsonManager:
    def read_json(self, file=None):
        fs = FileSystem()
        datatype_path = fs.get_package_path()+"/config/config.selection.json"
        if not fs.exist_file(datatype_path):
            raise FileNotFoundError("Config datatype file not found!")
        datatype = fs.read_file(datatype_path)
        try:
            json_datatype = json.loads(datatype)
        except json.JSONDecodeError as ex:
            raise RuntimeError("Datatype file seems to be malformed: ", ex)

        if file is None:
            latest_file = fs.get_latest_file(fs.get_dir_cwd() + "/*")
            base_latest_file = os.path.basename(latest_file)
            path = self._get_config(json_datatype, os.path.splitext(base_latest_file)[1][1:])
        elif file == ".":
            path = fs.get_package_path()+"/config/config.folder.json"
        elif file:
            path = self._get_config(json_datatype, os.path.splitext(file)[1][1:])
        else:
            raise NotImplementedError("Couldnt decide which config to load")

        if not fs.exist_file(path):
            raise FileNotFoundError(path, ' not found')
        else:
            json_string = fs.read_file(path)
            try:
                json_object = json.loads(json_string)
            except (json.JSONDecodeError, Exception) as ex:
                raise RuntimeError("Config file seems to be malformed: ", ex)
        return json_object

    @staticmethod
    def _get_config(json_datatype, dir_type):
        fs = FileSystem()
        for key, value in json_datatype.items():
            if dir_type in value:
                return fs.get_package_path()+f"/config/config.{key}.json"
        return fs.get_package_path()+"/config/config.default.json"

    @staticmethod
    def write_json(gui_list, path):
        json_object = dict()
        fs = FileSystem()

        if len(gui_list) < 1:
            raise ValueError("No Values to print")
        if fs.exist_file(path):
            raise FileExistsError(path, ' already exist')

        for items in gui_list:
            val = None
            if items.type in ['dropdown', 'email', 'textfield']:
                val = items.variable.get()
            elif items.type == 'datefield':
                val = items.content.get_date()
            elif items.type == 'spinbox':
                val = items.content.get()
            elif items.type == 'checkbox':
                single_answer = True
                if 'single_answer' in items.json_object:
                    single_answer = items.json_object['single_answer']
                if single_answer:
                    pos = items.variable.get()
                    value = items.json_object['value']
                    if isinstance(value, list):
                        val = value[pos]
                else:
                    val = dict()
                    value = items.json_object['value']
                    i = 0
                    for item in value:
                        val[item] = bool(items.variable[i].get())
                        i += 1
            else:
                raise NotImplementedError(f'Unknown type {items.type}! \nOnly type '
                                          'textfield/checkbox/datefield/email/dropdown/spinbox/ '
                                          'allowed!')

            if items.key is None or items.key == "" or val is None:
                raise ValueError("Key or Value is None")
            json_object[items.key] = val

        if len(json_object) != len(gui_list):
            raise ValueError(f"Json is {len(json_object)} long but {len(gui_list)} is expected!")

        try:
            fs.save_file(json.dumps(json_object, indent=2), path)
        except OSError as ex:
            raise OSError("File not saved \n", ex)
