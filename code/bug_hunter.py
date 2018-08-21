#!/usr/bin/python

import os
import re
import sys

ART_LOG = '/home/eshames/Documents/FinalProject/logs/Errors/test_snapshot_on_cloned_vm[iscsi]/art_test_runner.log'
ENGINE_LOG = '/home/eshames/Documents/FinalProject/logs/Errors/test_snapshot_on_cloned_vm[iscsi]/engine.log'
VDSM_1 = '/home/eshames/Documents/FinalProject/logs/Errors/test_snapshot_on_cloned_vm[iscsi]/hypervisor-lynx18_vdsm.log'
VDSM_2 = '/home/eshames/Documents/FinalProject/logs/Errors/test_snapshot_on_cloned_vm[iscsi]/hypervisor-lynx19_vdsm.log'
VDSM_3 = '/home/eshames/Documents/FinalProject/logs/Errors/test_snapshot_on_cloned_vm[iscsi]/hypervisor-lynx20_vdsm.log'

ENGINE_OUTPUT = '/home/eshames/Documents/FinalProject/logs/Errors/engine_output.txt'
VDSM_1_OUTPUT = '/home/eshames/Documents/FinalProject/logs/Errors/vdsm_1_output.txt'
VDSM_2_OUTPUT = '/home/eshames/Documents/FinalProject/logs/Errors/vdsm_2_output.txt'
VDSM_3_OUTPUT = '/home/eshames/Documents/FinalProject/logs/Errors/vdsm_3_output.txt'


def main(argv):

    # find corrID in art_log:
    id_list = find_correlation_id(ART_LOG)

    # search for corr_id in logs:
    for cid in id_list:
        search_for_corr_id_matches(ENGINE_LOG, ENGINE_OUTPUT, cid)
        search_for_corr_id_matches(VDSM_1, VDSM_1_OUTPUT, cid)
        search_for_corr_id_matches(VDSM_2, VDSM_2_OUTPUT, cid)
        search_for_corr_id_matches(VDSM_3, VDSM_3_OUTPUT, cid)

    # Find ERRORs and WARNINGs in logs:
    line_str = "\n******* ERRORS & WARNINGS *******\n"
    write_line(line_str, ENGINE_OUTPUT)
    find_errors_and_warnings(ENGINE_LOG, ENGINE_OUTPUT)
    write_line(line_str, VDSM_1_OUTPUT)
    find_errors_and_warnings(VDSM_1, VDSM_1_OUTPUT)
    write_line(line_str, VDSM_2_OUTPUT)
    find_errors_and_warnings(VDSM_2, VDSM_2_OUTPUT)
    write_line(line_str, VDSM_3_OUTPUT)
    find_errors_and_warnings(VDSM_3, VDSM_3_OUTPUT)


def find_errors_and_warnings(src_file, dst_file):

    with open(src_file, 'r') as textfile:

        regex = "(\A.*((ERROR)|(WARN)|(Traceback)).*)"
        reg = re.compile(regex)

        for line in textfile:
            m = reg.findall(line)
            if m:
                match = ''.join(m[0][0])+"\n"
                write_line(match, dst_file)

            # print traceback errors.
            # these errors doesnt start with date
            date_regex = "(\A\d{4}\-\d{2}\-\d{2} \d{2}\:\d{2}\:\d{2}.*)"
            date_reg = re.compile(date_regex)
            d = date_reg.findall(line)
            if not d:
                write_line(line, dst_file)


def write_line(match, dst_file):
    #####################################
    #    Save the match in a file       #
    #####################################

    with open(dst_file, 'a') as file_name:
        file_name.write(str(match))


def find_correlation_id(art_log):

    id_list = []  # save each corr_id in this list
    with open(art_log, 'r') as textfile:
        regex = re.compile("\A.*Using Correlation-Id: (.*)")  # regex for the correlation id
        '''
        In each line of art log file, if the string "Using Correlation-Id" is in the line
        find a match of the regex and save it in 'corr_id', then add it to the list
        '''
        for line in textfile:
            if "Using Correlation-Id" in line:
                corr_id = regex.findall(line)  # find correlation id
                id_list.append(corr_id)

    return id_list
    # now we have a list with all corr_id
    # next step: remove duplicates in that list.


def search_for_corr_id_matches(src_file, dst_file, corr_id):

    cid = "\n" + ''.join(corr_id) + ":\n"  # corr_id is now a string - cid
    write_line(cid, dst_file)
    with open(src_file, 'r') as textfile:
        '''
        In each line of the file: 
        for each corr_id in the list: make corr_id a string and save it as cid
        Then, if cid in line - print the line
        '''
        for line in textfile:
            cid = ''.join(corr_id)
            if cid in line:
                write_line(line, dst_file)


if __name__ == "__main__":
    main(sys.argv)