#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 23:55:52 2019

@author: JayMessina
"""

import pandas
import os

classes = {}

'''
def loadReq(directory):
    d = {}
    dataset = pandas.read_excel(directory)
    array = dataset.values
   
    for item in array:
        if len(item[0])<=22 or item[0]=="Statistical Methods (STAT)" or item[0]=="Environmental Studies (ENVS)":
            curKey = item[0]
            d[curKey] = []
        else:
            d[curKey].append(item[0])
    return d
'''

def loadReq(directory):
    d = set()
    dataset = pandas.read_excel(directory)
    array = dataset.values
   
    L = ["Quantitative and Formal Reasoning Courses With Prerequisites", "Statistical Methods (STAT)", "Physics and Astronomy (PHYS) (ASTR)", "Environmental Studies (ENVS)", "First Year Seminar Program (FYSP)", 'Computer Science (CSCI)']
    for item in array:
        
        if "-" not in item[0]:
            continue
        
        if len(item[0])<=22 or item[0] in L:
            continue
        else:
            s = item[0].split("-")
            d.add(s[0][0:len(s[0])-1])
    return d
    
def readClasses(directory):
    global classes
    #order of labels is: NUMB, SEC, CRN, HRS, MOD, TITLE, DAYS, TIME, BLDG, INSTRUCTOR
    for filename in os.listdir(directory):
            paren1 = '('
            paren2 = ')'
            
            if(filename==".DS_Store"):
                continue
            
            file = directory + "/" + filename
            
            a = filename.split(" ")
            #print(a)
            b = a[len(a)-1].split(".")
            c = b[0][1:len(b[0])-1]
            
            department = c
            
            dataset = pandas.read_excel(file)
            array = dataset.values
            for x in array:
                #cid, dep, wint, cd, qfr, ch, cat):
                courseID = department + " " + str(x[0])
                creditHours = x[3]

                value = [courseID, department, 0, 0, 0, creditHours, ""]
                classes[courseID] = value
                
                
            
            '''file = directory + "/" + filename
            dataset = pandas.read_excel(file)
            array = dataset.values
            #game = array[:,0,1]
            game = array[:,0:1]
            
            X = array[:,2:17]
            '''
    


def main():
    #webscraping + initial user interface
    
    #return dictionary
    directory = "writing_intensive.xlsx"
    dict_wint = loadReq(directory)
    
    directory = "cultural_diversity.xlsx"
    dict_cd = loadReq(directory)
    
    directory = "writing_advanced.xlsx"
    dict_wadv = loadReq(directory)
    
    directory = "QFR.xlsx"
    dict_qfr = loadReq(directory)
    
    #print(dict_wint)
    
   
    #{"course id exp CSCI 150": course()}
    directory = "class_schedules_fall_2019"
    readClasses(directory)
    
    directory = "class_schedules_fall_2018"
    readClasses(directory)
    
    directory = "class_schedules_spring_2019"
    readClasses(directory)
    
    directory = "class_schedules_spring_2018"
    readClasses(directory)
    
    global classes
    print(classes)
    
main()