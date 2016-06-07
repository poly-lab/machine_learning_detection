# -*- coding: utf-8 -*-
import json
import numpy as np
import matplotlib.pyplot as plt
a=open('json/10.txt',"r").read().replace('"',"'")
print type(a)
a=eval(a)
print type(a)
print a
dict = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
print dict['Name']
print a['1']
'''
x = np.linspace(0, 10, 1000)
y = np.cos(x)
z = np.cos(x**2)

plt.figure(figsize=(9,4))
plt.plot(x,y,label="$sin(x)$",color="red",linewidth=2)
plt.plot(x,z,"b--",label="$cos(x^2)$")
plt.xlabel("Time(s)")
plt.ylabel("Volt")
plt.title("PyPlot First Example")
plt.ylim(-1.2,1.2)
plt.legend()
plt.show()
'''
plt.plot([1,2,3,4])
plt.ylabel('some numbers')    #为y轴加注释
plt.show()