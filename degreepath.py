#degreepath.py
#Ryan Gleeson, Jay Messina, Marouane Abra
#Last Updated: 3/26/19

import sys
import copy
from queue import PriorityQueue
import pandas


        

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
        programQ.put((len(prog.req), prog))
        
main()