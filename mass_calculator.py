import element_masses

mass = 0
errorNumber = 0

def editUserInput(user_input):
    global errorNumber
    user_input = user_input.replace("[", "(")
    user_input = user_input.replace("]", ")")
    user_input = user_input.replace(" ", "")

    if user_input.count("*") > 1:
        errorNumber += 9
        return["xxx", True]

    asterixFound = False
    asterixMultiplier = ""
    asterixMultiplierFound = False
    afterAsterix = ""

    if "*" in user_input:
        for i in user_input:
            if i == "*":
                asterixFound = True
            elif asterixFound == True:
                try:
                    int(i)

                except ValueError:
                    asterixMultiplierFound = True

                else:
                    if asterixMultiplierFound == False:
                        asterixMultiplier += str(i)

            if asterixFound == True and asterixMultiplierFound == True:
                afterAsterix += i
            
        user_input = user_input[:user_input.find("*")]
        user_input = user_input + "(" + afterAsterix + ")" + asterixMultiplier
                

    return[user_input, False]

def reader(formula):
    global errorNumber
    element = ""
    multiplier = ""
    counter = 0
    element_found = False
    place = -1

    try:
        int(formula[0])

    except ValueError:
        pass

    else:
        errorNumber += 8
        return ["x", 1, 1, True]

    for i in formula:
        place = place + 1
        try:
            i = int(i)
        except ValueError:
            if element_found == False:
                if (len(formula) - place) != 1:
                    if (i + formula[place + 1]) in element_masses.masslist.keys():
                        element = i + formula[place + 1]
                        element_found = True
                    elif i in element_masses.masslist.keys():
                        element = i
                        element_found = True
                    else:
                        errorNumber += 1
                        return ["x", 1, 1, True] #ERROR

                elif i in element_masses.masslist.keys():
                        element = i
                        element_found = True

                else:
                    errorNumber += 2
                    return ["x", 1, 1, True] #ERROR
            
            elif (len(element)) == 2 and (element[-1] == i) and place == 1: # So the loop doesn't break with the second letter of a 2 letter element
                pass
                        
            else:
                break
        else:
            element_found = True
            i = str(i)
            multiplier = multiplier + i

    counter = len(element) + len(multiplier)

    if multiplier == "":
        multiplier = 1
    
    return [element, int(multiplier), counter, False]

def debracketer(formula):
    global errorNumber

    if ("(" and ")") not in formula:
        errorNumber += 3
        return["error", True]

    if formula.count("(") != formula.count(")"):
        errorNumber += 6
        return["error", True]
    
    checkForOpenBracket = 0
    checkForCloseBracket = 0

    for ch in formula:
        if ch == "(":
            checkForOpenBracket += 1
        
        if ch == ")" and checkForCloseBracket < checkForOpenBracket:
            checkForCloseBracket += 1

        elif ch == ")" and checkForCloseBracket == checkForOpenBracket:
            errorNumber += 7
            return["error", True]


    startPoint = 0
    endPoint = 0
    point = -1
    endBracketFound = False
    startBracketFound = False
    bracketMultiplier = ""
    withoutBracketMultiplier = False # Important in the end
    numberOfBrackets = formula.count("(")
    numberOfIncludedBrackets = 0
    numberOfBracketsFound = 0

    for ch in formula:
        point += 1

        if endBracketFound == True and startBracketFound == True:
            try:
                int(ch)

            except ValueError:
                break

            else:
                bracketMultiplier = bracketMultiplier + str(ch)


        if ch == "(" and startBracketFound == True: ### Count how many brackets is in the "main" bracket
            numberOfIncludedBrackets += 1

        elif ch == "(" and startBracketFound == False:
            startPoint = point
            startBracketFound = True

        if ch == ")" and numberOfIncludedBrackets > numberOfBracketsFound: ### Bracket
            numberOfBracketsFound += 1

        elif ch == ")" and numberOfIncludedBrackets == numberOfBracketsFound:
            endPoint = point
            endBracketFound = True



    if bracketMultiplier == "":
        withoutBracketMultiplier = True
        bracketMultiplier = 1

    else:
        bracketMultiplier = int(bracketMultiplier)

    ###################
    # The end of inBracket and bracketMultiplier finder function 


    insideBrackets = formula[startPoint+1:endPoint] # text inside brackets
    replaceWith = ""
    element = ""
    elementMultiplier = ""
    place = -1
    elementFound = False
    elementMultiplierFound = False
    bracketOpened = False
    bracketClosed = False

    if insideBrackets == "":
        errorNumber += 4
        return[formula, True]


    for e in insideBrackets:
        place = place + 1
        try:
            int(e)

        except ValueError:

            if bracketOpened == True and bracketClosed == True:
                elementMultiplierFound = True
                elementMultiplier = 1
            
            if e == "(":
                bracketOpened = True

            elif e == ")":
                bracketClosed = True

            if bracketOpened == True and bracketClosed == False:
                element = element + e

            if bracketOpened == False and bracketClosed == False: #### So brackets don't break the already working code for elements without them

                if (elementFound == True) and e != element[-1]: 
                    # Checks if the letter isn't part of a 2 letter element, that't been detected in the last cycle
                # If it isn't, it means that the element that the coeficient was already found or that there wasn't a coeficient mentioned - it's 1
                    elementMultiplierFound = True

                elif (elementFound == True) and (e == element[-1]) and ((len(insideBrackets) - place) != 1): # Prevents error message when e is a part of a 2 letter element ... see above 
                    #len.. added because otherwise it checks of for 1 letter elements automatically              
                    pass

                elif (elementFound == True) and (e == element[-1]) and ((len(insideBrackets) - place) == 1): #So it works when the insideBrackets ends with a 2 letter element
                    elementMultiplierFound = True
                

                elif (len(insideBrackets) - place) != 1: # Checks if e isn't the last character of inBrackets - prevents out of range error

                    if (elementMultiplierFound == False) and (e + insideBrackets[place + 1] in element_masses.masslist.keys()): #Detects 2 letter elements
                        element = e + insideBrackets[place + 1]
                        elementFound = True

                    elif (elementMultiplierFound == False) and (e in element_masses.masslist.keys()): #Detects 1 letter elements
                        element = e
                        elementFound = True

                elif (elementFound == False) and (elementMultiplierFound == False) and (e in element_masses.masslist.keys()): #Detects 1 letter elements
                    element = e
                    elementFound = True

                else:
                    errorNumber += 5
                    return[formula, True]
 
        else:
            if bracketOpened == True and bracketClosed == False:
                element = element + e
            else:
                elementMultiplier = elementMultiplier + str(e)

            if (len(insideBrackets) - place) == 1: #Checks if e is the last character of inBrackets
                #if it is, and e is number, the multiplier is already found
                elementMultiplierFound = True

        if bracketOpened == True and bracketClosed == True and (len(insideBrackets) - place) == 1: ### So it works when the formula ends with a )
            elementMultiplierFound == True

        if bracketOpened == True and bracketClosed == True and elementMultiplierFound == True: #### When bracket is ended and the multiplier of it is found

            replaceWith = replaceWith + element + ")" + elementMultiplier
            elementFound = False
            elementMultiplierFound = False
            element = ""
            elementMultiplier = ""
            bracketOpened = False
            bracketClosed = False
   
        elif bracketOpened == False and bracketClosed == False: #### So brackets don't break the already working code for elements without them

            if elementFound == True and (len(insideBrackets) - place == 1) and place == 0: # So it works if the is only 1 character inside brackets
                elementMultiplierFound = True


            if ((elementFound == True) and (elementMultiplierFound == True)):
                if elementMultiplier != "":
                    replaceWith = replaceWith + element + str(int(elementMultiplier) * int(bracketMultiplier))

                else: # When the coeficient isn't mentioned - it is 1
                    replaceWith = replaceWith + element + str(bracketMultiplier)
                # Resets the loop

                elementFound = False
                elementMultiplierFound = False
                element = ""
                elementMultiplier = ""

                # NOW the loop should be in an element -> I need to detect it - same code as above 
                # or it's in the multiplier - inBrackets ends with a digit

                if (len(insideBrackets) - place) != 1: 

                    if e + insideBrackets[place + 1] in element_masses.masslist.keys():
                        element = e + insideBrackets[place + 1]
                        elementFound = True

                    elif (elementMultiplierFound == False) and (e in element_masses.masslist.keys()): 
                        element = e
                        elementFound = True

                elif e in element_masses.masslist.keys():
                    element = e
                    elementFound = True

                else: 
                    try: # For error to not occur if inBrackets ended with a digit
                        int(e)
                    except ValueError:
                        pass

                if (elementFound == True) and ((len(insideBrackets) - place) == 1) and place != 0: # Prevents duplication if it's the first and only character inside brackets
                    # If the last character is an element
                    # It's an element with a coeficient of 1
                    replaceWith = replaceWith + element + str(bracketMultiplier)


    #############
    # The end of inBracket changer function 

    if withoutBracketMultiplier == False:
        # It's because at the start, when the bracketMultiplier is "", it changes to 1, but len("") in nothing and len("1") is one
        # Without this, if bracketMultiplier is "", the following code cuts the next letter/number
    
        formula = formula[:endPoint+1] + formula[endPoint+1 + len(str(bracketMultiplier)):]
        formula = formula.replace(formula[startPoint:endPoint+1], replaceWith, 1)

    else:
        formula = formula[:endPoint+1] + formula[endPoint+1:]
        formula = formula.replace(formula[startPoint:endPoint+1], replaceWith, 1)

    return[formula, False]

def calculator(element, multiplier):

    global mass

    element_mass = 0

    element_mass = element_masses.masslist.get(element)


    mass = mass + element_mass * multiplier


def process(user_input):

    global mass
    output = ""

    if editUserInput(user_input)[1] == True:
        output = "Error"
    else:
        user_input = editUserInput(user_input)[0]

    while (("(" or ")") in user_input) and (output == ""):
        
        if debracketer(user_input)[1] == False:
            user_input = debracketer(user_input)[0]
        else:
            output = "Error"
            break
       
    while user_input != "" and output == "":
        if reader(user_input)[3] == False:
            calculator(reader(user_input)[0], reader(user_input)[1])
            
            user_input = user_input[reader(user_input)[2]:]
           
        else:
            output = "Error"
            break

    if output != "Error" :
        output = mass
    else:
        output = output + " number " + str(errorNumber)

    mass = 0

    print(output)

user_input = str(input(
"""Insert your formula, if you want to end the program, press enter
Formula: """))

while user_input != "":
    process(user_input)
    user_input = str(input("Formula: "))

print("Process ended")
