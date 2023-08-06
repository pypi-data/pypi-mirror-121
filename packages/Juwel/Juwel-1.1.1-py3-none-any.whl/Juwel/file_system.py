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
import os, tempfile, subprocess, sys, glob


class FileSystem:
    def execute_scripts(self, json_object):
        timeout = True
        for item in sys.argv:
            if "false" == item.lower():
                timeout = False
            elif "true" == item.lower():
                timeout = True
        for key, value in json_object.items():
            if 'execute' in value and value['execute']:
                script = value['execute']
                if timeout:
                    print(f"Info: Script {script} started.")
                    print("Timeout in 30 Seconds!")
                    subprocess.run(['sh', script], timeout=30, check=True)
                else:
                    print(f"Info: Script {script} started.")
                    print("Timeout deactivated")
                    subprocess.run(['sh', script], check=True)
                print(f"Script {script} done")

    def exist_file(self, path):
        if os.path.isfile(path):
            return True
        else:
            return False

    def exist_dir(self, path):
        if os.path.isdir(path):
            return True
        else:
            return False

    def get_dir_cwd(self):
        return os.getcwd()

    def read_file(self, path):
        with open(path, "r") as file_reader:
            return file_reader.read().strip()

    def get_temp_path(self):
        return tempfile.gettempdir()

    def get_latest_file(self, path):
        list_of_files = glob.glob(path)
        for item in list_of_files:
            if item.split(".")[-1] == "meta":
                list_of_files.remove(item)
        return max(list_of_files, key=os.path.getctime)

    def get_package_path(self):
        return os.path.dirname(os.path.realpath(__file__))

    def save_file(self, file_object, path):
        with open(path, "w") as conf:
            conf.write(file_object)

    def read_geometry(self):
        path = self.get_package_path()+"/display_size.config"
        if os.path.isfile(path):
            with open(path, "r") as conf:
                return conf.read()
        else:
            return '400x400'
