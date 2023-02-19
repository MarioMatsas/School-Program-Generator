from random import randrange, sample
import csv
from time import sleep
from copy import deepcopy


#All the subjects of each class and their respective teachers
data = [
{
    'Al':'Al1',
    'C':'C1',
    'L':'L1',
    'En':'En1',
    'R':'R1',
    'Li':'Li1',
    'Ch':'Ch1',
    'B':'B1',
    'An':'An1',
    'Ger':'Ger1',
    'Pe':'Pe1',
    'G':'Geo1',
    'H':'H1',
    'P':'P1'
},
{
    'Al':'Al2',
    'C':'C1',
    'L':'L2',
    'En':'En1',
    'R':'R1',
    'Li':'Li2',
    'Ch':'Ch1',
    'B':'B1',
    'An':'An2',
    'Ger':'Ger1',
    'Pe':'Pe1',
    'G':'Geo2',
    'H':'H1',
    'P':'P1'
}
,
{
    'Al':'Al1',
    'C':'C1',
    'L':'L3',
    'En':'En1',
    'R':'R1',
    'Li':'Li3',
    'Ch':'Ch1',
    'B':'B1',
    'An':'An3',
    'Ger':'Ger1',
    'Pe':'Pe1',
    'G':'Geo3',
    'H':'H1',
    'P':'P1'
}
]


subjects = [[['Al','Al','Al','G','G','An','An','An','An','Ch','Ch','L','L','Li','Li','B','B','C','C','C'],['Al','Al','Al','G','G','An','An','An','An','Ch','Ch','L','L','Li','Li','B','B','C','C','C'],['Al','Al','Al','G','G','An','An','An','An','Ch','Ch','L','L','Li','Li','B','B','C','C','C']],[['Ger','Ger','En','En','R','R','Pe','Pe','H','H','P','P'],['Ger','Ger','En','En','R','R','Pe','Pe','H','H','P','P'],['Ger','Ger','En','En','R','R','Pe','Pe','H','H','P','P']]]

lessons = [[['Al','L','G','Ch','B','An','Li','C'],['Al','L','G','Ch','B','An','Li','C'],['Al','L','G','Ch','B','An','Li','C']],[['Ger','En','R','Pe','H','P'],['Ger','En','R','Pe','H','P'],['Ger','En','R','Pe','H','P']]]

programms = [[],[],[]]

programms_list = [[],[],[]]

hour = [sample([7, 7, 6, 6, 6], 5),sample([7, 7, 6, 6, 6], 5),sample([7, 7, 6, 6, 6], 5)]

header = "Days, 1st, 2nd, 3rd, 4th, 5th, 6th, 7th"
days = ['M','T','W','T','F']

#generates every class's daily programme
def dailyProgramme(class_number, day):
    #adds subject into the main list
    for p in range(hour[class_number - 1][day]):
        """
        we chose an index so we can place the most important subjects at the start of the day and secondary ones later on
        """
        index = 0 if p <4 else 1
        #chooses random subject
        ch = randrange(len(subjects[index][class_number - 1]))
        #appends it to the class programm and removes it from the subjects list, so as to not use it more than allowed
        programms[class_number - 1].append(subjects[index][class_number - 1][ch])
        subjects[index][class_number - 1].remove(subjects[index][class_number - 1][ch])
        #create deepcopy of the list and append it to the class's programm
        programme_copy = deepcopy(programms[class_number - 1])
    """
    The use of a deepcopy comes into play when we use the makeCorrections function, since we always want to compare
    one element of each class's programm's list the moment we add it, so it makes sence to clear the programms each time
    and use a deep copy to append each part of the programm list so corrections can be made immediately
    """  
    programms_list[class_number - 1].append(programme_copy)
    programms[class_number - 1].clear()

def generateProgramme(i):
    #generate 1st class's programme
    dailyProgramme(1, i)
    #generate 2nd class's programme
    dailyProgramme(2, i)
    #generate 3rd class's programme
    dailyProgramme(3, i)


def makeCorrections(i, classNumber):
    global count
    global minimumTime
    #k depends by the number of classes since each class number will have to be compred to (its number - 1) other classes
    for k in range(classNumber - 1):
        #Track how many hours have differnt sumbjects/ techers at the same hour
        count = 0
        #hour comparisons depend on the class with less hours between the 2 compared
        minimumTime = min(hour[classNumber - 2 - k ][i], hour[classNumber - 1][i])
        for _ in range(minimumTime):
            """
            similarely to before, we chose an index so the changes we make to each subject corresponds to whether that subject is a primary
            or a secondary one
            """
            index = 0 if _ < 4 else 1
            #compare if 2 classes have the same the same lesson at the same time
            if programms_list[classNumber - 2 - k ][i][_] == programms_list[classNumber - 1][i][_]:
                #check if that lesson is taught by the same professor
                if data[classNumber - 2 - k ][programms_list[classNumber - 2 - k ][i][_]] == data[classNumber - 1][programms_list[classNumber - 1][i][_]]:
                    #if so, we remove that lesson from the possible choices
                    try: lessons[index][classNumber - 1].remove(programms_list[classNumber - 1][i][_])
                    except: pass
                    #and add it back to the subjects list, so it can be choses later (when it gets the chance)
                    subjects[index][classNumber - 1].append(programms_list[classNumber - 1][i][_])
                    #make changes to lessons so that they contain only the subjects that have yet to be used up
                    lessons[index][classNumber - 1] = list(set(subjects[index][classNumber - 1]))
                    #then we choose a new random subject from the lessons list (excluding the one we removed)
                    choice = randrange(len(lessons[index][classNumber - 1]))
                    #we add it to the class's programm list
                    programms_list[classNumber - 1][i][_] = lessons[index][classNumber - 1][choice]
                    #we remove it from the subjects list so we dont choose it again
                    subjects[index][classNumber - 1].remove(programms_list[classNumber - 1][i][_])
                    #and we append it back to the lessons list so it can be used later
                    lessons[index][classNumber - 1].append(programms_list[classNumber - 2 - k ][i][_])
                    #make changes to lessons so that they contain only the subjects that have yet to be used up
                    lessons[index][classNumber - 1] = list(set(subjects[index][classNumber - 1]))
                else:
                    count += 1
            else:
                count += 1


def bringTogether(i, classNumber):
    #Seperate the priority subjects from the rest
    firstPart = programms_list[classNumber - 1][i][:4] #Priority subjects
    secondPart = programms_list[classNumber - 1][i][4:]
    #Place same subjects in consecutive positions
    firstPart.sort()
    secondPart.sort()
    finalResult = firstPart + secondPart
    #Apply changes
    programms_list[classNumber - 1][i] = finalResult


def overallCorrections(i, classNumber):
    searchforIniniteloop = 0
    #Checks whether the changes applied result in a programm with no overlapping subjects and/ or teachers
    while count < minimumTime:
        bringTogether(i, classNumber) 
        makeCorrections(i, classNumber)
        searchforIniniteloop += 1
        """
        In case of an infinite (indicated by the continuous repetition of the 2 functions above) loop caused by the fact that no changes 
        resulting in a "correct" programm can be made, the programm will only apply the pure corrections, without necessarily placing the
        same subjects next to one another
        """
        if searchforIniniteloop > 10:
            makeCorrections(i, classNumber)
            break
            

def runProgramm(choice):
    global count
    for i in range(5):
        #Create the programm prototypes
        generateProgramme(i)
        #Complete the first one
        if choice == 1:
            bringTogether(i, 1)
        #Apply all the chosen corrections to the rest
        makeCorrections(i, 2)
        if choice == 1:
            count = 0
            overallCorrections(i, 2)          
        makeCorrections(i, 3)
        if choice == 1:
            count = 0
            overallCorrections(i, 3)
        
    print("\n-----------------------\n")
    print(programms_list[0])
    print(programms_list[1])
    print(programms_list[2])
    print("\n-----------------------\n")
    

def add_to_file(classNumber):
    with open('Programme.csv', 'a') as f:
        f.write(f'\nClass {classNumber}\n')
        for i in range(5):
            if len(programms_list[classNumber - 1][i]) == 7:
                f.write(f'{days[i]}, {programms_list[classNumber - 1][i][0]}, {programms_list[classNumber - 1][i][1]}, {programms_list[classNumber - 1][i][2]}, {programms_list[classNumber - 1][i][3]}, {programms_list[classNumber - 1][i][4]},{programms_list[classNumber - 1][i][5]}, {programms_list[classNumber - 1][i][6]}\n')
            else:
                f.write(f'{days[i]}, {programms_list[classNumber - 1][i][0]}, {programms_list[classNumber - 1][i][1]}, {programms_list[classNumber - 1][i][2]}, {programms_list[classNumber - 1][i][3]}, {programms_list[classNumber - 1][i][4]}, {programms_list[classNumber - 1][i][5]}\n')


def save_info():
    with open('Programme.csv', 'w') as f:
        f.write(f'{header}\n')
    add_to_file(1)
    add_to_file(2)
    add_to_file(3)
  
                
def main():
    user_choice = input("Would you like to include place the same subjects in consecutive hours?\nPress 'Yes' or 'No': ")
    if user_choice.title() == 'No':
        runProgramm(0)
    elif user_choice.title() == 'Yes':
        runProgramm(1)
    save_info()

if __name__ == '__main__':
    main()


