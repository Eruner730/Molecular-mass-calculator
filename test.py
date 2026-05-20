import element_masses

numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

user_input = input("Formula: ")

mass = 0

def reader(input):
    global numbers

    element = ""
    multiplier = ".."
    counter = 0
    element_found = False

    for i in input:
        if i not in numbers and element_found == False:
            element = element + i   

        elif i in numbers:
            element_found = True
            multiplier = multiplier + i

        else:
            break 
        counter = counter + 1

    if multiplier == "":
        multiplier = "1"

    while element not in element_masses.masslist.keys():
        element = element[:-1]
        counter = counter - 1
        multiplier = 1

    print(element)
    return [element, int(multiplier), int(counter)]


def calculator(element, multiplier):

    global mass

    element_mass = 0

    if element in element_masses.masslist:
        element_mass = element_masses.masslist.get(element)


    mass = mass + element_mass * multiplier


def cutter(counter):
    global user_input

    user_input = user_input[counter:]




print(reader(user_input)[2])
print(user_input)

