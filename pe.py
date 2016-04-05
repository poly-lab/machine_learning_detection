import hashlib
from multiprocessing import Pool
import os

__author__ = 'liebesu'

import pefile
from lib.core.constants import ROOTPATH
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
def get_path(ROOTPATH,FlagStr=[]):
    FILEPATH=os.path.join(ROOTPATH,"pefile")
    FileList=[]
    FileNames=os.listdir(FILEPATH)
    if (len(FileNames)>0):
       for fn in FileNames:
           if (len(FlagStr)>0):

               if (IsSubString(FlagStr,fn)):
                   fullfilename=os.path.join(FILEPATH,fn)
                   FileList.append(fullfilename)
           else:

               fullfilename=os.path.join(FILEPATH,fn)
               FileList.append(fullfilename)


    if (len(FileList)>0):
        FileList.sort()
    return FileList
def IsSubString(SubStrList,Str):
    flag=True
    for substr in SubStrList:
        if not(substr in Str):
            flag=False

    return flag

if __name__=="__main__":
    filelist=get_path(ROOTPATH)
    pool=Pool(processes=10)
    pool.map(get_pe_sha256,filelist)
    pool.close()
    pool.join()

