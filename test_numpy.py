# -*- coding: utf-8 -*-
import json
from operator import add,mul,sub
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
    all_white=[]
    all_worm=[]
    for id in a:
        for whiteiteme in a[id]['white'].keys():
            if "-" in whiteiteme:
                del a[id]['white'][whiteiteme]
        for wormiteme in a[id]['worm'].keys():
            if "-" in wormiteme:
                del a[id]['worm'][wormiteme]
        inter_keys=list(set(a[id]['worm'].keys()).intersection(set(a[id]['white'].keys())))
        ids,nums,square_percent_list,white_percent_list,worm_percent_list=get_id_num(a,id,inter_keys)
        all_ids.extend(ids)
        all_num.extend(nums)
        all_squ.extend(square_percent_list)
        all_white.extend(white_percent_list)
        all_worm.extend(worm_percent_list)

        ax.scatter(ids,nums,square_percent_list,c='r', marker='^')
    all=zip(all_ids,all_num,all_squ)
    m=max(all_squ)
    print m
    index =  [i for i, j in enumerate(all_squ) if j == m]
    print index
    print [all_squ[i] for i in index]
    print [all[i] for i in index]
    print "white:",[1-all_white[i] for i in index]
    print "worm:",[all_worm[i] for i in index]
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
    add_square_percent_list=map(add,white_percent_list,worm_percent_list)
    sub_square_percent_list=map(sub,white_percent_list,worm_percent_list)
    square_percent_list=map(sub,add_square_percent_list,map(abs,sub_square_percent_list))
    return  ids,nums,square_percent_list,white_percent_list,worm_percent_list

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
    result_path="json/198.txt"
    open_get(result_path)
