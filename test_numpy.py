# -*- coding: utf-8 -*-
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def open_get(path):
    a=open(path,'r').read()
    a=eval(a)
    trim(a)
def trim(a):

    for id in a:

        for whiteiteme in a[id]['white'].keys():
            if "-" in whiteiteme:
                del a[id]['white'][whiteiteme]
        for wormiteme in a[id]['worm'].keys():
            if "-" in wormiteme:
                del a[id]['worm'][wormiteme]
        inter_keys=list(set(a[id]['worm'].keys()).intersection(set(a[id]['white'].keys())))

        #print inter_keys
        white_percent_list=[]
        worm_percent_list=[]
        square_percent_list=[]
        nums=[]
        ids=[]
        for sig_inter_key in inter_keys:

            all_white_valus=0
            all_worm_valus=0
            white_values = 0
            worm_values =0
            for whiteiteme in a[id]['white'].keys():
                all_white_valus +=float(a[id]['white'][whiteiteme])
            for whiteiteme in a[id]['white'].keys():
                if int(sig_inter_key)>=int(whiteiteme):
                    white_valu=a[id]['white'][whiteiteme]
                    white_values +=int(white_valu)
                    white_percent=white_values/all_white_valus
            #white_percent_list.append(white_percent)

            for wormiteme in a[id]['worm'].keys():
                all_worm_valus +=float(a[id]['worm'][wormiteme])
            for wormiteme in a[id]['worm'].keys():
                if int(sig_inter_key)>=int(wormiteme):
                    worm_valu=a[id]['worm'][wormiteme]
                    worm_values +=int(worm_valu)
                    worm_percent=1-(worm_values/all_worm_valus)


                    ids.append(id)
            nums.append(sig_inter_key)
            square=(worm_percent*worm_percent)+(white_percent*white_percent)
            square_percent_list.append(square)

            #worm_percent_list.append(worm_percent)
            #white_percent=1-white_percent
            #if np.sqrt((worm_percent*worm_percent)-(white_percent*white_percent))>0.623:
            '''if white_percent+worm_percent>1.2:
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
            print white_percent_list,worm_percent_list'''
        '''plt.plot(white_percent_list,worm_percent_list,'ro')
        plt.title("PE Detection Rate")
        plt.xlabel('White_percent')
        plt.ylabel('Malware_percent')    #为y轴加注释
        plt.plot(white_percent_list,worm_percent_list,'ro')
        plt.title("PE Detection Rate")
        plt.xlabel('White_percent')
        plt.ylabel('Malware_percent')    #为y轴加注释'''
        print ids,nums,square_percent_list
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot_surface(ids, nums, square_percent_list, rstride=1, cstride=1,cmap='rainbow')
    plt.show()
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
    result_path="json/31.txt"
    open_get(result_path)
