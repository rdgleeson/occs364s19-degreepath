#degreepath.py
#Ryan Gleeson, Jay Messina, Marouane Abra
#Last Updated: 3/26/19

import sys
from queue import PriorityQueue
import loadData
import myClasses
from loadData import classes

        

def addClassToSchedule(course, schedule, semNum, year):   #semNum is a number of what semester we are adding this class
    sem = schedule.sched[semNum]
    if sem.addClass(course, year):
        if semNum < len(schedule.sched)-1:
            schedule.sched[semNum +1].taken.add(course.cid) #adds course to next semesters taken courses
        schedule.wint -= course.wint
        schedule.cd -= course.cd
        schedule.qfr -= course.qfr
        for nextclasses in course.above:            #removing from prereq because we know we have already taken  
            nextclasses.prereqs.remove(course.cid)
        for prog in course.programs:                #remove course from program requirements
            prog.req.remove(course.cid)
        return True
    return False

def removeFromSchedule(course, schedule, semNum):
    #sem = schedule.sched[semNum]
    if semNum < len(schedule.sched)-1:
        schedule.sched[semNum+1].taken.remove(course.cid)
    schedule.wint += course.wint
    schedule.cd += course.cd
    schedule.qfr += course.qfr
    for nextclasses in course.above:
        nextclasses.prereqs.add(course.cid)
    for prog in course.programs:
        prog.req.add(course.cid)


def conflict(clas, schedule, semNum, year):
    sem = schedule.sched[semNum]
    for courseStr in sem.classes:
        try:
            course = classes[courseStr]
            coursetimes = course.days[year]
            clastimes = clas.days[year]
        except:
            continue
        for day in coursetimes.keys():
            try:
                currentTimes = coursetimes[day]
                addedTimes = clastimes[day] 
            except: #this means they dont conflict on day
                continue
            for time in currentTimes:
                for time2 in addedTimes:
                    try:
                        if (time2[0] > time[0] and time2[0] < time[1]) or (time[0] > time2[0] and time[0] < time2[1]):           #Start of added course is between the start and end of a course already in the semester 
                            course.guessed = True
                            course.conflicted.append(clas)
                    except:
                        continue
        classes[courseStr] = course
        
    
#The constraints that need to be met for our AI are:
#len(required) == 0
#schedule.wint <=  0
#schedule.cd <= 0
#schedule.qfr <= 0
#len(schedule.humanities) >= 2
#len(schedule.socialsci) >= 2
#len(schedule.natsc)i >= 2
def main():
    global classes
    semLeft = 8 #sys.argv[1]
    i = 0 #sys.argv[2]
    majorsstring = input("Enter your intended major(s)")
    majors = majorsstring.split(" ")
    minorsstring = input("Enter your intended minor(s)")
    minors = minorsstring.split(" ")
    #webscraping + initial user interface
    requiredSet = set() #set of required courses based off major(s)/minor(s) chosen
    for major in majors:
        filename = major + "_major_requirements.xlsx"
        num_total_req, course_dict, num_elec_req, electives, required_classes = loadData.readProgramRequirements(filename)
        for course in required_classes:
            requiredSet.add(course.upper())
        for course in electives:
            try:
                requiredSet.add(course.upper())
            except:
                continue
        for key in course_dict.keys():
            try:
                classes[key.upper()].prereqs = course_dict[key][0].upper().split(", ")
            except:
                continue
    #####################################################################################################
    
    programList = []
    honors = 0    #binary to determine whether to leave room senior year for honors
    requiredQ = PriorityQueue()
    programQ = PriorityQueue()
    schedule = myClasses.Schedule(semLeft, i)
    #Make priority queue of classes
    for courseStr in requiredSet:
        try:
            course = classes[courseStr]
            requiredQ.put((len(course.prereqs), courseStr))
        except:
            continue
    #CSP
    currentSem = 0 #index of what semester we are on
    j = 0 #how many classes added per semester
    while i < semLeft:
        reqnum, courseStr = requiredQ.get()
        course = classes[courseStr]
        if(reqnum == 0 and addClassToSchedule(course, schedule, i, currentSem)):
            classes[courseStr] = course
            j+=1
        elif(reqnum != 0 and j == 0): #BACKTRACK
            found = False
            while not found:
                sem = schedule.sched[i]
                if sem.guessed:
                    reqnum, courseStr = requiredQ.get()
                    course = classes[courseStr]
                    coursestr2 = sem.classes.pop(0)
                    course2 = classes[coursestr2]
                    removeFromSchedule(course2, schedule, i) #need to make
                    addClassToSchedule(course, schedule, i, currentSem)
                    classes[courseStr] = course
                    classes[coursestr2] = course2
                else:
                    courseconflict = False
                    for course1Str in sem.classes:
                        course1 = classes[course1Str]
                        if course1.guessed:
                            removeFromSchedule(course1, schedule, i)
                            classes[course1Str] = course1
                            courseconflict = True
                            break
                    if courseconflict:
                        sem.classes.remove(course1Str)
                        cc = course1.conflicted[0]
                        addClassToSchedule(cc, schedule, i, currentSem)
                        classes[cc.cid] = cc
                    else:
                        for courseStr in sem.classes:
                            course3 = classes[courseStr]
                            removeFromSchedule(course3, schedule, i)
                            classes[courseStr] = course3
                            
                            
                        sem.classes = []
                        if currentSem == 0:
                            currentSem = 3
                        else:
                            currentSem -= 1
                        i-=1
                        j=4 #remake priority queue
        elif(reqnum != 0 and j != 0):
            j = 4              #we want to change semesters
        else:
            #need to figure out what course conflicts with the one we were trying to add
            conflict(course, schedule, i, currentSem) #finds what conflicted and sets guessed to True
            j+=1
        if j == 4 or requiredQ.qsize() == 0:
            if requiredQ.qsize() != 0:
                reqnum2, course2Str = requiredQ.get()
                if reqnum2 == 0:
                    #mark as a guess
                    schedule.sched[i].guessed = True
            j = 0
            i+=1
            if currentSem == 3:
                currentSem = 0
            else:
                currentSem += 1
            #make new priorityqueue
            requiredQ = PriorityQueue()
            if i < semLeft:
                nextsem = schedule.sched[i]
                if i != semLeft-1:
                    schedule.sched[i+1].taken = nextsem.taken
                for courseStr in requiredSet:
                    if courseStr not in nextsem.taken:
                        try:
                            course = classes[courseStr]
                            for prereq in nextsem.taken:
                                if prereq in course.prereqs:
                                    course.prereqs.remove(prereq)
                            requiredQ.put((len(course.prereqs), courseStr))
                        except:
                            continue
            else:
                continue


    #After we add in the required classes to schedule
    i = 0
    for sem in schedule.sched:
        for courseStr in sem.classes:
            print(courseStr, i)
            course = classes[courseStr]
            if course.category == "hum":
                schedule.humanities.add(course.dep)
            elif course.category == "ss":
                schedule.socialsci.add(course.dep)
            else:
                schedule.natsci.add(course.dep)
        i+=1
    #Make priority queue of programs
    for prog in programList:
        programQ.put((len(prog.req), prog))
        
main()