import hashlib
import os

__author__ = 'liebesu'

import pefile
def get_pe_imports(PATH):
    pe=pefile.PE(PATH)
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        dll=entry.dll
        print dll
        for imp in entry.imports:
            print "\t",imp.name

def get_pe_sha256(PATH):
    f = open(PATH, "rb")
    BUFSIZE = 1024*1024
    buf = f.read(BUFSIZE)
    sha256=hashlib.sha256(buf).hexdigest()
    return sha256
    a=open("sha256","a")
    a.write(sha256+"\r\n")
    a.close()
def get_path():
    list =os.listdir(rootdir)





