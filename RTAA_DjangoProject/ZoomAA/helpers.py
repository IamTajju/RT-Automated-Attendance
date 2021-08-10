from typing import List


class userResponse:

    def __init__(self):
        self.studentNames = []
        self.counter = 0
        self.grade = 9

    def addStudentNames(self, text):
        self.studentNames = self.studentNames + text.split('\n')
        self.counter = self.counter + 1

    def setGrade(self, grade):
        self.grade = grade

    def reset(self):
        self.studentNames = []
        self.counter = 0
        self.grade = 9


'''
def compareNames(name1, name2):
    if (len(name1) < 5):
        return False

    elif (name2.find(name1) == -1):
        return False

    else:
        return True
'''


def compareNames(name1, name2):
    if (len(name1) < 5):
        return False

    l1 = name1.split()
    l2 = name2.split()

    counter = 0
    for word1 in l1:
        for word2 in l2:
            if word1.lower() == word2.lower():
                counter = counter + 1
                break

    if (counter == len(l1)) or (counter > 1):
        return True
    else:
        return False


def getPresentStudentsIndex(zoomList, dbList):

    presentStudentIndex = []

    for name in zoomList:
        for list in dbList:
            dbName = list[1]
            if(compareNames(name, dbName)):
                presentStudentIndex.append(int(list[0]))
                break

    return presentStudentIndex


def convertDayToLetter(day):

    letter = ''
    index = (day + 2) % 26

    if ((day + 2) < 26):
        letter = chr(ord('A') + index)

    else:
        buffer = chr(ord('A') + index)
        letter = 'A' + buffer

    return letter


def getRedundantColumns(ListOfList):
    redundantCols = []
    for i in range(len(ListOfList[1])):
        if (len(ListOfList[1][i]) == 0):
            redundantCols.append(i)

    return redundantCols


def contactListOfAbsentees(summary, listOfIndices):
    absenteeContactList = ""
    presentContactList = ""
    for list in summary:
        if (list[2] == "8801734719888"):
            continue
        if str(list[0]) in listOfIndices:
            if (len(absenteeContactList) == 0):
                absenteeContactList = absenteeContactList + list[2]
            else:
                absenteeContactList = absenteeContactList + "," + list[2]
        else:
            if (len(presentContactList) == 0):
                presentContactList = presentContactList + list[2]
            else:
                presentContactList = presentContactList + "," + list[2]

    return absenteeContactList, presentContactList


def cleaningList(ListOfList, redundantCols):
    while((len(ListOfList[0]) > len(ListOfList[1]))):
        ListOfList[0].pop()

    for List in ListOfList:
        counter = 0
        for index in redundantCols:
            List.pop(index - counter)
            counter = counter + 1

    return ListOfList
