import sys

# get_section: function that returns the lines of a specific section in the input file
# it is used to separate sections (sigma, states, transitions)
def getSection(name, l_gen):
    flag = False
    lRet = []

    for line in l_gen:
        if line == name + ":":   # the beginning of the section
            flag = True
            continue
        if line == "end":        # the end of the section
            flag = False
        if flag == True:         # if we have not reached the end of the section,
            lRet.append(line)   # we append the line of the file to the list

    return lRet

# load_dfa_from_file: function that uses the get_section function, to load the sections of a DFA config file
# and return them in lists, together with an error code if the file is not valid
def loadDfaFromFile(fileName):
    lGen = []
    errorCode = 0

    file = open(fileName)

    for line in file:
        line = line.strip().lower()
        if len(line) > 0 and line[0] != "#":    # we create a list from the input file only with the
            lGen.append(line)                   # lines that are different from comments
                                                # sp we can  pass it to the get_section function

    listSigma = getSection("sigma", lGen)               # getting the alphabet of the DFA from the config file
    listStates = getSection("states", lGen)             # getting the states of the DFA from the config file
    listTransitions = getSection("transitions", lGen)   # getting the transitions of the DFA from the config file

    listStatesEx = []

    for state in listStates:                    # finding the start and the final states
        tmp = state.split(",")
        tmpState = []
        tmpState.append(tmp[0])
        isStartState = 0
        isFinalState = 0
        for entry in tmp[1:]:
            if entry == "f":                    # if the state is final
                isFinalState = 1
            if entry == "s":                    # if the state is a start state
                isStartState = 1
        tmpState.append(isStartState)
        tmpState.append(isFinalState)
        listStatesEx.append(tmpState)           # if the state is neither a final, nor a start state, we append it
                                                # to the extended states list followed by two zeros

    listStates = []

    for state in listStatesEx:
        listStates.append(state[0])             # putting only the state in the list of states

    # if a section is null, we generate the error code 1
    if len(listSigma) == 0 or len(listStates) == 0 or len(listTransitions) == 0:
        errorCode = 1

    # validating the transitions section of the DFA config file
    transFlag = True
    listTransitionsEx=[]
    for trans in listTransitions:               # if the first word of the transition is not a state, or the second
        tmp = trans.split(",")                  # is not found in the input alphabet, or the third word is not a state
        if tmp[0] not in listStates or tmp[1] not in listSigma or tmp[2] not in listStates:    # the transition is not valid
            transFlag = False                                                                  # and we generate the error code 2
        listTransitionsEx.append(tmp)
    if transFlag == False:
        errorCode = 2

    return errorCode, listSigma, listStatesEx, listTransitionsEx

errorCode, listSigma, listStates, listTransitions = loadDfaFromFile(sys.argv[1])

if errorCode == 1:
    print(f"A section of the config file \"{sys.argv[1]}\" is missing!")
elif errorCode == 2:
    print(f"A transition of the config file \"{sys.argv[1]}\" is not valid!")
else:
    print(f"The config file \"{sys.argv[1]}\" is valid!")
