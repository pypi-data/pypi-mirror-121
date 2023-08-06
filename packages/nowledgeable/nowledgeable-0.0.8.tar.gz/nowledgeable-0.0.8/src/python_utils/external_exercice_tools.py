import os
import sys
import yaml
import time

import errno
import uuid
import json
import base64
import mimetypes
import io
import re
import ctypes
import locale

import subprocess

from PIL import Image
from PIL import ImageChops
from PIL import ImageStat

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from PythonRunner import OneFilePythonRunner

correct_file_extensions = [
    ".py", ".ipynb"
]

def run_checks(yaml_path):

    """ 
    loads a yaml exercice path and make run the exercice corrections 


    Todo : hash check
    """
    exercice_data = load_yaml(yaml_path)

    language = exercice_data['language']
    main_file = exercice_data['testMainFile']
    
    if main_file.endswith(".ipynb"):
        return check_notebok(yaml_path, exercice_data)
    else:
        return check_exercice(yaml_path, exercice_data)


def pretty_print_output(output):

    if output['status'] != 0:
        print(output['stderr'])
        return

    print( "right" if output['isRight'] else  "wrong")

    for assesment, i in enumerate(output['assesments']):

        print("--- Test n° {} ---".format(i))

        print(assesment['isRight'])
    

def check_exercice(yaml_path, exercice_data):
    
    runner = get_runner(exercice_data)

    output = runner.run_external_check(yaml_path, exercice_data)
    pretty_print_output(output)
    return output

def get_language():

    if os.name != 'posix':
        windll = ctypes.windll.kernel32
        lang = locale.windows_locale[windll.GetUserDefaultUILanguage()]
    else:
        lang = os.environ['LANG']

    return lang

def abs_path(path):
    return path if os.path.isabs(path) else os.path.join(os.getcwd(), path)


def invalid_metadata_error(abs_submission_path, submission_path):

    print("""Error: File '{}' does not exist. 
            Make sure you have not deleted the default 
            exercice file or create a new file '{}'""".format(
            abs_submission_path, submission_path))
    print(e)
    exit(1)



def get_runner(exercice_data):

    print('temporary hardcode')

    return OneFilePythonRunner()



def yaml_param_check(abs_yaml_path, all_params, param):
        if param not in all_params:
            raise Exception(
                "Error: '{}' is not defined in YAML exercice settings file! ({})".format(param, abs_yaml_path))
        return True


def check_hash(params):
    print('todo')
    if False:
        raise Exception('do not modify internal files, you cheater')

def load_yaml(yaml_path):
   
    """# Relative to nowledgeable.py
    abs_yaml_path = os.path.join(os.path.dirname(__file__), yaml_path)"""

    # Relative to CWD
    abs_yaml_path = os.path.join(os.getcwd(), yaml_path)

    try:
        yaml_file = open(abs_yaml_path)
    except IOError as e:
        print("Error: Exercice YAML ({}) doesn't exist.".format(abs_yaml_path))
        print(e)
        exit(1)

    try:
        params = yaml.load(yaml_file, Loader=yaml.Loader)
    except yaml.YAMLError as e:
        print("Error: Exercice YAML ({}) is wrongly formatted.".format(abs_yaml_path))
        print(e)
        exit(1)

    yaml_file.close()


    yaml_param_check(abs_yaml_path, params, "userId")
    yaml_param_check(abs_yaml_path, params, "exerciceId")
    yaml_param_check(abs_yaml_path, params, "testMainFile")
    yaml_param_check(abs_yaml_path, params, "testCommand")
    check_hash(params)


    main_file = os.path.join(os.path.dirname(abs_yaml_path), params["testMainFile"])
    
    return params




class ModifiedFileHandlerTester(FileSystemEventHandler):
    def __init__(self, filename, yaml_path, min_interval):
        super().__init__()
        self.filename = filename
        self.yaml_path = yaml_path
        self.min_interval = min_interval
        self.last_event = self.current_milli_time()

    def current_milli_time(self):
        return round(time.time() * 1000)

    def on_modified(self, event):
        event_time = self.current_milli_time()
        if not event.is_directory and event.src_path.endswith(self.filename) and event_time-self.last_event > self.min_interval:
            print("{} ms".format(event_time-self.last_event))
            self.last_event = event_time
            output = runChecks(self.yaml_path)
            print(output)


def watch_test(yaml_path):

    exercice_params = load_yaml(yaml_path)

    abs_submission_path = abs_path(submission_path)

    event_handler = ModifiedFileHandlerTester(submission_path, yaml_path, 500)
    observer = Observer()
    observer.schedule(event_handler, path=abs_submission_path, recursive=False)

    try:
        observer.start()
    except OSError as e:
        print("Error: File '{}' does not exist. Make sure you have not deleted the default exercice file or create a new file '{}'".format(
            abs_submission_path, submission_path))
        print(e)
        exit(1)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()