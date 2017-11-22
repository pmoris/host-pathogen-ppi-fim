#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Pieter Moris
'''

"""
Tool to format lines of the format:
('v@GO0003677,v@GO0005515,v@GO0030683>h@GO0044238', 157, (0.7804054054054054, 231))
h@GO1902578,h@IPR016024>v@GO0033647;0.5474452554744526;0.26993124967785675


to 

h@GO name, h@IPR016024 > v@GO0name; 0.5474452554744526; 0.26993124967785675

('v@"GO name",v@"GO name",v@"GO name">h@"GO name"', 157, (0.7804054054054054, 231))

NOTE: paths to obo-tools are hardcoded.
"""

import re
import os
import sys
sys.path.append(os.path.abspath('..'))

from pathlib import Path

from go_tools import obo_tools

# sys.path.insert(0, r'/media/pieter/DATA/Wetenschap/Doctoraat/host-pathogen-project/host-pathogen-ppi-fim/ppi_scripts/go_tools')


try:
    input_file = Path(sys.argv[1])
except IndexError:
    print('No input file was defined.')
try:
    output_file = Path(sys.argv[2])
except IndexError:
    print('No output file was defined.')

# go_dict = obo_tools.importOBO(r'/media/pieter/DATA/Wetenschap/Doctoraat/host-pathogen-project/host-pathogen-ppi-fim/go_data/go.obo')
go_dict = obo_tools.importOBO(r'../../data/raw/go_data/go.obo')

def grab_name(match):
    # l = element.split('@')
    # print(l)
    # go_name = go_dict.get([1]).name
    # return l[0]+'-'+go_name
    id = match.group(1) + ':' + match.group(2)
    if id in go_dict:
        return go_dict[id].name
    else:
        print('{} was not found in GO dictionary'.format(id))
        return id

with input_file.open() as f:
    with output_file.open('w') as o:
        regex = re.compile('(GO|IPR)(\d*)', re.IGNORECASE)
        regex_hv = re.compile('(h|v)@', re.IGNORECASE)
        for line in f:
            substituted = regex.sub(grab_name, line)
            substituted = regex_hv.sub(lambda x: x.group(1).upper() + '-', substituted)
            substituted = substituted.strip('\n')
            print(substituted)
            o.write(substituted + '\t' + str(len(substituted)) + '\n')

