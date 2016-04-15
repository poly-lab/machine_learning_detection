import hashlib
from multiprocessing import Pool
import os

__author__ = 'liebesu'

import pefile
from lib.core.constants import ROOTPATH
def get_pe_imports(PATH):
    pe=pefile.PE(PATH)
    print pe.sections
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
    print sha256
    get_pe_imports(PATH)
    a=open("sha256","a")
    a.write(sha256+"\n")
    a.close()
def get_pe_md5(PATH):
    with open(PATH,'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        a=open("md5","a")
        a.write(hash+"\n")
        a.close()
def get_path(ROOTPATH):
    pefiles=os.path.join(ROOTPATH,"pefiles")
    for root ,dirs,files in os.walk(pefiles):
        for file in files:
            filepa=os.path.join(root,file)
            print filepa
            try:
                get_pe_sha256(filepa)
                get_pe_md5(filepa)
            except Exception as e:
                print e
                pass


if __name__=="__main__":
   get_path(ROOTPATH)


