import element_masses

user_input = input("Formula: ")

mass = 0

def reader(formula):

    element = ""
    multiplier = ""
    counter = 0
    element_found = False
    error = False
    
    for i in formula:
        try:
            i = int(i)
        except ValueError:
            if element_found == False:
                element = element + i
                counter = counter + 1

            else:
                break
        else:
            element_found = True
            i = str(i)
            multiplier = multiplier + i
            counter = counter + 1


    if element not in element_masses.masslist.keys():
        counter = counter - len(multiplier)
        multiplier = 1

    while element not in element_masses.masslist.keys():
        element = element[:-1]
        counter = counter - 1
        if element == "":
            error == True
            break


    if multiplier == "":
        multiplier = 1

    
    return [element, int(multiplier), counter, error]


def calculator(element, multiplier):

    global mass

    element_mass = 0

    if element in element_masses.masslist:
        element_mass = element_masses.masslist.get(element)


    mass = mass + element_mass * multiplier


def cutter(counter):
    global user_input

    user_input = user_input[counter:]


if user_input != "":
    calculator(reader(user_input)[0],reader(user_input)[1])
    cutter(reader(user_input)[2])


print(mass)