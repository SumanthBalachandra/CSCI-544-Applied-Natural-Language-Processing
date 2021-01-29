from fst import FST
import string, sys
from fsmutils import composechars, trace


def letters_to_numbers():
    """
    Returns an FST that converts letters to numbers as specified by
    the soundex algorithm
    """
    classOne = ['a', 'e', 'h', 'i', 'o', 'u', 'w', 'y', 'A', 'E', 'H', 'I', 'O', 'U', 'W', 'Y']
    classTwo = ['b', 'f', 'p', 'v', 'B', 'F', 'P', 'V']
    classThree = ['c', 'g', 'j', 'k', 'q', 's', 'x', 'z', 'C', 'G', 'J', 'K', 'Q', 'S', 'X', 'Z']
    classFour = ['d', 't', 'D', 'T']
    classFive = ['l', 'L']
    classSix = ['m', 'n', 'M', 'N']
    classSeven = ['r', 'R']

    # Let's define our first FST
    f1 = FST('soundex-generate')

    # Indicate that '1' is the initial state
    f1.add_state('start')
    f1.add_state('classOne')
    f1.add_state('classTwo')
    f1.add_state('classThree')
    f1.add_state('classFour')
    f1.add_state('classFive')
    f1.add_state('classSix')
    f1.add_state('classSeven')

    f1.initial_state = 'start'

    # Set all the final states
    f1.set_final('classOne')
    f1.set_final('classTwo')
    f1.set_final('classThree')
    f1.set_final('classFour')
    f1.set_final('classFive')
    f1.set_final('classSix')
    f1.set_final('classSeven')

    finalStates = ['classOne', 'classTwo', 'classThree', 'classFour', 'classFive', 'classSix', 'classSeven']
    finalStatesList = [classOne, classTwo, classThree, classFour, classFive, classSix, classSeven]
    valueList = ['', '1', '2', '3', '4', '5', '6']
    # Add the rest of the arcs

    #for letter in string.ascii_letters:
        #f1.add_arc('start', 'intermediate', (letter), (letter))

    for i in range(10):
        f1.add_arc('start', 'start', (str(i)), ())
    for state, stateList, value in zip(finalStates, finalStatesList, valueList):
        f1 = addStates(state, stateList, finalStates, value, f1)

    return f1

    # The stub code above converts all letters except the first into '0'.
    # How can you change it to do the right conversion?
def addStates(state, stateList, finalStates, value, f1):
    for states in finalStates:
        for character in stateList:
            #f1.add_arc('intermediate', state, (character), (value))
            f1.add_arc('start', state, (character), (character))
            if state == states:
                f1.add_arc(state, state, (character), (''))
            else:
                f1.add_arc(states, state, (character), (value))
    return f1

def truncate_to_three_digits():
    """
    Create an FST that will truncate a soundex string to three digits
    """

    # Ok so now let's do the second FST, the one that will truncate
    # the number of digits to 3
    f2 = FST('soundex-truncate')

    # Indicate initial and final states
    f2.add_state('initial')
    f2.add_state('firstDigit')
    f2.add_state('secondDigit')
    f2.add_state('thirdDigit')

    f2.initial_state = 'initial'

    f2.set_final('initial')
    f2.set_final('firstDigit')
    f2.set_final('secondDigit')
    f2.set_final('thirdDigit')

    source = ['initial', 'firstDigit', 'secondDigit', 'thirdDigit']
    destination = ['firstDigit', 'secondDigit', 'thirdDigit', 'thirdDigit']

    # Add the arcs
    for letter in string.letters:
        f2.add_arc('initial', 'initial', (letter), (letter))

    for cur, next in zip(source, destination):
        f2 = addTruncateStates(cur, next, f2)

    return f2

    # The above stub code doesn't do any truncating at all -- it passes letter and number input through
    # what changes would make it truncate digits to 3?
def addTruncateStates(source, destination, f2):
    for i in range(10):
        if source != destination:
            f2.add_arc(source, destination, (str(i)), (str(i)))
        else:
            f2.add_arc(source, destination, (str(i)), ())
    return f2

def add_zero_padding():
    # Now, the third fst - the zero-padding fst
    f3 = FST('soundex-padzero')

    f3.add_state('1')
    f3.add_state('1a')
    f3.add_state('1b')
    f3.add_state('1c')
    f3.add_state('1d')
    f3.add_state('2')

    f3.initial_state = '1'
    f3.set_final('2')

    for letter in string.letters:
        f3.add_arc('1', '1', (letter), (letter))
    for number in xrange(10):
        f3.add_arc('1', '1a', (str(number)), (str(number)))
        f3.add_arc('1a', '1b', (str(number)), (str(number)))
        f3.add_arc('1b', '2', (str(number)), (str(number)))

    f3.add_arc('1', '1c', (), ('0'))
    f3.add_arc('1c', '1d', (), ('0'))
    f3.add_arc('1d', '2', (), ('0'))

    f3.add_arc('1a', '1d', (), ('0'))
    f3.add_arc('1b', '2', (), ('0'))

    return f3

    # The above code adds zeroes but doesn't have any padding logic. Add some!


if __name__ == '__main__':
    user_input = raw_input().strip()
    f1 = letters_to_numbers()
    f2 = truncate_to_three_digits()
    f3 = add_zero_padding()

    if user_input:
        print("%s -> %s" % (user_input, composechars(tuple(user_input), f1, f2, f3)))