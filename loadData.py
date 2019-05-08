#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 23:55:52 2019

@author: JayMessina
"""

import pandas

def loadReq(directory):
    d = {}
    dataset = pandas.read_excel(directory)
    array = dataset.values
   
    for item in array:
        if len(item[0])<=22:
            curKey = item[0]
            d[curKey] = []
        else:
            d[curKey].append(item)
    return d

    
def readClasses(directory):
    for filename in os.listdir(directory):
            if(filename==".DS_Store"):
                continue
            print(filename)
            file = directory + "/" + filename
            dataset = pandas.read_excel(file)
            array = dataset.values
            #game = array[:,0,1]
            game = array[:,0:1]
            
            X = array[:,2:17]
    


def main():
    #webscraping + initial user interface
    
    #return dictionary
    directory = "writing_intensive.xlsx"
    dict_wint = loadWINT(directory)
    
    directory = "cultural_diversity.xlsx"
    dict_cd = loadReq(directory)
    
    directory = "writing_advanced.xlsx"
    dict_wadv = loadReq(directory)
    
    directory = "QFR.xlsx"
    dict_qfr = loadReq(directory)
    
    print(dict_qfr)
    
    
main()