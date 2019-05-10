#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 23:55:52 2019

@author: JayMessina
"""

import pandas
import os

classes = {}

from myClasses import Course



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
def readClasses(directory, dict_wint, dict_cd, dict_wadv, dict_qfr, year):
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
                days = x[5]


                try:
                    startTime = x[7]
                    endTime = x[8][0:(len(x[8])-2)]
                    stime = int(startTime[0:2]) + (int(startTime[2:4]))/60
                    etime = int(endTime[0:2]) + (int(endTime[2:4]))/60
                except:
                    continue

                if(endTime[4:6]=="pm" and eval(endTime[0:2])!=12):
                    etime+=12

                timeList = [days, stime, etime]
                time = {year: [days, stime, etime]}
                wint = 0
                cd = 0
                qfr = 0

                if (courseID in dict_wint or courseID in dict_wadv):
                    wint = 1
                if (courseID in dict_cd):
                    cd = 1
                if (courseID in dict_qfr):
                    qfr = 1



                if courseID in classes.keys():
                    #classes[courseID].append(time)

                    course = classes[courseID]
                    if year in course.days.keys():
                        course.days[year].append(timeList)
                    else:
                        course.days[year] = timeList

                else:
                    value = Course(courseID, department, wint, cd, qfr, creditHours, time, "")
                    classes[courseID] = value



            '''file = directory + "/" + filename
            dataset = pandas.read_excel(file)
            array = dataset.values
            #game = array[:,0,1]
            game = array[:,0:1]

            X = array[:,2:17]
            '''


def readProgramRequirements(directory):
    required_classes = set()
    electives = set()
    num_elec_req = 0
    num_total_req = 0
    course_dict = {}
    dataset = pandas.read_excel(directory)
    array = dataset.values
    #print(array)
    for item in array:
        if num_total_req == 0:
            if isinstance(item[0],int):
                num_total_req = item[0]
                continue
        if isinstance(item[0],int):
            num_elec_req = item[0]
            continue
        if num_elec_req != 0:
            electives.add(item[0]+' '+str(int(item[1])))
        if num_elec_req == 0:
            required_classes.add(item[0]+' '+str(int(item[1])))
        if item[3] == "None":
            course_dict[item[0]+' '+str(int(item[1]))] = []
        else:
            course_dict[item[0]+' '+str(int(item[1]))] = [item[3]]

    return num_total_req, course_dict, num_elec_req, electives, required_classes
    #print("the total number of required classes",num_total_req)
    #print("The prereqs are:",course_dict)
    #print(num_elec_req)
    #print("The electives are:",electives)
    #print("The required classes",required_classes)



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
    readClasses(directory, dict_wint, dict_cd, dict_wadv, dict_qfr, 2)

    directory = "class_schedules_fall_2018"
    readClasses(directory, dict_wint, dict_cd, dict_wadv, dict_qfr, 0)

    directory = "class_schedules_spring_2019"
    readClasses(directory, dict_wint, dict_cd, dict_wadv, dict_qfr, 3)

    directory = "class_schedules_spring_2018"
    readClasses(directory, dict_wint, dict_cd, dict_wadv, dict_qfr, 1)

    #print(dict_wint)

    #{"course id exp CSCI 150": course()}


    #major requirements
    #cs
    directory = "csci_major_requirements.xlsx"
    readProgramRequirements(directory)

    directory = "csci_minor_requirements.xlsx"
    readProgramRequirements(directory)

    directory = "math_minor_requirements.xlsx"
    readProgramRequirements(directory)

    print()
    global classes
    print(classes)
    #print(classes["ANTH 353"])

main()
