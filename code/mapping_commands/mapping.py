#!/usr/bin/python

import os
import re

SRC = '/home/eshames/Documents/Final Project/Mapping/files/'
DEST = '/home/eshames/Documents/Final Project/Mapping/script/mapping_file.txt'

def find_regex(file_name):
    ######################################################
    #    Find a match for .*getBroker\(\)\.([\w|_]+)     #
    ######################################################

    regex = 'getBroker' 
    with open(SRC+file_name, 'r') as textfile:
        reg = re.compile("getBroker\(\)\.([\w|_]+)")
        for line in textfile:
            if regex in line:    # if 'getBroker' was found in file
                match = reg.findall(line) # find regex and save it as match
                #print match
                if match:    # if regex was found, create a new line to add to the DEST
                    new_line = file_name[:-5], match[0]
                    return new_line


				
def save_founded_match(match, file_name):
    #####################################
    #    Save the match in a file       #
    #####################################
    
    with open(DEST, 'a') as file_name:
        file_name.write(str(match))


for file_name in os.listdir(SRC):
    match = find_regex(file_name)
    if not match:    #regex wasn't found.
        match = file_name[:-5], ""

    print match
    save_founded_match(match, file_name)
	
