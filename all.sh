#!/bin/bash
allsvm=`find . -name "*.svm"`
echo "$allsvm" | while read line;do echo $line>>lireport echo `svm-train -t 0 -v 5 $line` >>lireport; done
