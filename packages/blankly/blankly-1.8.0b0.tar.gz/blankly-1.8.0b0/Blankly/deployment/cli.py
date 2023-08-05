"""
    CLI for interacting with and uploading blankly models.
    Copyright (C) 2021  Emerson Dove

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import sys
import warnings
import os
import platform
import runpy
import time
import requests
import json
import zipfile
import tempfile

from blankly.deployment.api import API
from blankly.utils.utils import load_json_file


very_important_string = """
██████╗ ██╗      █████╗ ███╗   ██╗██╗  ██╗██╗  ██╗   ██╗    ███████╗██╗███╗   ██╗ █████╗ ███╗   ██╗ ██████╗███████╗
██╔══██╗██║     ██╔══██╗████╗  ██║██║ ██╔╝██║  ╚██╗ ██╔╝    ██╔════╝██║████╗  ██║██╔══██╗████╗  ██║██╔════╝██╔════╝
██████╔╝██║     ███████║██╔██╗ ██║█████╔╝ ██║   ╚████╔╝     █████╗  ██║██╔██╗ ██║███████║██╔██╗ ██║██║     █████╗  
██╔══██╗██║     ██╔══██║██║╚██╗██║██╔═██╗ ██║    ╚██╔╝      ██╔══╝  ██║██║╚██╗██║██╔══██║██║╚██╗██║██║     ██╔══╝  
██████╔╝███████╗██║  ██║██║ ╚████║██║  ██╗███████╗██║       ██║     ██║██║ ╚████║██║  ██║██║ ╚████║╚██████╗███████╗
╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝       ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝
"""


def add_path_arg(arg_parser):
    arg_parser.add_argument('path',
                            metavar='path',
                            type=str,
                            help='Path to the directory containing the blankly enabled folder.')


def create_and_write_file(filename: str, default_contents: str = None):
    try:
        file = open("./" + filename, 'x+')
        if default_contents is not None:
            file.write(default_contents)
    except FileExistsError:
        print("Already exists - skipping...")


parser = argparse.ArgumentParser(description='Blankly CLI & deployment tool.')


subparsers = parser.add_subparsers(help='Different blankly commands.')

init_parser = subparsers.add_parser('init', help='Sub command to create a blankly-enabled development environment.')
init_parser.set_defaults(which='init')

login_parser = subparsers.add_parser('login', help='Log in to your blankly account.')
login_parser.set_defaults(which='login')

deploy_parser = subparsers.add_parser('deploy', help='Sub command to deploy the model.')
deploy_parser.set_defaults(which='deploy')

add_path_arg(deploy_parser)

run_parser = subparsers.add_parser('run', help='Mimic the run mechanism used in blankly deployment.')
run_parser.add_argument('--monitor',
                        action='store_true',
                        help='Add this flag to monitor the blankly process to understand CPU & memory usage. '
                             'The module psutil must be installed.')
run_parser.set_defaults(which='run')

add_path_arg(run_parser)


def zipdir(path, ziph, ignore_files: list):
    # From https://stackoverflow.com/a/1855118/8087739
    # Notice we're using this instead of shutil because it allows customization such as passwords and skipping
    # directories
    # ziph is zipfile handle

    # Set all the ignored files to be absolute
    for i in range(len(ignore_files)):
        ignore_files[i] = os.path.abspath(ignore_files[i])

    for root, dirs, files in os.walk(path, topdown=True):
        for file in files:
            # (Modification) Skip everything that is in the blankly_dist folder
            filepath = os.path.join(root, file)

            if not os.path.abspath(filepath) in ignore_files:
                # This takes of the first part of the relative path and replaces it with /model/
                relpath = os.path.relpath(filepath,
                                          os.path.join(path, '..'))
                relpath = os.path.normpath(relpath).split(os.sep)
                relpath[0] = os.sep + 'model'
                relpath = os.path.join(*relpath)

                ziph.write(filepath, relpath)
            else:
                print('Skipping:', file, 'in folder', root)


def main():
    args = vars(parser.parse_args())
    try:
        which = args['which']
    except KeyError:
        parser.print_help()
        return
    if which == 'deploy':
        if args['path'] is None:
            deploy_parser.print_help()
            return
        else:
            api = API()

            try:
                f = open(os.path.join(args['path'], 'blankly.json'))
                deployment_options = json.load(f)
            except FileNotFoundError:
                raise FileNotFoundError("A blankly.json file must be present at the top level of the directory "
                                        "specified.")

            print("Zipping...")

            with tempfile.TemporaryDirectory() as dist_directory:
                print(dist_directory)
                source = os.path.abspath(args['path'])

                model_path = os.path.join(dist_directory, 'model.zip')
                zip_ = zipfile.ZipFile(model_path, 'w', zipfile.ZIP_DEFLATED)
                zipdir(source, zip_, deployment_options['ignore_files'])

                zip_.close()

                time.sleep(25)

                print("Uploading...")
                print(api.upload(model_path, project_id='u4PB0Adpb4XAYd33qsH1', model_id='Fb0D0me8ubzVT7L75dO5'))

    elif which == 'init':
        print("Initializing...")
        print(very_important_string)

        # Directly download keys.json
        print("Downloading keys template...")
        keys_example = requests.get('https://raw.githubusercontent.com/Blankly-Finance/'
                                    'Blankly/main/examples/keys_example.json')
        create_and_write_file('keys.json', keys_example.text)

        # Directly download settings.json
        print("Downloading settings defaults...")
        settings = requests.get('https://raw.githubusercontent.com/Blankly-Finance/Blankly/main/examples/settings.json')
        create_and_write_file('settings.json', settings.text)

        # Directly download backtest.json
        print("Downloading backtest defaults...")
        backtest = requests.get('https://raw.githubusercontent.com/Blankly-Finance/Blankly/main/examples/backtest.json')
        create_and_write_file('backtest.json', backtest.text)

        # Directly download an rsi bot
        print("Downloading RSI bot example...")
        bot = requests.get('https://raw.githubusercontent.com/Blankly-Finance/Blankly/main/examples/rsi.py')
        create_and_write_file('bot.py', bot.text)

        print("Writing deployment defaults...")
        # Interpret defaults and write to this folder
        py_version = platform.python_version_tuple()
        deploy = {
            "main_script": "./bot.py",
            "python_version": py_version[0] + "." + py_version[1],
            "requirements": "./requirements.txt",
            "working_directory": ".",
            "ignore_files": ['']
        }
        create_and_write_file('blankly.json', json.dumps(deploy, indent=2))

        # Write in a blank requirements file
        print("Writing requirements.txt defaults...")
        create_and_write_file('requirements.txt', 'blankly')

        print("Done!")

    elif which == 'login':
        from http.server import BaseHTTPRequestHandler, HTTPServer

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                content_len = int(self.headers.get('Content-Length'))
                post_body = self.rfile.read(content_len).decode('ascii')
                token: str = json.loads(post_body)['token']

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()

                message = "Success"
                self.wfile.write(bytes(message, "utf8"))

        server = HTTPServer(('', 8080), Handler)

        server.handle_request()

    elif which == 'run':
        if args['path'] is None:
            run_parser.print_help()
        else:
            current_directory = os.getcwd()
            blankly_folder = os.path.join(current_directory, args['path'])
            deployment_location = os.path.join(blankly_folder, 'deploy.json')
            try:
                # Find where the user specified their working directory and migrate to that
                deployment_dict = load_json_file(deployment_location)
            except FileNotFoundError:
                raise FileNotFoundError(f"Deployment json not found in location {deployment_location}.")

            # Set the working directory to match the deployment dictionary
            os.chdir(os.path.join(blankly_folder, deployment_dict['working_directory']))

            current_version = platform.python_version_tuple()
            current_version = current_version[0] + "." + current_version[1]

            if current_version != str(deployment_dict['python_version']):
                warn_string = f"Specified python version different than current interpreter. Using version " \
                              f"{platform.python_version()}. The specified version will be followed on full" \
                              f" deployment."
                warnings.warn(warn_string)

            if 'requirements' in deployment_dict and deployment_dict['requirements'] is not None:
                warning_string = "Requirements specified but not installed in this test script. Install " \
                                 "manually if needed."
                warnings.warn(warning_string)

            sys.path.append(blankly_folder)

            # The execute function to run the modules
            main_script_abs = os.path.abspath(deployment_dict['main_script'])
            runpy.run_path(main_script_abs, {}, "__main__")

            if args['monitor']:
                try:
                    import psutil
                except ImportError:
                    raise ImportError("Must install psutil (pip install psutil) to monitor "
                                      "the Blankly process")
                print("Process must be killed to halt monitoring.")

                pid = os.getpid()
                process = psutil.Process(pid)
                while True:
                    monitor_string = "\rCPU Usage: "
                    monitor_string += str(process.cpu_percent())
                    monitor_string += " | "
                    monitor_string += "Memory Usage: "
                    monitor_string += str(process.memory_percent())
                    sys.stdout.write(monitor_string)
                    sys.stdout.flush()
                    time.sleep(5)


if __name__ == "__main__":
    main()
