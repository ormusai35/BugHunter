import os
import re
import sys

# ART_LOG = 'C:\\Users\\ormusai35\\Desktop\\bug_hunter\\test_snapshot_on_cloned_vm[iscsi]\\engine.log'
# ENGINE_LOG = 'C:\\Users\\ormusai35\\Desktop\\bug_hunter\\test_snapshot_on_cloned_vm[iscsi]\\art_test_runner.log'
# VDSM_1 = 'C:\\Users\\ormusai35\\Desktop\\bug_hunter\\test_snapshot_on_cloned_vm[iscsi]\\hypervisor-lynx18_vdsm.log'
# VDSM_2 = 'C:\\Users\\ormusai35\\Desktop\\bug_hunter\\test_snapshot_on_cloned_vm[iscsi]\\hypervisor-lynx19_vdsm.log'
# VDSM_3 = 'C:\\Users\\ormusai35\\Desktop\\bug_hunter\\test_snapshot_on_cloned_vm[iscsi]\\hypervisor-lynx20_vdsm.log'

ENGINE_OUTPUT = 'C:\\Users\\ormusai35\\Desktop\\bug_hunter\\outputs\\engine_output.txt'
VDSM_1_OUTPUT = 'C:\\Users\\ormusai35\\Desktop\\bug_hunter\\outputs\\vdsm_1_output.txt'
VDSM_2_OUTPUT = 'C:\\Users\\ormusai35\\Desktop\\bug_hunter\\outputs\\vdsm_2_output.txt'
VDSM_3_OUTPUT = 'C:\\Users\\ormusai35\\Desktop\\bug_hunter\\outputs\\vdsm_3_output.txt'


################# functions ################################################################################
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

def analyze_log_files(engine_file, art_log_file, vdsm1_file, vdsm2_file, vdsm3_file):
    # find corrID in art_log:
    id_list = find_correlation_id(art_log_file)

    # search for corr_id in logs:
    for cid in id_list:
        search_for_corr_id_matches(engine_file, ENGINE_OUTPUT, cid)
        search_for_corr_id_matches(vdsm1_file, VDSM_1_OUTPUT, cid)
        search_for_corr_id_matches(vdsm2_file, VDSM_2_OUTPUT, cid)
        search_for_corr_id_matches(vdsm3_file, VDSM_3_OUTPUT, cid)

    # Find ERRORs and WARNINGs in logs:
    line_str = "\n******* ERRORS & WARNINGS *******\n"
    write_line(line_str, ENGINE_OUTPUT)
    find_errors_and_warnings(engine_file, ENGINE_OUTPUT)
    write_line(line_str, VDSM_1_OUTPUT)
    find_errors_and_warnings(vdsm1_file, VDSM_1_OUTPUT)
    write_line(line_str, VDSM_2_OUTPUT)
    find_errors_and_warnings(vdsm2_file, VDSM_2_OUTPUT)
    write_line(line_str, VDSM_3_OUTPUT)
    find_errors_and_warnings(vdsm3_file, VDSM_3_OUTPUT)

############### Flask ###################################################################################

from flask import Flask,render_template,request

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def printer(path):
    print (path)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'logfiles/')[0:-1]
    print(target)
    file1 = request.files['file1']
    file2 = request.files['file2']
    file3 = request.files['file3']
    file4 = request.files['file4']
    file5 = request.files['file5']
    engine_file = '\\'.join([target, file1.filename])
    art_log_file = '\\'.join([target, file2.filename])
    vdsm1_file = '\\'.join([target, file3.filename])
    vdsm2_file = '\\'.join([target, file4.filename])
    vdsm3_file = '\\'.join([target, file5.filename])
    print(engine_file, art_log_file, vdsm1_file, vdsm2_file, vdsm3_file)
    analyze_log_files(engine_file, art_log_file, vdsm1_file, vdsm2_file, vdsm3_file)
    return engine_file


if __name__ == "__main__":
	app.run(debug=True)

