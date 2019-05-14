#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 20:26:42 2019

@author: JayMessina
"""
from loadData import classes
#an individual class
class Course():
    def __init__(self, cid, dep, wint, cd, qfr, ch, days, cat):
        self.dep = dep          #department
        self.cid = cid          #course ID
        self.prereqs = set()    #set of prereqs (strings of their course ID's)
        self.days = days       #dictionary with inner list equal to [day, start, end]
        self.wint = wint
        self.cd = cd
        self.qfr = qfr
        self.creditHours = 4
        self.category = cat     #a string of the category it is in hum, ss, ns
        self.programs = []
        self.above = []         #a list of classes that this is the prereq of
        self.guessed = False
        self.conflicted = []

    def __eq__(self, other):
        if self.cid == other.cid:
            return True
        else:
            return False

    def __ne__(self,other):
        if self.cid != other.cid:
            return True
        else:
            return False

    def __gt__(self,other):
        return True
        
    def __lt__(self, other):
        return False
        
    def __le__(self, other):
        return False
    
    def __ge__(self, other):
        return False

    def addProgram(self, prog):
        self.programs.append(prog)

    
        
#a major/minor/concentration
class Program():
    def __init__(self, title, type1):
        self.title = title      #title of program
        self.type1 = type1      #0 for major, 1 for minor, 2 for concentration
        self.req = set()        #list of required classes for program
        self.cons = ""          #concentration within major ("" for minors or concentrations)


#one semester (important for time conflicts and such)        
class Semester():
    def __init__(self):
        self.classes = []       #list of classes
        self.maxx = 16          #max credit hours unless they wanna do overtime
        self.hours = 0
        self.taken = set()      #set of classes taken !!!!!!!!! not sure we need this actually
        self.guessed = False

    def addClass(self, clas, currentsem):
        conflict = False
        try:
            for courseStr in self.classes:
                course = classes[courseStr]
                coursetimes = course.days[currentsem]
                clastimes = clas.days[currentsem]
                for day in coursetimes:
                    currentTimes = coursetimes[day]
                    try:
                        addedTimes = clastimes[day] 
                    except: #this means they dont conflict on day
                        continue
                    for time in currentTimes:
                        for time2 in addedTimes:
                            if (time2[0] > time[0] and time2[0] < time[1]) or (time[0] > time2[0] and time[0] < time2[1]):           #Start of added course is between the start and end of a course already in the semester 
                                conflict = True
            if conflict == False:
                self.classes.append(clas.cid)
                #self.hours += clas.creditHours
                return True
            return False
        except:
            return False
#a students schedule
class Schedule():
    def __init__(self, semLeft, currentsem):
        self.semLeft = semLeft  #semesters left
        self.current = currentsem  #0 for falleven, 1 for springeven, 2 for fallodd, 3 for springodd
        self.taken = set()      #courses already taken mostly for ap purposes
        self.humanities = set() #set of department in humanities
        self.socialsci = set()  #set of department in social sciences
        self.natsci = set()     #set of department in natural sciences
        self.wint = 3           #number of writing intensive courses left to take
        self.cd = 3             #number of cultural diversity courses left to take
        self.qfr = 3            #number of quantitative formal reasoning courses left to take
        self.sched = []
        for i in range(0, self.semLeft):
            sem = Semester()
            self.sched.append(sem)

    def addClassTaken(self, course):
        self.taken.append(course.cid)