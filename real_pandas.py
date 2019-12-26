#!/usr/bin/python -tt
# Project: pandas
# Filename: real_pandas
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "2019-12-19"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"


import argparse
import pandas as pd
import json
import netaddr
import re
import requests
import time
import pprint
import basic_textfsm
import os
import IPython



def print_type(an_object,print_dir=False):
    """
    Print Value and Print Type
    Handy function to look at a returned object
    :return:
    """

    print("-"*20)
    print(f"Value: \t{an_object}")
    print(f"Type: \t{type(an_object)}")
    print(f"Length: \t{len(an_object)}")
    if print_dir:
        print(f"Dir: \t{dir(an_object)}")
    print("-"*20)


def get_oui(mac):
    """
    This function uses the built in option for lookups
    :param mac:
    :return:
    """

    maco = netaddr.EUI(mac)
    try:
        macf = maco.oui.registration().org
    except netaddr.core.NotRegisteredError:
        macf = "Not available"

    # print("macf is {}".format(macf))
    return macf


# https://macvendors.co/api/python
def get_oui_macvendors(mac, debug=False):
    """
    This function uses the MacVendors API to find information about the MAC
    Organizationally Unique Identifier or OUI
    This lookup provides more information than the get_oui netaddr lookup
    :param mac: MAC in any format
    :return: the companey value of the look up or the "no result" string
    """

    # maco = netaddr.EUI(mac)
    MAC_URL = f"http://macvendors.co/api/{mac}"
    mac_get = requests.get(MAC_URL)

    mac_response_json = json.loads(mac_get.text)

    if debug:
        pprint.pprint(mac_get.json())
        print(dir(mac_get))
        print_type(mac_response_json)

        #print(temp['result'].keys())

    # If the JSON response includes a 'company' key we have Vendor information
    # otherwise return a string indicating the lookup did not return any data
    if 'company' in mac_response_json['result'].keys():

        mac_lookup = mac_response_json['result']['company']

    else:
        mac_lookup = "Query returned no result"

    return mac_lookup

    # https://github.com/coolbho3k/manuf
    # Something else to check out
    # https://www.wireshark.org/tools/oui-lookup.html


def get_int(interface, debug=False):

    """
    Function that parses the interface and returns the last interface number
    For example: Gi1/0/17
    Returns string "17"
    """

    int_only = re.sub(r"^\s*\D{2,3}", "", interface)

    _ = interface.split("/")
    if debug:
        print(int_only)
        print(f"\n\n{_}")
        print(type(_[-1]))

    return _[-1]


def unkn2int(value):

    if re.search(r'/d*', value):
        number_value = int(value)
    else:
        number_value = value
    return(number_value)


def convert(v):
    try:
        return int(v)
    except ValueError:
        return v


def print_section_header(header, separater_number=80):
    """
    Print a section header and separator
    :param header:
    :param separater_number:
    :return:
    """

    print("="*separater_number)
    print(f"===== {header}\n")

###############################################################################################################
###############################################################################################################
def main():

    """
    Trying to understand a Pandas Data Frame and how it can help analyze Mac address table output
    :return:
    """


    # provides a pause after each section - Default is 1 second
    # Use the -p command
    # python real_pandas.py -p 0
    pause_in_seconds = arguments.pause_in_seconds

    # Textfsm parsing using the NTC cisco_ios_show_mac-address-table.template
    # https://github.com/networktocode/ntc-templates

    if arguments.file:
        csv_data_file = arguments.file
    else:
        csv_data_file = os.path.join(".", "txt_data", "weddell-sw01.uwaco.com-readable-show-output_cisco_ios_show_mac-address-table_latests-results.csv")


    print(f"=====  Using data file {csv_data_file}\n")

    # For interactive Shell
    # pd.set_option('display.max_columns', None)
    # pd.options.mode.chained_assignment = None

    # These are the variables pulled by the TextFSM template
    # Cast as category to save memory
    dtypes = {
        'DESTINATION_ADDRESS': "category",
        'TYPE': "category",
        'VLAN': "category",
        'DESTINATION_PORT': "category",
    }

    ###############################################################################################################
    print_section_header(f"\n1. Load the CSV data file {csv_data_file} into a Data Frame df\n")

    # Read CSV file into a Pandas Data Frame
    # index_col is important with False I get the ADDRESS data back into the Data frame
    # with index_col = 0 the ADDRESS column becomes the index

    # First we will read in without any "fine tuning"
    print(f"Read in data from CSV without any options")
    df = pd.read_csv(csv_data_file)
    df_keys = df.keys()
    print_type(f"\nPrinting the data frame df (read executed without any options: \n{df}")
    print_type(f"Printing the data frame keys df.keys(): \n{df_keys}")

    print_type(f"\nPrinting the data frame df row index when index_col=True (default): \n{df.index}")

    print_type(f"Printing the data types : \n{df.dtypes}")
    print_type(f"Printing the data types Memory Usage : \n{df.memory_usage()}")
    # df.memory_usage(index=True)

    time.sleep(pause_in_seconds)

    # Reload data frame data with index_col=False (does not use first column but rather adds sequential index) and
    # does not shift column headings.
    # Without index_col=False, with the MAC data set, the MAC column becomes the index and the Destination address
    # column becomes the TYPE column
    df = pd.read_csv(csv_data_file, index_col=False, dtype=dtypes)
    print_type(f"\nPrinting the data frame df with index_col=False: \n{df}")

    print_type(f"\nPrinting the data frame df row index when index_col=False: \n{df.index}")

    df_keys = df.keys()
    print_type(f"Printing the data frame keys df.keys(): \n{df_keys}")

    print_type(f"Printing the data types : \n{df.dtypes}")
    print_type(f"Printing the data types Memory Usage : \n{df.memory_usage()}")

    # delete a column
    # del df['AGE']


    # Every step has a pause - default is 1 second and can be set to your preferece
    # with the -p <sec> command line option
    time.sleep(pause_in_seconds)

    ###############################################################################################################
    print_section_header(f"\n2. Examine the Column headers, Index (Rows), and data types\n")

    # Tuple with number of rows and columns
    rows, cols = df.shape

    # Print the first (5 by default) rows
    df.head()

    # Print the last (5 by default) rows
    df.tail()

    #Columns
    df_column_keys = df.keys()
    #Rows
    df_rows = df.first_valid_index
    print(df)
    print(df_column_keys)
    print(df_rows)

    # Show index "headings" or row headings with df.index
    print(f"Print df.index: \n{df.index}")

    # Show column headings with df.columns
    print(f"Print df.columns: \n{df.columns}")

    # Show values with df.values
    print(f"Print df.values: \n{df.values}")

    # Rename a column
    # without inplace=True save to another df variable.
    # inplace=True updates the existing Data Frame df
    df.rename(columns={'DESTINATION_ADDRESS': 'MAC'}, inplace=True)

    # Set the index
    # What is the performance impact of non-unique indexes in pandas?
    # https://stackoverflow.com/questions/16626058/what-is-the-performance-impact-of-non-unique-indexes-in-pandas
    #
    # Note that this does not modify df but creates a new Data Frame
    df.set_index('MAC')

    # To modify df use
    df.set_index('MAC', inplace=True)
    # This allows you to use the MAC in df.loc as an index

    # To reset the index
    df.reset_index(inplace=True)

    # Rename a column
    df.rename(columns={'MAC': 'DESTINATION_ADDRESS'}, inplace=True)

    # Note yoy can pass a list to the Data Frame to get selected columns
    only_print = ['DESTINATION_ADDRESS', 'DESTINATION_PORT']
    print(f"Only Print Selected Columns in a list:  {only_print}")
    print(df[only_print])

    time.sleep(pause_in_seconds)

    ###############################################################################################################
    print_section_header(f"3. Use describe on the data frame to get totals and a statistical summary of the data...\n")
    desc = df.describe()
    print_type(desc)

    # Same keys as the data frame
    # print(desc.keys())

    time.sleep(pause_in_seconds)

    ###############################################################################################################
    print_section_header(f"\n4. Iterate through the Pandas Series for MAC Addresses")

    # Here we iterate through one column of the Data Frame (which is a series)
    macs_column = df['DESTINATION_ADDRESS']
    print(f"Type is: {type(macs_column)}")
    print(f"Length of {type(macs_column)} is {len(macs_column)}\n")
    for item in macs_column:
        # print_type(item)
        print(f"MAC: {item} \tVENDOR: {get_oui(item)}")
        # column_entry = df[column]
        # print(column_entry.values)
    time.sleep(pause_in_seconds)

    ###############################################################################################################
    print_section_header(f"\n5. Add a column to the Data Frame for MAC Address OUI/Vendor.\n "
                         f"Note that you do not need to iterate over the data frame!  ")
    print_type(f"Printing the data frame keys df.keys() BEFORE adding VENDOR_CODE column: \n{df.keys()}")
    df['VENDOR_CODE'] = df['DESTINATION_ADDRESS'].map(get_oui_macvendors)
    print_type(f"Printing the data frame keys df.keys() AFTER adding VENDOR_CODE column: \n{df.keys()}")

    time.sleep(pause_in_seconds)

    ###############################################################################################################
    print_section_header(f"\n6. Add a column to the Data Frame for Port number so that we can sort numerically\n")
    df['PORT'] = df['DESTINATION_PORT'].map(get_int)
    print_type(f"Printing the data frame keys df.keys() AFTER adding a PORT column: \n{df.keys()}")

    time.sleep(pause_in_seconds)

    ###############################################################################################################
    print_section_header(f"\n7. Review updated Data Frame\n")

    print_type(f"Printing the FULL updated data frame df: \n{df}")
    print_type(f"Printing the data frame keys df.keys(): \n{df.keys()}")


    desc = df.describe()
    print_type(f"Printing the data frame description: \n{desc}")


    time.sleep(pause_in_seconds)

    ###############################################################################################################
    ####### GROUP BY

    print_section_header(f"\n8. Group by Vendor\n")
    # https://realpython.com/pandas-groupby/

    # Use the groupby method to a list of groups and use .size to get totals for each group.
    group_by_vendor = df.groupby('VENDOR_CODE')
    print_type(group_by_vendor.size())



    # Group by Port and Vendor Code
    pv = df.groupby(['PORT', 'VENDOR_CODE']).size()
    print()

    find_group = "Vmware"

    for item in group_by_vendor:
        print(item)
        print(type(item))

    cols = ['PORT', 'DESTINATION_ADDRESS']
    p = df[df['PORT'] != 'CPU'].groupby(cols)
    print(p)
    print(p.groups)
    print(p.first())

    # Alternative iteration

    for index, row in df.iterrows():
        print(f"INDEX: {index} \nROW: \n{row}\n")
    time.sleep(pause_in_seconds)

    ###############################################################################################################
    ####### INTERFACE MAP

    print_section_header(f"\n9. Filter Data Frame Rows to remove the Static Entries and find specific rowns\n")

    # New Data Frame with just the interfaces
    int_map = df[df['VLAN'] != "All"]
    print_type(int_map)


    # Get MACs associated to one interface
    macs_on_1int = df.loc[df['DESTINATION_PORT'] == 'Fa1/0/17']

    vendor_list = ["VMware"]
    # This gives us a boolean on the rows where the codition is true
    vmacs_on_ints = df["VENDOR_CODE"].isin(vendor_list)



    # Using the logic above in the df provides the actual data
    vmi = df[df["VENDOR_CODE"].isin(vendor_list)]


    time.sleep(pause_in_seconds)

    ###############################################################################################################
    print_section_header(f"\n10. Filter out unnecessary columns \n")
    # pandas.DataFrame([convert(c) for c in l] for l in df.values).sort([0, 1])
    # Data Frame without the Type column - This is the
    int_map_essentials = int_map[['DESTINATION_ADDRESS','VLAN', 'DESTINATION_PORT', 'VENDOR_CODE', 'PORT']]

    time.sleep(pause_in_seconds)

    ###############################################################################################################
    print_section_header(f"\n11. Print filtered data frame (aka indexed), cast column to_numeric so it can be o"
                         f"rdered in the next step \n")
    print(int_map_essentials)

    # https://stackoverflow.com/questions/47914274/pandas-sort-values-does-not-sort-numbers-correctly
    # Using the dot notation may have unexpected results and so is not recommended.
    # Use 'coerce' to force any string to type NaN (Not a Number)
    # int_map_essentials.PORT = pd.to_numeric(int_map_essentials.PORT, errors='coerce')
    int_map_essentials['PORT'] = pd.to_numeric(int_map_essentials['PORT'], errors='coerce')
    # A less ambiguous way using loc
    # int_map_essentials = df.loc[:, 'PORT'] = pd.to_numeric(df['PORT'], errors='coerce')
    # https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas

    time.sleep(pause_in_seconds)

    ###############################################################################################################
    print_section_header(f"\n12. Print the new indexed view of the data frame sorted by port number and \nsave both"
                         f"views as JSON files. \n")
    int_map_sorted = int_map_essentials.sort_values('PORT')
    # int_map_sorted = df.loc[:, 'PORT'].sort_values('PORT')
    print(int_map_sorted)
    # If there was already a column with port number but with some other data as well
    # Use the pd.to_numeric(df['PORT'])

    default_orientation_fn = os.path.join(".","output","int_map_sorted.json")
    records_orientation_fn = os.path.join(".","output","int_map_sorted_orientrecords.json")

    int_map_sorted.to_json(default_orientation_fn)

    int_map_sorted.to_json(records_orientation_fn, orient='records')

    time.sleep(pause_in_seconds)

    ###############################################################################################################
    print_section_header(f"\n13. Find the unique list of Mac Vendor Codes with the unique method \n")
    vc = df['VENDOR_CODE']
    vc_unique = pd.unique(vc)
    print(vc_unique)
    print(f"\n{len(vc_unique)} Unique Vendor Codes:")
    print(f"\nTotal Unique Vendor Codes using .size: {vc_unique.size}")
    for v in vc_unique:
        print(f"\t- {v}")
    print()

    time.sleep(pause_in_seconds)

    print_section_header(f"1\n3A. Find the unique list of Mac Vendor Codes and counts using the value_counts method \n")
    print(df['VENDOR_CODE'].value_counts())
    print()

    time.sleep(pause_in_seconds)

    ###############################################################################################################
    print_section_header(f"\n14. More Indexing \n")

    vendor_code = 'Cisco Meraki'
    print(f"\nLook for a specific vendor code {vendor_code} in the data frame.\nThis will return a boolean for each row.\n")
    find_dev_type = df['VENDOR_CODE'] == 'Cisco Meraki'
    print(find_dev_type)

    print(f"\nThe value_counts method gives you the totals for {vendor_code} in the data frame.\n")
    print(find_dev_type.value_counts())


    loc_by_label = df.loc[df['VENDOR_CODE'] == vendor_code, : ]
    print_type(loc_by_label, print_dir=True)

    time.sleep(pause_in_seconds)

    print(df['DESTINATION_ADDRESS'])

    # Read in the JSON file

    # records_orientation_fn = 'int_map_sorted_orientrecords.json'
    if records_orientation_fn:
        with open(records_orientation_fn, 'r') as f:
            datastore = json.load(f)

    print(datastore)

    # Transform to a dict of dicts

    dictofints = {}

    for item in datastore:
        print("\n======")
        print(f"Item: {item}")
        print()
        if item['DESTINATION_PORT'] not in dictofints.keys():
            dictofints.update({item['DESTINATION_PORT']: [item]})
        else:
            temp_list = []
            print(f"Key {item['DESTINATION_PORT']} exists\n")

            for k,v in dictofints.items():
                print(f"Key: {k} \t Value: {v}\n")


            print(f"\nList before adding to it: {dictofints[item['DESTINATION_PORT']]}")
            temp_list = dictofints[item['DESTINATION_PORT']]
            print(temp_list)
            temp_list.append(item)
            print(f"After append: {temp_list}")
            dictofints.update({item['DESTINATION_PORT']: temp_list})


    print(f"\n\n Dictioayr of Interfaces:")
    for k, v in dictofints.items():
        print(f"Key: {k} \n")
        for line in v:
            print(f"\t Value: {line}")


    # Drop into an interactive iPython shell to continue playing with the data
    if arguments.interactive:
        IPython.embed()



# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python real_pandas' ")

    #parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    parser.add_argument('-f', '--file', help='Full path to parsed show mac address-table data', action='store')
    parser.add_argument('-p', '--pause_in_seconds', help='Number of seconds to pause between steps (default = 1)', action='store',
                        type=int, default=1)
    parser.add_argument('-i', '--interactive', help='Drop into the interactive IPython shell when script compeltes',
                        action='store_true')
    arguments = parser.parse_args()
    main()


