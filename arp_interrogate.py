#!/usr/bin/python -tt
# Project: pandas_neteng
# Filename: arp_interrogate
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "2019-12-24"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

import argparse
import os
import basic_textfsm
import real_pandas
import pandas as pd
import numpy as np
import IPython

def print_header(q):
    print(f"\n\n")
    print("-"*60)
    print(f"-- {q}")
    print("-"*60)

def arp_intr_main(template_file, output_file, verbose, filename, save, comparison, interactive):

    # Example of executing entire basic_textfsm script
    basic_textfsm.main(template_file, output_file, verbose, filename, save, interactive)

    # Executing textfsm strainer function only to get data
    strained, strainer = basic_textfsm.textfsm_strainer(template_file, output_file, debug=False)

    # strained holds the parsed data
    # print(strained)

    # strainer holds the regular expression or pattern used to parse the data
    # print(strainer)

    df = pd.DataFrame(strained)
    print_header("Q: Show all the data in the Data Frame without any column information")
    print(df)

    # Examples of queries without any column names
    df[df[5] == 'Vlan101']

    len(df[df[5] == 'Vlan1'])

    df[df[1].str.contains('10.1.10.')]

    df[~df[1].str.contains('10.1.10.')]

    ######## WITH COLUMN NAMES
    # Dont like to have to refer to the columns by their number
    # so lets re load the Data Frame and give it the column names from the textFSM header

    df = pd.DataFrame(strained, columns=strainer.header)

    # Now we have a Data Frame with Column Headers

    print_header("Q: Show all the data in the Data Frame with meaningful column HEADERS")
    print(df)

    print_header("Q: What are all the IPs in Vlan1?")
    # Print the filtered data frame
    print(f"The Data Frame: \n {df[df['INTERFACE'] == 'Vlan1']}")
    # Save the filtered data frame for only the ADDRESS column and extract the values of each IP
    v1 = df['ADDRESS'].loc[df['INTERFACE'] == 'Vlan1'].values
    print(f"The IP Values: \n{v1}")

    ##  The old Way

    if comparison:

        print("\n\t*** COMPARISON ***")
        print("\tUsing PANDAS...")
        print(f"\t{v1}")

        # Using Python Only
        print("\n\tUsing Python only..")
        vlan1ips = []
        for line in strained:
            if line[5] == 'Vlan1':
                vlan1ips.append(line[1])
        print(f"\t{vlan1ips}")


        # Using list comprehension
        print(f"\n\tUsing Python List Comprehension...")
        vlan1ips_lc = [line[1] for line in strained if line[5] == 'Vlan1' ]

        print(f"\tUsing List Comprehension: \n\t{vlan1ips_lc}\n")


    print_header("Q: What are all the IPs in Vlan101?")
    print(df[df['INTERFACE'] == 'Vlan101'])

    print_header("Q: How many IPs are in Vlan1?")
    print(len(df[df['INTERFACE'] == 'Vlan1']))

    print_header("Q: What is all the APR information for the MAC ending in 421c")
    row_info = df.loc[df['MAC'].str.contains('421c', na=False)]
    print(row_info)

    print_header("Q: What is the IP of the MAC ending in 421c")
    # Turn into a string
    ip = df['ADDRESS'].loc[df['MAC'].str.contains('421c', na=False)].values[0]
    print(f"\t{ip}")
    print(f"\tThe ip of MAC ADDRESS {df['MAC'].loc[df['MAC'].str.contains('421c', na=False)].values[0]}"
          f"is {ip}")

    print_header("Q: What IPs have the first three octets of 10.1.10. and how many are there?")
    # Using loc is apparently a more predictable approach and in case a data set has NaN "Not a Number" values in
    # the Pandas Data Frame set na=False ot ignore
    slist = df.loc[df['ADDRESS'].str.contains('10.1.10.', na=False)]
    quant = len(slist)

    print(slist)
    print(f"----------\nTotal: \t{quant}")
    # Drop into an interactive iPython shell to continue playing with the data

    print_header("Q: What is the MAC Vendor (OUI) information for each MAC Address? (show MAC, IP, and OUI)")
    df['OUI'] = df['MAC'].map(real_pandas.get_oui_macvendors)
    print(df[['MAC', 'ADDRESS','OUI']])

    ################ END #################
    # Drop into iPython if the -i opiton was provided when the script was called
    # (pandas) Claudias-iMac:pandas_neteng claudia$ python arp_interrogate.py -i
    #
    if arguments.interactive:
        IPython.embed()




# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python arp_interrogate.py  Will run with default data in the "
                                            "repository' ")
    defa_template = "cisco_ios_show_ip_arp.textfsm"
    arg_defa_fn = os.path.join(".","tfsm_templates", defa_template)
    parser.add_argument('-t', '--template_file', help=" TextFSM Template File ", default=arg_defa_fn)

    defa_show = "weddell-sw01.uwaco.com-arp.txt"
    arg_defa_show_fn = os.path.join(".","txt_data", defa_show)
    parser.add_argument('-o', '--output_file', help='Full path to file with show command show ip arp output',
                        default=arg_defa_show_fn)

    parser.add_argument('-v', '--verbose',
                        help='Enable all of the extra print statements used to investigate the results ',
                        action='store_true', default=False)

    defa_out = defa_template.split(".")[0]
    parser.add_argument('-f', '--filename', help='Resulting device data parsed output file name suffix',
                        action='store', type=str, default=defa_out)

    parser.add_argument('-s', '--save', help='Save Parsed output in TXT, JSON, YAML, and CSV Formats',
                        action='store_true', default=False)

    parser.add_argument('-i', '--interactive', help='Drop into iPython', action='store_true', default=False)

    parser.add_argument('-c', '--comparison', help='Show Comparison', action='store_true', default=False)

    arguments = parser.parse_args()

    arp_intr_main(template_file=arguments.template_file, output_file=arguments.output_file,
                  verbose=arguments.verbose, filename=arguments.filename, save=arguments.save,
                  interactive=arguments.interactive, comparison=arguments.comparison)
