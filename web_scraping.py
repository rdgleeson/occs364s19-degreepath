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
    #url = 'http://www2.oberlin.edu/registrar/class-schedules/2019-2020/FINAL%20FALL%202019%204.19.19.rhtml.html'
    #url = 'http://www2.oberlin.edu/registrar/class-schedules/2018-2019/FINAL%20FALL%202018%2010.31.rhtml.html'
    url = 'http://www2.oberlin.edu/registrar/class-schedules/2017-2018/FINAL%20SPRING%202018%202.9.18.rhtml.html'
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
                #print("here", len(x))
                
                    
                if len(x)==0:
                    continue
                if(x[len(x)-1]==" "):
                    x = x[0:len(x)-1]
                    #len 11
                
                newArr.append(x)
            #first 5 so [5: len(y)-6]
            newL = []
            number = ""
            for item in newArr:
                try:
                    
                    if(item[0]==" "):
                        item = number + item
                    else:
                        number = item[0:3]
                except:
                    number=number
                try:
                    item = item.replace("-", " ") 
                    #print(item)
                    
                except:
                    item=item
                    
                #number = item[0]
                #print("here ", item)
                if(len(item)<=1):
                    continue
                #print(item[0:4])
                if(item[0:4]=='NUMB'):
                    continue
                
                L = []
                y = item.split(" ")
                print(y)
                courseName = []
                professor = []
                if(y[len(y)-2]=="C"):
                    y = y[0:(len(y)-2)]
                else:
                    y = y[0:(len(y)-1)]
                for i in range(0,len(y)):
                    if(i>4 and i<len(y)-7):
                        courseName.append(y[i])
                    elif(i>len(y)-3 and i<len(y)):
                        professor.append(y[i])
                    else:
                        L.append(y[i])
                        
                    if(i == len(y)-7):
                        courseName = " ".join(courseName)
                        L.extend([courseName])
                    elif(i==len(y)-1):
                        professor = " ".join(professor)
                        L.extend([professor])
                if(L[0]!=""):
                    newL.append(L)
            
        if(len(newL)==0 or newL[0][0]=='NUMB'):
            #print(newL)
            continue
        
        if(newL[0][0]=='EXTRA'):
            break
        
        #french, or latin american studies or middle east
        #fall 2019
        '''
        if(count ==3 or count == 17 or count == 18 or count == 24 or count ==37 or count ==39 or count == 45):
            counter+=1
        if (count == 17):
            count+=1
            continue
        
        if (count == 50):
            counter+=1
            count += 1
            print("here")
            continue
        
        print(count)
        '''
        #fall 2018
        '''
        if(count ==3 or count==30 or count==35 or count == 36 or count ==40 or count==41 or count ==44):
            counter+=1
            print(len(headers[counter]))
        if(count==17):
            count+=1
            counter+=2
        '''
        #spring 2019
        '''
        if(count==3 or count ==17 or count==18 or count==21 or count==29 or count ==34 or count ==35 or count ==41):
            counter+=1
        if (count == 17):
            count+=1
            continue
        '''
        if(count==28 or count==37 or count==38 or count ==44 or count ==49):
            counter+=1
        print(len(newL), headers[counter])
        print(count)
        if(headers[counter]=='\xa0' or headers[counter]=='This program does not regularly offer courses in MENA. Please see the online catalog for a list of courses offered in other departments that apply toward this minor.'):
            counter+=1
        if(len(newL)==0):
            continue
        else:
            df = pd.DataFrame.from_records(newL)
            data.append(df)
            result = pd.concat(data)
            file = "class_schedules_spring_2018/" + headers[counter] + ".xlsx"
            writer = pd.ExcelWriter(file)
            result.to_excel(writer,"Sheet1")
            writer.save()
            count += 1
            counter += 1
            #if counter == 5:
            #    break
            


main()