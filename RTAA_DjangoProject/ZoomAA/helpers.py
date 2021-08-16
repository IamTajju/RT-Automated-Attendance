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


def createContactList(summary, listOfIndices):

    # List of strings where each string is 3 contact numbers concatenated
    absenteeContactList = []
    presentContactList = []

    # Counter to access index
    AbsentCounter = 0
    PresentCounter = 0

    for list in summary:

        # Storing String in batches of 3 contacts concatented
        if ((AbsentCounter % 3 == 0) or ((AbsentCounter + PresentCounter) == (len(summary)-1))):

            # Appending to list if a batch of 3 contacts have been contenated.
            if (AbsentCounter > 0):

                # Check if this the first batch to appended
                if not absenteeContactList:
                    absenteeContactList.append(absenteeContacts3)
                    # Setting these variables to empty string for next batch of contacts
                    absenteeContacts3 = ""

                # Check if this the same batch getting duplicated
                elif ((absenteeContacts3 != absenteeContactList[-1]) and absenteeContacts3):
                    absenteeContactList.append(absenteeContacts3)
                    # Setting these variables to empty string for next batch of contacts
                    absenteeContacts3 = ""

            else:
                # Setting these variables to empty string for next batch of contacts
                absenteeContacts3 = ""

        # Repeating for present students
        if ((PresentCounter % 3 == 0) or ((AbsentCounter + PresentCounter) == (len(summary)-1))):

            if (PresentCounter > 0):

                if not presentContactList:
                    presentContactList.append(presentContacts3)
                    presentContacts3 = ""

                elif ((presentContacts3 != presentContactList[-1]) and presentContacts3):
                    presentContactList.append(presentContacts3)
                    presentContacts3 = ""

            else:
                presentContacts3 = ""

        # Ignoring filler contact
        if (list[2] == "8801734719888"):
            continue

        # If student index matches checked indexes student is absent
        if str(list[0]) in listOfIndices:

            # For first contact
            if not absenteeContacts3:
                absenteeContacts3 = absenteeContacts3 + str(list[2])
            else:
                absenteeContacts3 = absenteeContacts3 + "," + str(list[2])

            # Incrementing Absentee counter
            AbsentCounter = AbsentCounter + 1

        # Else Student is present
        else:
            # For first contact
            if not presentContacts3:
                presentContacts3 = presentContacts3 + str(list[2])
            else:
                presentContacts3 = presentContacts3 + "," + str(list[2])

            # Incrementing Present counter
            PresentCounter = PresentCounter + 1

        # Adding if any contact hasn't been appended during last iteration
        if ((AbsentCounter + PresentCounter) == (len(summary))):
            if absenteeContacts3:
                absenteeContactList.append(absenteeContacts3)
            if presentContacts3:
                presentContactList.append(presentContacts3)

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
