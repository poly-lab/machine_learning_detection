import yara

import os
import fnmatch
a=yara.compile('/polylab/updatepack/test/yararules/all.yar')

def iterfindfiles(path, fnexp):
    for root, dirs, files in os.walk(path):
        for filename in fnmatch.filter(files, fnexp):
            yield os.path.join(root, filename)

for filename in iterfindfiles(r"/data2/samples/kaspersky/", "*.vir"):
    
    
    try:
        b=a.match(filename)
    except :
        error_file=open("error.txt",'a')
        error_file.write(filename+"\n")
        error_file.close()
        
    if b:
        have_result=open("result.txt",'a')
        have_result.write(filename+"\n")
        have_result.write(str(b)+"\n")
        have_result.close()
    else:
        no_result=open("no_result.txt",'a')
        no_result.write(filename+"\n")
        no_result.close()

