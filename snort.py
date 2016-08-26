import os
import re
lines=open('20160826.rules').readlines()
for line in lines:
    num=90522013
    num=num+lines.index(line)
    sig_new='sid:'+str(num)
    sig=re.compile('sid:\d+')
    info=re.sub(sig, sig_new, line)
    re1='.*?'	# Non-greedy match on filler
    re2='(msg)'	# Variable Name 1
    re3='.*?'	# Non-greedy match on filler
    re4='(".*?")'	# Double Quote String 1
    
    rg = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)
    m = rg.search(line)
    if m:
        var1=m.group(1)
        string1=m.group(2)
        msg="("+var1+")"+"("+string1+")"+"\n"
    
    new_map=str(num)+" || GPL polydata "+msg.replace('(msg)("','').replace('")','')
    a=open('polydata.rules','a+')
    a.write(info)
    a.close
    b=open('polydata.map','a')
    b.write(new_map)
    b.close
    