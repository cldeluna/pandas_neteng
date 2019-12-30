#!/usr/bin/python -tt
# Project: pandas_neteng
# Filename: arp_interrogate
# claudia
# PyCharm

# from __future__ import absolute_import, division, print_function

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

    """
    Simple formatting function to print the question text
    :param q: Question
    :return:  This function does not return any value
    """
    print(f"\n\n")
    print("-"*60)
    print(f"-- {q}")
    print("-"*60)


def arp_intr_main(template_file, output_file, verbose, filename, save, comparison, interactive):
    """
    REPL Script for ARP analysis in Pandas

    :param template_file: TextFSM Template file for show ip apr
    :param output_file:  show command output file for a device
    :param verbose: Flag to print out additional commands from the basic_textfsm script
    :param filename: File name suffix to use for the parsed output files
    :param save: Flag to save parsed output
    :param comparison: Flag to print some comparisons
    :param interactive: Flag to drop into iPython after script run completes

    """


    # Example of executing entire basic_textfsm script
    basic_textfsm.main(template_file, output_file, verbose, filename, save, interactive)

    # Executing textfsm strainer function only to get data
    strained, strainer = basic_textfsm.textfsm_strainer(template_file, output_file, debug=False)

    # strained holds the parsed data
    # print(strained)

    # strainer holds the regular expression or pattern used to parse the data
    # print(strainer)


    ###### QUESTION
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

    ###### QUESTION
    print_header("Q: Show all the data in the Data Frame with meaningful column HEADERS")
    print(df)

    ###### QUESTION
    print_header("Q: What are all the IPs in Vlan1?")
    # Print the filtered data frame
    print(f"The Data Frame: \n {df[df['INTERFACE'] == 'Vlan1']}")

    # Save the filtered data frame for only the ADDRESS column extracting the values of each IP only for Vlan1
    # In [2]: type(pandas_vlan1ips)
    # Out [2]: numpy.ndarray
    pandas_vlan1ips = df['ADDRESS'].loc[df['INTERFACE'] == 'Vlan1'].values

    # Getting the IP list with the .to_list() method
    # In [4]: type(pandas_vlan1ips)
    # Out[4]: list
    pandas_vlan1ips = df['ADDRESS'].loc[df['INTERFACE'] == 'Vlan1'].to_list()
    print(f"The IP Values in a list: \n{pandas_vlan1ips}")


    ###### QUESTION
    print_header("Q: Can I build a dictionary of IP and MACs where the key is the IP and the value is the MAC?")

    # dictionary of dictionaries where the key is the index (row) and the value
    # is a dict with keys of ADDRESS and MAC
    vlan1ipmac_dict = df[['ADDRESS', 'MAC']].to_dict(orient='index')

    # list of dictionaries  ***  This is what you want
    # dict with keys of ADDRESS and MAC
    vlan1ipmac_ldict = df[['ADDRESS', 'MAC']].to_dict(orient='records')
    print(f"List of dictionaries, each with Key/Value of IP/Mac..."
          f"\n{vlan1ipmac_ldict}")

    ##
    """
    https://www.geeksforgeeks.org/python-pandas-dataframe-to_dict/
    
    orient: String value, (‘dict’, ‘list’, ‘series’, ‘split’, ‘records’, ‘index’) 
    Defines which dtype to convert Columns(series into). For example, 
    ‘list’ would return a dictionary of lists with Key=Column name and Value=List 
    (Converted series).

    In[28]: vlan1ipmac_dict = df[['ADDRESS', 'MAC']].to_dict(orient='split')

    In[29]: vlan1ipmac_dict
    Out[29]:
    {'index': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
     'columns': ['ADDRESS', 'MAC'],
     'data': [['10.1.10.1', '28c6.8ee1.659b'],
              ['10.1.10.11', '6400.6a64.f5ca'],
              ['10.1.10.10', '0018.7149.5160'],
              ['10.1.10.21', 'a860.b603.421c'],
              ['10.1.10.37', 'a4c3.f047.4528'],
              ['10.10.101.1', '0018.b9b5.93c2'],
              ['10.10.100.1', '0018.b9b5.93c1'],
              ['10.1.10.102', '0018.b9b5.93c0'],
              ['71.103.129.220', '28c6.8ee1.6599'],
              ['10.1.10.170', '000c.294f.a20b'],
              ['10.1.10.181', '000c.298c.d663']]}

    In[30]: vlan1ipmac_dict = df[['ADDRESS', 'MAC']].to_dict(orient='index')

    In[31]: vlan1ipmac_dict
    Out[31]:
    {0: {'ADDRESS': '10.1.10.1', 'MAC': '28c6.8ee1.659b'},
     1: {'ADDRESS': '10.1.10.11', 'MAC': '6400.6a64.f5ca'},
     2: {'ADDRESS': '10.1.10.10', 'MAC': '0018.7149.5160'},
     3: {'ADDRESS': '10.1.10.21', 'MAC': 'a860.b603.421c'},
     4: {'ADDRESS': '10.1.10.37', 'MAC': 'a4c3.f047.4528'},
     5: {'ADDRESS': '10.10.101.1', 'MAC': '0018.b9b5.93c2'},
     6: {'ADDRESS': '10.10.100.1', 'MAC': '0018.b9b5.93c1'},
     7: {'ADDRESS': '10.1.10.102', 'MAC': '0018.b9b5.93c0'},
     8: {'ADDRESS': '71.103.129.220', 'MAC': '28c6.8ee1.6599'},
     9: {'ADDRESS': '10.1.10.170', 'MAC': '000c.294f.a20b'},
     10: {'ADDRESS': '10.1.10.181', 'MAC': '000c.298c.d663'}}

    In[32]:
    
    In [32]: vlan1ipmac_dict = df[['ADDRESS', 'MAC']].to_dict(orient='records')                                                                

    In [33]: vlan1ipmac_dict                                                                                                                   
    Out[33]: 
    [{'ADDRESS': '10.1.10.1', 'MAC': '28c6.8ee1.659b'},
     {'ADDRESS': '10.1.10.11', 'MAC': '6400.6a64.f5ca'},
     {'ADDRESS': '10.1.10.10', 'MAC': '0018.7149.5160'},
     {'ADDRESS': '10.1.10.21', 'MAC': 'a860.b603.421c'},
     {'ADDRESS': '10.1.10.37', 'MAC': 'a4c3.f047.4528'},
     {'ADDRESS': '10.10.101.1', 'MAC': '0018.b9b5.93c2'},
     {'ADDRESS': '10.10.100.1', 'MAC': '0018.b9b5.93c1'},
     {'ADDRESS': '10.1.10.102', 'MAC': '0018.b9b5.93c0'},
     {'ADDRESS': '71.103.129.220', 'MAC': '28c6.8ee1.6599'},
     {'ADDRESS': '10.1.10.170', 'MAC': '000c.294f.a20b'},
     {'ADDRESS': '10.1.10.181', 'MAC': '000c.298c.d663'}]

    
    """

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
        lc_vlan1ips = [line[1] for line in strained if line[5] == 'Vlan1' ]

        print(f"\tUsing List Comprehension: \n\t{lc_vlan1ips}\n")


    ###### QUESTION
    print_header("Q: What are all the IPs in Vlan101?")
    print(df[df['INTERFACE'] == 'Vlan101'])

    ###### QUESTION
    print_header("Q: How many IPs are in Vlan1?")
    print(len(df[df['INTERFACE'] == 'Vlan1']))

    ###### QUESTION
    print_header("Q: What is all the APR information for the MAC ending in 421c")
    row_info = df.loc[df['MAC'].str.contains('421c', na=False)]
    print(row_info)

    ###### QUESTION
    print_header("Q: What is the IP of the MAC ending in 421c")
    # Turn into a string
    ip = df['ADDRESS'].loc[df['MAC'].str.contains('421c', na=False)].values[0]
    print(f"\t{ip}")
    print(f"\tThe ip of MAC ADDRESS {df['MAC'].loc[df['MAC'].str.contains('421c', na=False)].values[0]}"
          f" is {ip}")

    ###### QUESTION
    print_header("Q: What IPs have the first three octets of 10.1.10. and how many are there?")
    # Using loc is apparently a more predictable approach and in case a data set has NaN "Not a Number" values in
    # the Pandas Data Frame set na=False ot ignore
    slist = df.loc[df['ADDRESS'].str.contains('10.1.10.', na=False)]
    quant = len(slist)

    print(slist)
    print(f"----------\nTotal: \t{quant}")

    ###### QUESTION
    print_header("Q: What is the MAC Vendor (OUI) information for each MAC Address? (show MAC, IP ADDRESS, and OUI)")
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
