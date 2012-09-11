#!/usr/bin/python

import argparse
import os
import io

args = None

def generate_script_tag(path):
    result  = "<script src=\""
    result += path
    result += "\"></script>"
    return result

def read_folder(folder_path):
    paths = []
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for filename in files:
            original_name, file_extension = os.path.splitext(filename)
            if file_extension == ".js":
                path_to_process = os.path.join(root, filename)
                path_to_process = os.path.relpath(path_to_process, os.path.dirname(args.runner));
                
                if original_name.startswith("Spec"):
                    paths.append(generate_script_tag(path_to_process))

    print("Including " + str(len(paths)) + " file(s)")
    return paths

def file_list_to_string(file_list):
    list_str = ""
    for file_path in file_list:
        list_str += "  " + file_path + "\n"

    return list_str

def generate_spec_runner(sources, tests, output_path, template_path):
    # Read Template
    template_file = open(template_path, "r")
    template_data = template_file.read()

    # Replace Values
    tests_str   = file_list_to_string(tests)

    template_data = template_data.replace("$TEST_FILES$", tests_str)

    # Write 
    generated_file = open(output_path, "w")
    generated_file.writelines(template_data)

def parse_args():
    parser = argparse.ArgumentParser(description='Builds Jasmine Test Runner HTML file')
    parser.add_argument("specfolder", help="Root path containing spec files.")
    parser.add_argument("runner", help="Path to Jasmine html spec runner.")
    parser.add_argument("template", help="Path to Jasmine html template")

    return parser.parse_args()

def run():  
    # Load In Source Files
    sources = []
    tests   = read_folder(args.specfolder)

    generate_spec_runner(sources, tests, args.runner, args.template)        

if __name__ == "__main__":
    args = parse_args()
    run()