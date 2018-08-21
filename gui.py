import os
import re
import sys

from tkinter import filedialog
from tkinter import *

ENGINE_FLOW_FILE = 'C:\\Users\ormusai35\Desktop\searchLogs\\test_snapshot_on_cloned_vm[iscsi]\Flow_File.txt'

################# functions ################################################################################

def write_line(file_to_write, match):
    #####################################
    #    Save the match in a file       #
    #####################################

    with open(file_to_write, 'a') as file_name:
        file_name.write(str(match))

    return file_name


def Find_Flow(text_file, corr):
    with open(text_file, 'r') as textfile:
        '''
        In each line of engine_log file: 
        for each corr_id in the list: make corr_id a string and save it as cid
        Then, if cid in line - print the line
        '''
        for line in textfile:
            if corr in line:
                cid = ''.join(corr)
                # print cid, ": ",  line
                write_line(ENGINE_FLOW_FILE, line)
                T.insert(END, line)
                # next step: save output to a file
                # next step: seperate the prints into blocks per corr_id

def choose_engine():
    root.engine = filedialog.askopenfilename(initialdir="/", title="Select file",
                                             filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    return

def choose_Artlog():
    root.artlog = filedialog.askopenfilename(initialdir="/", title="Select file",
                                             filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    return

def choose_VDSM():
    root.vdsm = filedialog.askopenfilename(initialdir="/", title="Select file",
                                             filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    return

############### Gui ###################################################################################

root = Tk()

photo = PhotoImage(file = "rh.png")
label = Label(root,image = photo)
# label.pack()

uploadEngine_bt = Button(root,text = "choose Engine file", command= choose_engine, bd = 5).pack(fill =X)
# uploadEngine_bt.pack()
uploadArt_bt = Button(root,text = "choose Art-Log file", command= choose_Artlog, bd = 5).pack(fill = X)
# uploadArt_bt.pack()
uploadVDSM_bt = Button(root,text = "choose VDSM file", command= choose_VDSM, bd = 5).pack(fill = X)
# uploadVDSM_bt.pack()
# root.art_log = filedialog.askopenfilename(initialdir="/", title="Select file",
#                                            filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

butt = Button(root,bd = 5,background = "red",text = "enter here", command= lambda: Find_Flow(root.engine,"vms_delete_f3d4fe0f-0c7b-469c")).pack(side = BOTTOM,fill = Y)

S = Scrollbar(root)
T = Text(root, height=20, width=60)
S.pack(side=RIGHT, fill=Y)
T.pack(side=BOTTOM, fill=Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)

# butt.pack()
root.mainloop()