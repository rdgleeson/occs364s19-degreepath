#degreepath.py
#Ryan Gleeson, Jay Messina, Marouane Abra
#Last Updated: 3/26/19

#an individual class
class Course():
    def __init__(self, cid, dep, wint, cd, qfr, ch):
        self.dep = dep          #department
        self.cid = cid          #course ID
        self.prereqs = []       #list of prereqs (strings of their course ID's)
        self.days = []          #2D list with inner list equal to [day, start, end]
        self.wint = wint
        self.cd = cd
        self.qfr = qfr
        self.creditHours = ch

    def __eq__(self, other):
        if self.cid == other.cid:
            return True
        else:
            return False

    def __ne__(self, ,other):
        if self.cid != other.cid:
            return True
        else:
            return False
        
#a major/minor/concentration
class Program():
    def __init__(self, title, type1):
        self.title = title      #title of program
        self.type1 = type1      #0 for major, 1 for minor, 2 for concentration
        self.req = []           #list of required classes for program
        self.cons = ""          #concentration within major ("" for minors or concentrations)


#one semester (important for time conflicts and such)        
class Semester():
    def __init__(self):
        self.classes = set()    #set of classes
        self.maxx = 16          #max credit hours unless they wanna do overtime
        self.hours = 0

    def addClass(self, clas):
        conflict = False
        for course in self.classes:
            for time in course.days:
                for time2 in clas.days:
                    if time[0] == time2[0]:
                        if time2[1] > time[1] and time2[1] < time[2]:           #Start of added course is between the start and end of a course already in the semester 
                            conflict = True
        if conflict == False and self.maxx >= (self.hours + clas.creditHours):
            self.classes.add(clas)
            self.hours += clas.creditHours

#a students schedule
class Schedule():
    def __init__(self, semLeft):
        self.semLeft = semLeft  #semesters left
        self.taken = []         #courses already taken
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
        

    
#The constraints that need to be met for our AI are:
#len(required) == 0
#schedule.wint == 0
#schedule.cd == 0
#schedule.qfr == 0
#len(schedule.humanities) >= 2
#len(schedule.socialsci) >= 2
#len(schedule.natsc)i >= 2
def main():
    #webscraping + initial user interface
    required = [] #list of required courses based off major(s)/minor(s) chosen
    honors = 0    #binary to determine whether to leave room senior year for honors

    
    
