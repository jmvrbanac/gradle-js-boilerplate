#!/usr/bin/python
import subprocess
import argparse
import sys
import os

args = None

def run():
    rhino_process = subprocess.Popen(["java", "-jar", "../tools/rhino/js.jar", "-opt", "-1","../tools/rhino/envjs.bootstrap.js", "../tools/jasmine/ci-testrunner.html"], stdout=subprocess.PIPE)
    all_lines = rhino_process.stdout.readlines()

    runner_finished = False
    for console_output_line in all_lines:
        final_number_of_failures = -1
        output = console_output_line.rstrip()

        if console_output_line.find("Runner Finished") >= 0:
            runner_finished = True
        elif runner_finished and console_output_line.find("failure") >= 0:
            final_number_of_failures = int(output.split(", ")[1].split(" ")[0])

        # Color output for messages
        if final_number_of_failures == -1 and output.lower().find("fail") >= 0 or output.find("error") >=0:
            output = "\033[91m" + output + "\033[0m"
        elif output.lower().find("passed") >= 0:
            output = "\033[92m" + output + "\033[0m"
        elif runner_finished:
            output = "\033[94m" + output + "\033[0m"

        print(output)

        if final_number_of_failures > 0:
            sys.exit(1)

def parse_args():
    parser = argparse.ArgumentParser(description='Continous Integration Layer for running Jasmine through RhinoJS.')
    parser.add_argument("runner", help="Path to Jasmine html spec runner.")
    parser.add_argument("-r", "--rhino", default="../rhino/js.jar", help="Path to RhinoJS's js.jar file")
    parser.add_argument("-b", "--envjs-bootstrap", default="../rhino/envjs.bootstrap.js", help="Path to EnvJS bootstrap file.")
    parser.add_argument("-j", "--java", default="java", help="Path to Java executable.")

    args = parser.parse_args()

if __name__ == "__main__":
    parse_args()
    run()