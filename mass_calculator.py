import element_masses

mass = 0
errorSequence = ""

def reader(formula):
    global errorSequence
    element = ""
    multiplier = ""
    counter = 0
    element_found = False
    error = False
    place = -1

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
                        errorSequence = errorSequence + "1"
                        error = True

                elif i in element_masses.masslist.keys():
                        element = i
                        element_found = True

                else:
                    errorSequence = errorSequence + "2"
                    error = True
            
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


    
    return [element, int(multiplier), counter, error]

def debracketer(formula):
    error = False
    global errorSequence

    if ("(" and ")") not in formula:
        errorSequence = errorSequence + "3"
        error = True

    startPoint = formula.find("(")
    endPoint = formula.find(")")
    endBracketFound = False
    bracketMultiplier = ""
    withoutBracketMultiplier = False # Important in the end

    for ch in formula:
        if endBracketFound == True:
            try:
                int(ch)

            except ValueError:
                break

            else:
                bracketMultiplier = bracketMultiplier + str(ch)

        elif ch == ")":
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

    if insideBrackets == "":
        errorSequence = errorSequence + "4"
        error = True


    for e in insideBrackets:
        place = place + 1
        try:
            int(e)

        except ValueError:
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
                errorSequence = errorSequence + "5"
                error = True

            
     
        
        else:
            elementMultiplier = elementMultiplier + str(e)

            if (len(insideBrackets) - place) == 1: #Checks if e is the last character of inBrackets
                #if it is, and e is number, the multiplier is already found
                elementMultiplierFound = True

   
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

    return[formula, error]

def calculator(element, multiplier):

    global mass

    element_mass = 0

    element_mass = element_masses.masslist.get(element)


    mass = mass + element_mass * multiplier


def process(user_input):

    global mass
    output = ""

    while ("(" or ")") in user_input:
        print("Debracketer input: " + user_input)
        if debracketer(user_input)[1] == False:
            user_input = debracketer(user_input)[0]
        else:
            output = "Error"
            break
        print("Debracketer output: " + user_input)

    while user_input != "":
        if reader(user_input)[3] == False:
            calculator(reader(user_input)[0], reader(user_input)[1])
            print("Cutter input: " + user_input)
            user_input = user_input[reader(user_input)[2]:]
            print("Cutter output: " + user_input)
        else:
            output = "Error"
            break

    if output != "Error" :
        output = mass
    else:
        output = output + " number " + str(errorSequence)

    mass = 0

    print(output)

user_input = str(input(
"""Insert your formula, if you want to end the program, press enter
Formula: """))

while user_input != "":
    process(user_input)
    user_input = str(input("Formula: "))

print("Process ended")
