#!/usr/bin/python -tt
# Project: pandas_neteng
# Filename: simple_mac_compare
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "4/10/20"
__copyright__ = "Copyright (c) 2020 Claudia"
__license__ = "Python"

import argparse
import re
import pandas as pd


def normalize_mac(mac):
    """
    Given a Mac, strip periods, colons, or dashes form string and return result in lower case
    :param mac:
    :return:
    """
    return re.sub(r'(\.|:|\-)', '', mac).lower()


def load_nxos_data():

    data = """
server_sw01# show mac address-table
Legend:
* - primary entry, G - Gateway MAC, (R) - Routed MAC, O - Overlay MAC
age - seconds since first seen,+ - primary entry using vPC Peer-Link
VLAN MAC Address Type age Secure NTFY Ports/SWID.SSID.LID
---------+-----------------+--------+---------+------+----+------------------
* 98 0008.e3ff.fd8c dynamic 18144320 F F Po11
* 98 0050.5684.5b01 dynamic 5264790 F F Po204
* 99 0000.0000.0100 dynamic 5264790 F F Po204
* 750 a025.b5f2.5000 dynamic 5263760 F F Po205
* 750 a025.b5f2.5004 dynamic 0 F F Po205
* 704 0008.e3ff.fd8c dynamic 25832130 F F Po11
* 700 0050.5680.5f61 dynamic 2965950 F F Po205
* 700 0050.5680.6564 dynamic 3740090 F F Po204
* 700 0050.5684.5f2f dynamic 5264800 F F Po204
* 700 0050.5684.cca7 dynamic 5264800 F F Po204
* 700 0050.5684.d66e dynamic 5263760 F F Po205
* 700 80e0.1d37.1e18 dynamic 25301470 F F Eth1/8
* 700 80e0.1d37.1e1e dynamic 25832170 F F Eth1/44
+ 700 80e0.1d37.2b7c dynamic 0 F F Po777
* 700 80e0.1d37.2b82 dynamic 25832170 F F Eth1/37
+ 700 e4aa.5dac.81f6 dynamic 0 F F Po777
* 700 e4aa.5dac.81f7 dynamic 636250 F F Eth1/43
* 699 0008.e3ff.fd8c dynamic 25832130 F F Po11
* 699 02a0.98d3.71f5 dynamic 1523000 F F Po202
server_sw01#    
    """
    return data


def load_aci_data():

    aci_data = {
        "totalCount": "4",
        "imdata": [
            {
                "fvCEp": {
                    "attributes": {
                        "annotation": "",
                        "childAction": "",
                        "contName": "",
                        "dn": "uni/tn-SnV/ap-Rescue/epg-Web/cep-42:5D:BC:C4:00:00",
                        "encap": "vlan-123",
                        "extMngdBy": "",
                        "id": "0",
                        "idepdn": "",
                        "ip": "10.193.101.10",
                        "lcC": "learned",
                        "lcOwn": "local",
                        "mac": "42:5D:BC:C4:00:00",
                        "mcastAddr": "not-applicable",
                        "modTs": "2020-04-10T11:11:11.736+00:00",
                        "monPolDn": "uni/tn-common/monepg-default",
                        "name": "42:5D:BC:C4:00:00",
                        "nameAlias": "",
                        "status": "",
                        "uid": "0",
                        "uuid": "",
                        "vmmSrc": ""
                    }
                }
            },
            {
                "fvCEp": {
                    "attributes": {
                        "annotation": "",
                        "childAction": "",
                        "contName": "",
                        "dn": "uni/tn-SnV/ap-Evolution_X/epg-Web/cep-42:5D:BC:C4:00:00",
                        "encap": "vlan-121",
                        "extMngdBy": "",
                        "id": "0",
                        "idepdn": "",
                        "ip": "2222::65:a",
                        "lcC": "learned",
                        "lcOwn": "local",
                        "mac": "42:5D:BC:C4:00:00",
                        "mcastAddr": "not-applicable",
                        "modTs": "2020-04-10T11:11:11.736+00:00",
                        "monPolDn": "uni/tn-common/monepg-default",
                        "name": "42:5D:BC:C4:00:00",
                        "nameAlias": "",
                        "status": "",
                        "uid": "0",
                        "uuid": "",
                        "vmmSrc": ""
                    }
                }
            },
            {
                "fvCEp": {
                    "attributes": {
                        "annotation": "",
                        "childAction": "",
                        "contName": "",
                        "dn": "uni/tn-SnV/ap-Chaos/epg-Web/cep-42:5D:BC:C4:00:00",
                        "encap": "vlan-125",
                        "extMngdBy": "",
                        "id": "0",
                        "idepdn": "",
                        "ip": "10.193.101.10",
                        "lcC": "learned",
                        "lcOwn": "local",
                        "mac": "42:5D:BC:C4:00:00",
                        "mcastAddr": "not-applicable",
                        "modTs": "2020-04-10T11:11:11.736+00:00",
                        "monPolDn": "uni/tn-common/monepg-default",
                        "name": "42:5D:BC:C4:00:00",
                        "nameAlias": "",
                        "status": "",
                        "uid": "0",
                        "uuid": "",
                        "vmmSrc": ""
                    }
                }
            },
            {
                "fvCEp": {
                    "attributes": {
                        "annotation": "",
                        "childAction": "",
                        "contName": "",
                        "dn": "uni/tn-SnV/ap-Power_Up/epg-Web/cep-42:5D:BC:C4:00:00",
                        "encap": "vlan-127",
                        "extMngdBy": "",
                        "id": "0",
                        "idepdn": "",
                        "ip": "2222::65:a",
                        "lcC": "learned",
                        "lcOwn": "local",
                        "mac": "42:5D:BC:C4:00:00",
                        "mcastAddr": "not-applicable",
                        "modTs": "2020-04-10T11:11:11.736+00:00",
                        "monPolDn": "uni/tn-common/monepg-default",
                        "name": "42:5D:BC:C4:00:00",
                        "nameAlias": "",
                        "status": "",
                        "uid": "0",
                        "uuid": "",
                        "vmmSrc": ""
                    }
                }
            },
            {
                "fvCEp": {
                    "attributes": {
                        "annotation": "",
                        "childAction": "",
                        "contName": "",
                        "dn": "uni/tn-SnV/ap-Power_Up/epg-Web/cep-42:5D:BC:C4:00:00",
                        "encap": "vlan-700",
                        "extMngdBy": "",
                        "id": "0",
                        "idepdn": "",
                        "ip": "2222::65:a",
                        "lcC": "learned",
                        "lcOwn": "local",
                        "mac": "00:50:56:80:65:64",
                        "mcastAddr": "not-applicable",
                        "modTs": "2020-04-10T11:11:11.736+00:00",
                        "monPolDn": "uni/tn-common/monepg-default",
                        "name": "42:5D:BC:C4:00:00",
                        "nameAlias": "",
                        "status": "",
                        "uid": "0",
                        "uuid": "",
                        "vmmSrc": ""
                    }
                }
            }
        ]
    }

    return aci_data


def main():

    # Load the nxos data
    nxos = load_nxos_data()
    # Process the text output of the show command and turn into a list of lines
    n = nxos.splitlines()

    # Initialize an empty list of mac lines which will contain lists of each line with a mac address
    # This is a list of lists
    mac_list = []

    # Iterate over the lines and look for the mac address result line pattern
    # * 700 80e0.1d37.2b82 dynamic 25832170 F F Eth1/37
    for line in n:
        # print(line)
        # mac_match = re.search(r'([0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})', line, re.IGNORECASE)
        line_match = re.search(r'^.{1,3}\s+\d{1,4}\s+([0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})\s+\w+', line, re.IGNORECASE)
        if line_match:
            # If the re search finds a match, split the line into a list (split on spaces)
            line_split = line_match.group().split()
            # append the line_split list to the mac_list (list of lists)
            mac_list.append(line_split)
    # Turn the mac_list list of lists into a Pandas Data Frame
    df = pd.DataFrame(mac_list)
    # Add a new column called 'normalized_mac' and strip off any punctuation characters and make lower case
    # The normalize_mac function does this
    df['normalized_mac']= df[2].map(normalize_mac)
    print(f"\nNXOS Data Frame: \n{df}")

    # Load the aci data
    aci = load_aci_data()
    aci_mac_list = []
    for line in aci['imdata']:
        temp_list = []
        # print(line['fvCEp']['attributes']['mac'])
        temp_list.append(line['fvCEp']['attributes']['mac'])
        temp_list.append(line['fvCEp']['attributes']['encap'])
        aci_mac_list.append(temp_list)

    # Turn the aci_mac_list list of lists into a Pandas Data Frame
    df_aci = pd.DataFrame(aci_mac_list)
    # Add a new column called 'normalized_mac' and strip off any punctuation characters and make lower case
    # The normalize_mac function does this
    df_aci['normalized_mac']= df_aci[0].map(normalize_mac)
    print(f"\nACI Data Frame: \n{df_aci}")

    df_merged = pd.merge(df, df_aci, on='normalized_mac', how='outer', indicator='Exist')
    print(f"\nNX-OS and ACI MERGED Data Frame: \n{df_merged}")

    found_df = df_merged.loc[df_merged['Exist'] == 'both']
    notfound_df = df_merged.loc[df_merged['Exist'] != 'both']

    print(f"\n\nFound {len(found_df)} MAC(s): \n{found_df}")
    print(f"\n\n{len(notfound_df)} MAC(s) MISSING: \n{notfound_df}")

    print(f"\n\n============== SUMMARY ============== ")
    print(f"Of {len(df_merged)} Total MACs both legacy and ACI: \n\t- FOUND\t\t{len(found_df)} "
          f"\n\t- MISSING\t{len(notfound_df)} \n\n")


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python simple_mac_compare' ")
    arguments = parser.parse_args()
    main()
