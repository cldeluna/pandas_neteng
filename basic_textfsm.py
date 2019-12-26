#!/usr/bin/python -tt
# Project: Dropbox (Indigo Wire Networks)
# Filename: textfsm.py
# claudia
# PyCharm

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "2019-04-12"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse
import textfsm
import csv
import json
import yaml
import os




def textfsm_strainer(template_fil, data, debug=False):
    """
    Standard TextFSM Parser function given a textfms template file and a data file

    :param template_fil: TextFSM Template to use
    :param data:  Data File to parse
    :param debug:  Bool to enable or disable diagnostic printing
    :return: the list of results (strained) and the FSM result object (strainer)
    """

    strained = ''

    # Open the template file, and initialise a new TextFSM object with it.
    with open(template_fil) as template_fil_fh:
        strainer = textfsm.TextFSM(template_fil_fh)

    # Read stdin until EOF, then pass this to the FSM for parsing.
    with open(data) as data_fh:
        input_data = data_fh.read()

    strained = strainer.ParseText(input_data)

    return strained, strainer


def main(template_file, output_file, verbose, filename, save, interactive):

    fsm_results, fsm_object = textfsm_strainer(template_file,output_file)

    if verbose:
        print("\nTextFSM Template Methods:")
        print(dir(fsm_object))
        print(f"\nFSM Values: \n\t{fsm_object.values}")
        print(f"\nFSM States: \n\t{fsm_object.states.keys()}")
        print(f"\nFSM States Full: \n\t{fsm_object.states}")
        print(f"\nFSM Value MAP:")
        for k,v in fsm_object.value_map.items():
            print(f"\tKey: {k} \tValue: {v}")

        print(f"\nTextFSM results variable is of type {type(fsm_results)} and has standard list Methods:")
        print(dir(fsm_results))

        print(f'\n\nTextFSM Results Header:\n{fsm_object.header}')
        print("="*60)
        print(f"Results is of type {type(fsm_results)} and Length {len(fsm_results)} with Rows:\n")
        for row in fsm_results:
            print(f"{row}")
        print("="*60)
        print("\n")

    if save:

        # Save to Text File
        filename = f"{filename}.txt"
        fn = os.path.join(".", "output", filename)
        with open(fn, 'w') as out_fh:
            out_fh.write(f"{fsm_object.header}\n")
            [out_fh.write(f"{line}\n") for line in fsm_results]
        print(f"Saved parsed data as Text to file: \t{fn}\n")

        # Save to JSON File
        filename = f"{filename}.json"
        fn = os.path.join(".", "output", filename)
        _ = []
        for line in fsm_results:
            _.append(dict(zip(fsm_object.header, line)))
        with open(fn, 'w') as out_fh:
            json.dump(_, out_fh)
        print(f"Saved parsed data as JSON to file: \t{fn}\n")

        # Save to YAML
        filename = f"{filename}.yml"
        fn = os.path.join(".", "output", filename)
        with open(fn, 'w') as out_fh:
            yaml.dump(_, out_fh)
        print(f"Saved parsed data as YAML to file: \t{fn}\n")

        # Save to CSV File
        filename = f"{filename}.csv"
        fn = os.path.join(".", "output", filename)
        fsm_results.insert(0, fsm_object.header)
        with open(fn, 'w') as out_fh:
            csv_fh = csv.writer(out_fh)
            csv_fh.writerows(fsm_results)
        print(f"Saved parsed data as CSV to file: \t{fn}\n")


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This script applys a textfsm template to a text file of unstructured data (often show commands).  The resulting structured data is saved as text (output.txt) and CSV (output.csv).",
                                     epilog="Usage: ' python textfsm.py <template file> <show output file>' ")

    parser.add_argument('template_file', help=" TextFSM Template File ")
    parser.add_argument('output_file', help=' Device data (show command) output')
    parser.add_argument('-v', '--verbose', help='Enable all of the extra print statements used to investigate the results ', action='store_true', default=False)
    parser.add_argument('-f', '--filename', help='New filename to override the standard "output.x" filename used by default', action='store', type=str, default='output')
    parser.add_argument('-s', '--save', help='Save Parsed output in TXT, JSON, YAML, and CSV Formats', action='store_true', default=False)
    parser.add_argument('-i', '--interactive', help='Drop into iPython', action='store_true', default=False)


    arguments = parser.parse_args()
    # print(arguments)
    main(template_file=arguments.template_file, output_file=arguments.output_file, verbose=arguments.verbose,
         filename=arguments.filename, save=arguments.save, interactive=arguments.interactive)
