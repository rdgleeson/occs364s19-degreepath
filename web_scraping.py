#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 13:37:09 2019

@author: JayMessina
"""

import requests
import lxml.html as lh
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests
import openpyxl
#import datetime
import os


def main():
    url = 'http://www2.oberlin.edu/registrar/class-schedules/2019-2020/FINAL%20FALL%202019%204.19.19.rhtml.html'
  
    #Create a handle, page, to handle the contents of the website
    a = requests.get(url)
    soup = BeautifulSoup(a.text, 'lxml')
    #page = requests.get(url)
    
    L = []
    data = []
    headers = []
    for head in soup.findAll('span', {'class': 'departmentHeader'}):
        h = head.text
        headers.append(h)
        
    counter = 0
    flag = 0
    count = 0
    for p in soup.findAll('pre'):
        
        L = []
        data = []
        line = p.text
        arr = line.split("\n")
        if(len(arr[0])==0):
            continue
        else:
            newArr = []
            for i in arr:
                x = re.sub('\s+',' ', i)
                #remove first space
                #if(x[0]==" "):
                #    x = x[1:len(x)]
                    #remove last space
                if len(x)==0:
                    continue
                if(x[len(x)-1]==" "):
                    x = x[0:len(x)-1]
                    #len 11
                
                newArr.append(x)
            #first 5 so [5: len(y)-6]
            newL = []
            for item in newArr:
                if(len(item)<=10):
                    continue
                L = []
                y = item.split(" ")
                courseName = []
                professor = []
                if(y[len(y)-2]=="C"):
                    y = y[0:(len(y)-2)]
                else:
                    y = y[0:(len(y)-1)]
                for i in range(0,len(y)):
                    if(i>4 and i<len(y)-5):
                        courseName.append(y[i])
                    elif(i>len(y)-3 and i<len(y)):
                        professor.append(y[i])
                    else:
                        L.append(y[i])
                        
                    if(i == len(y)-6):
                        courseName = " ".join(courseName)
                        L.extend([courseName])
                    elif(i==len(y)-1):
                        professor = " ".join(professor)
                        L.extend([professor])
                if(L[0]!=""):
                    newL.append(L)
        
        
        if(count ==1):
            count += 1
            continue
        
        print(len(newL))
        if(len(newL)<=1):
            continue
        else:
            df = pd.DataFrame.from_records(newL)
            data.append(df)
            result = pd.concat(data)
            file = "class_schedules/" + headers[counter] + ".xlsx"
            writer = pd.ExcelWriter(file)
            result.to_excel(writer,"Sheet1")
            writer.save()
            count += 1
            counter += 1
            #if counter == 5:
            #    break
            


main()