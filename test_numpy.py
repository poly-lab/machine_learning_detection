# -*- coding: utf-8 -*-
import json
from operator import add,mul
from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def open_get(path):
    a=open(path,'r').read()
    a=eval(a)
    trim(a)
def trim(a):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    all_ids=[]
    all_num=[]
    all_squ=[]

    for id in a:
        for whiteiteme in a[id]['white'].keys():
            if "-" in whiteiteme:
                del a[id]['white'][whiteiteme]
        for wormiteme in a[id]['worm'].keys():
            if "-" in wormiteme:
                del a[id]['worm'][wormiteme]
        inter_keys=list(set(a[id]['worm'].keys()).intersection(set(a[id]['white'].keys())))
        ids,nums,square_percent_list=get_id_num(a,id,inter_keys)
        all_ids.extend(ids)
        all_num.extend(nums)
        all_squ.extend(square_percent_list)


        ax.scatter(ids,nums,square_percent_list,c='r', marker='^')
    all=zip(all_ids,all_num,all_squ)
    m=max(all_squ)
    print m
    index =  [i for i, j in enumerate(all_squ) if j == m]
    print index
    print [all_squ[i] for i in index]
    print [all[i] for i in index]

    ax.set_xlabel('id')
    ax.set_ylabel('num')
    ax.set_zlabel('square_percent')
    plt.show()


def get_id_num(a,id,inter_keys):
    white_percent_list=[]
    worm_percent_list=[]
    ids=[]
    nums=[]
    square_percent_list=[]
    for sig_inter_key in inter_keys:
        all_white_valus=0
        all_worm_valus=0
        white_values = 0
        worm_values =0
        for whiteiteme in a[id]['white'].keys():
            all_white_valus +=float(a[id]['white'][whiteiteme])

        white_percent=white_percent_(a,id,all_white_valus,sig_inter_key)
        white_percent_list.append(white_percent)
        for wormiteme in a[id]['worm'].keys():
            all_worm_valus +=float(a[id]['worm'][wormiteme])
        worm_percent=worm_percent_(a,id,all_worm_valus,sig_inter_key)
        worm_percent_list.append(worm_percent)

        nums.append(float(sig_inter_key))
        ids.append(float(id))
    square_percent_list=map(add,map(mul,white_percent_list,white_percent_list),map(mul,worm_percent_list,worm_percent_list))
    return  ids,nums,square_percent_list
def draw_3d(ids,nums,square_percent_list):
    #平面图
    '''print ids,nums,square_percent_list
    plt.plot(nums,square_percent_list,'ro')
    plt.title("PE Detection Rate")
    plt.xlabel('White_percent')
    plt.ylabel('Malware_percent')    #为y轴加注释'''
    #立体图
    print ids,nums,square_percent_list
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(ids,nums,square_percent_list,c='r', marker='o')


def worm_percent_(a,id,all_worm_valus,sig_inter_key):
    worm_values=0
    for wormiteme in a[id]['worm'].keys():
        if int(sig_inter_key)>=int(wormiteme):
            worm_valu=a[id]['worm'][wormiteme]
            worm_values +=int(worm_valu)
            worm_percent=1-(worm_values/all_worm_valus)

    return worm_percent
def white_percent_(a,id,all_white_valus,sig_inter_key):
    white_values=0
    for whiteiteme in a[id]['white'].keys():
        if int(sig_inter_key)>=int(whiteiteme):
            white_valu=a[id]['white'][whiteiteme]
            white_values +=int(white_valu)
            white_percent=white_values/all_white_valus
    return white_percent

    '''worm_percent_list.append(worm_percent)
    square=(worm_percent*worm_percent)+(white_percent*white_percent)
    square_percent_list.append(square)
    print ids,nums,square_percent_list
    ax=plt.subplot(111,projection='3d')
#ax = Axes3D(fig)
    ax.plot_surface(ids, nums, square_percent_list)
    plt.show()'''
    '''worm_percent_list.append(worm_percent)
    #white_percent=1-white_percent
    #if np.sqrt((worm_percent*worm_percent)-(white_percent*white_percent))>0.623:
    if white_percent+worm_percent>1.2:
        white_percent=1-white_percent
        if np.sqrt((worm_percent*worm_percent)-(white_percent*white_percent))>0.50:
            print "id:",id
            print "num:",sig_inter_key
            print "all_white_valus",all_white_valus
            print "all_worm_valus",all_worm_valus
            print "white_percent:",white_percent
            print "worm_percent:",worm_percent
            white_percent_list.append(white_percent)
            worm_percent_list.append(worm_percent)

        print sig_inter_key
        print white_percent
        print worm_percent
        print white_percent_list,worm_percent_list
    plt.plot(white_percent_list,worm_percent_list,'ro')
    plt.title("PE Detection Rate")
    plt.xlabel('White_percent')
    plt.ylabel('Malware_percent')    #为y轴加注释
    plt.plot(white_percent_list,worm_percent_list,'ro')
    plt.title("PE Detection Rate")
    plt.xlabel('White_percent')
    plt.ylabel('Malware_percent')    #为y轴加注释'''

    #print max(white_percent_list)
    #print max(worm_percent_list)
    #plt.show()


def pre_pares(a):
    pass


def get_dec(a):
    for id in a:
        print id
        feature_num=a[id]['feature_num']
        api_ratio=a[id]['api_ratio']
        white=a[id]['white']
        worm=a[id]['worm']
        api_thresh=a[id]['api_thresh']
        print feature_num,api_ratio,worm.keys(),worm.values(),worm,api_thresh

        plt.plot(worm.keys(),worm.values())
        plt.ylabel('worm')    #为y轴加注释
        plt.show()

if __name__ == "__main__" :
    result_path="json/23.txt"
    open_get(result_path)
