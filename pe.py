import hashlib
from multiprocessing import Pool
import os
import MySQLdb
import shutil

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

def get_pe_sha256(PATH,sha256s):

    f = open(PATH, "rb")
    BUFSIZE = 1024*1024
    buf = f.read(BUFSIZE)
    sha256=hashlib.sha256(buf).hexdigest()
    print sha256
    #get_pe_imports(PATH)

    '''a=open("sha256","a")
    a.write(sha256+"\n" )
    a.write(PATH+"\n")
    a.close()'''
    if sha256 in sha256s:
        shutil.copy(PATH,"white_exe")
def dabase_select():
    db= MySQLdb.connect(db="malware_info", user="root", passwd="polydata", host="localhost", port=3306,charset='utf8')

    cursor = db.cursor()
    try:
        select_sql="select sha256 from lvmeng_dll_exe_5m_white"
        cursor.execute(select_sql)
        sha256s=cursor.fetchall()
        sha256s_list=[str(x).replace('u',"").replace("(","").replace(")","").replace(",","").replace("'","")for x in list(sha256s)]
        db.commit()
        cursor.close()
        db.close()
        return sha256s_list
    except Exception as e:
        print e
        exit()
def get_pe_md5(PATH):
    with open(PATH,'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        a=open("md5","a")
        a.write(hash+"\n")
        a.close()
def get_path(ROOTPATH,sha256s):
    pefiles=os.path.join(ROOTPATH,"lvmeng_dll_5m")
    for root ,dirs,files in os.walk(pefiles):
        for file in files:
            filepa=os.path.join(root,file)
            print filepa
            try:
                get_pe_sha256(filepa,sha256s)
                #get_pe_md5(filepa)
            except Exception as e:
                print e
                pass


if __name__=="__main__":
    sha256s=dabase_select()
    print sha256s
    print type(sha256s)
    get_path(ROOTPATH,sha256s)


