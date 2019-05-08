#degreepath.py
#Ryan Gleeson, Jay Messina, Marouane Abra
#Last Updated: 3/26/19

import sys
import copy
from queue import PriorityQueue
import pandas

#an individual class
class Course():
    def __init__(self, cid, dep, wint, cd, qfr, ch, cat):
        self.dep = dep          #department
        self.cid = cid          #course ID
        self.prereqs = set()    #set of prereqs (strings of their course ID's)
        self.days = {}          #dictionary with inner list equal to [day, start, end]
        self.wint = wint
        self.cd = cd
        self.qfr = qfr
        self.creditHours = ch
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
        for course in self.classes:
            coursetimes = course.days[currentsem]
            clastimes = clas.days[currentsem]
            for time in coursetimes:  
                for time2 in clas.days:
                    if time[0] == time2[0]:
                        if time2[1] > time[1] and time2[1] < time[2]:           #Start of added course is between the start and end of a course already in the semester 
                            conflict = True
        if conflict == False and self.maxx >= (self.hours + clas.creditHours):
            self.classes.append(clas)
            self.hours += clas.creditHours
            return True
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
        

def addClassToSchedule(course, schedule, semNum):   #semNum is a number of what semester we are adding this class
    sem = schedule.sched[semNum]
    if sem.addClass(course):
        if semNum < len(schedule.sched)-1:
            self.sched[semNum +1].taken.add(course) #adds course to next semesters taken courses
        schedule.wint -= course.wint
        schedule.cd -= course.cd
        schedule.qfr -= course.qfr
        for nextclasses in course.above:            #removing from prereq because we know we have already taken  
            nextclasses.prereqs.remove(course)
        for prog in course.programs:                #remove course from program requirements
            prog.req.remove(course)
        return True
    return False

def removeFromSchedule(course, schedule, semNum):
    sem = schedule.sched[semNum]
    if semNum < len(schedule.sched)-1:
        self.sched[semNum+1].taken.remove(course)
    schedule.wint += course.wint
    schedule.cd += course.cd
    schedule.qfr += course.qfr
    for nextclasses in course.above:
        nextclasses.prereqs.add(course)
    for prog in course.programs:
        prog.req.add(course)


def conflift(clas, schedule, semNum):
    sem = schedule.sched[semNum]
    for course in sem.classes:
        coursetimes = course.days[currentsem]
        clastimes = clas.days[currentsem]
        for time in coursetimes:  
            for time2 in clas.days:
                if time[0] == time2[0]:
                    if time2[1] > time[1] and time2[1] < time[2]:           #Start of added course is between the start and end of a course already in the semester 
                        course.guessed = True
                        course.conflicted.append(clas)
    

    
#The constraints that need to be met for our AI are:
#len(required) == 0
#schedule.wint <=  0
#schedule.cd <= 0
#schedule.qfr <= 0
#len(schedule.humanities) >= 2
#len(schedule.socialsci) >= 2
#len(schedule.natsc)i >= 2
def main():
    semLeft = sys.argv[1]
    currentsem = sys.argv[2]
    majorsstring = input("Enter your intended major(s)")
    majors = majorsstring.split(" ")
    minorsstring = input("Enter your intended minor(s)")
    minors = minorsstring.split(" ")
    #webscraping + initial user interface
    
    
    for filename in os.listdir(directory):
        if(filename==".DS_Store"):
            continue
        print(filename)
        file = directory + "/" + filename
        dataset = pandas.read_excel(file, names=names)
        array = dataset.values
        #game = array[:,0,1]
        game = array[:,0:1]
        
        X = array[:,2:17]
    
    
    
    #####################################################################################################
    requiredSet = set() #set of required courses based off major(s)/minor(s) chosen
    programList = []
    honors = 0    #binary to determine whether to leave room senior year for honors
    requiredQ = PriorityQueue()
    programQ = PriorityQueue()
    schedule = Schedule(semLeft, currentsem)
    #Make priority queue of classes
    for course in requiredList:
        requiredQ.put((len(course.prereqs), course))
    #CSP
    i = 0 #index of what semester we are on
    j = 0 #how many classes added per semester
    while requiredQ.qsize() != 0:
        reqnum, course = requiredQ.get()
        if(reqnum == 0 and addClassToSchedule(course, schedule, i)):
            print("class added")
            j+=1
        elif(reqnum != 0 and j == 0): #BACKTRACK
            print("need to backtrack")
            found = False
            while not found:
                sem = schedule.sched[i]
                if sem.guessed:
                    reqnum, course = requiredQ.get()
                    removeFromSchedule(sem.classes.pop(0), schedule, i) #need to make
                    addClassToSchedule(course, schedule, i)
                else:
                    courseconflict = False
                    for course1 in sem.classes:
                        if course1.guessed:
                            removeFromSchedule(course1, schedule, i)
                            courseconflict = True
                            break
                    if courseconflict:
                        sem.classes.remove(course1)
                        addClassToSchedule(course1.conflicted[0], schedule, i)
                    else:
                        for course in sem.classes:
                            removeFromSchedule(course, schedule, i)
                        sem.classes = []
                        i-=1
                        j=4 #remake priority queue
                            
        elif(reqnum != 0 and j != 0):
            j = 4              #we want to change semesters
        else:
            #need to figure out what course conflicts with the one we were trying to add
            print("time to guess")
            conflict(course, schedule, i) #finds what conflicted and sets guessed to True
            j+=1
        if j == 4:
            reqnum2, course2 = requiredQ.get()
            if reqnum2 == 0:
                #mark as a guess
                schedule.sched[i].guessed = True
            j = 0
            i+=1
            #make new priorityqueue
            requiredQ = PriorityQueue()
            if i < semLeft:
                nextsem = schedule.sched[i]
                for course in requiredList:
                    if course not in nextsem.taken:
                        requiredQ.put((len(course.prereqs), course))
            


    #After we add in the required classes to schedule
    for sem in schedule.sched:
        for course in sem:
            if course.category == "hum":
                schedule.humanities.add(course.dep)
            elif course.category == "ss":
                schedule.socialsci.add(course.dep)
            else:
                schedule.natsci.add(course.dep)
    #Make priority queue of programs
    for prog in programList:
        programQ.put((len(prog.req), prog)

    
    
