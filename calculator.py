import math

#from interpret import condense, extend

exportString = ""

timesI = 50

#firstInf = "(1)"
#firstRelativeRep = [0]
#firstMaxRR = max(firstRelativeRep)
#firstArrayRR = []

operation = "*"

#secondInf = "(1)"
#secondRelativeRep = [0]
#secondMaxRR = max(secondRelativeRep)
#secondArrayRR = []

operationalLCM = 0

testAna = []
global numOfZero

def stringToArray(stri):
    nowArray = []
    inArray = False
    tempS = ""
    tempN = 0

    for char in stri:
        #print(tempS)
        if char == "," or char == "]":
            nowArray.append(int(tempS))
            tempS = ""
        elif (char == "0" or char == "1" or char == "2" or char == "3"
              or char == "4" or char == "5" or char == "6" or char == "7" or char == "8" or char == "9"):
            tempS += char
        else:
            continue

    print(nowArray)
    return nowArray


def lcm(x, y):

    counter = 0
    lcm = y
    if x == 0:
        return y
    if y == 0:
        return x
    while lcm % x != 0:
        lcm += y

    return lcm


# interpreting infinite number notation to create a number used for calculations
# now taking in both numbers at the same time, for LCM(lcm) calculations
def infTextToInt2(s, T, s2, T2, rrAdder):
    output = 0
    base = ""
    rDigit = ""
    rSets = []
    cSets = []
    allSets = []
    post = ""
    global numOfZero, operationalLCM
    numOfZeroL = 0
    time = T.copy()
    time2 = T2.copy()

    # now we need to add rrAdder to each RR in both arrays since it is no longer automatic
    counter = 0
    for R in time:
        time[counter] += rrAdder
        counter += 1

    counter = 0
    for R in time2:
        time2[counter] += rrAdder
        counter += 1

    # for now, use this to determine if the inf number is basic or not.
    isBasic = False

    # first, lets find the base before the end of repeating digits
    for digit in s:
        if digit != '(' and digit != ')':
            base += digit
        if digit == "(":
            break
    if base == "":
        base = "0"

    # find the repeating digit set
    insideP = False
    isBase = True
    for digit in s:
        if digit == "(":
            insideP = True
            isBase = False
            # if there are any numbers we assumed to be Post,
            # those should be in a middle set since we found another parenthesis
            if post != "":
                allSets.append(post)
            post = ""
            continue
        if insideP and digit != ")":
            rDigit += digit
            if digit == "0" and rDigit.endswith("0") and base == "0":
                numOfZeroL += 0#1
            continue

        # since we found the end of a set, add the current set to rSets and start over
        if digit == ")":
            insideP = False
            rDigit = "r" + rDigit
            rSets.append(rDigit)
            allSets.append(rDigit)
            rDigit = ""

            continue
        if not insideP and not isBase and digit != ")":
            post += digit
            continue


    #-------------------------

    output2 = 0
    base2 = ""
    rDigit2 = ""
    rSets2 = []
    allSets2 = []
    post2 = ""
    global numOfZero
    numOfZeroL = 0
    # for now, use this to determine if the inf number is basic or not.
    isBasic = False
    # first, lets find the base before the end of repeating digits
    for digit in s2:
        if digit != '(' and digit != ')':
            base2 += digit
        if digit == "(":
            break
    if base2 == "":
        base2 = "0"

    # find the repeating digit set
    insideP = False
    isBase = True
    for digit in s2:
        if digit == "(":
            insideP = True
            isBase = False
            # if there are any numbers we assumed to be Post,
            # those should be in a middle set since we found another parenthesis
            if post2 != "":
                allSets2.append(post2)
            post2 = ""
            continue
        if insideP and digit != ")":
            rDigit2 += digit
            if digit == "0" and rDigit2.endswith("0") and base2 == "0":
                numOfZeroL += 0  # 1
            continue

        # since we found the end of a set, add the current set to rSets and start over
        if digit == ")":
            insideP = False
            rDigit2 = "r" + rDigit2
            rSets2.append(rDigit2)
            allSets2.append(rDigit2)
            rDigit2 = ""

            continue
        if not insideP and not isBase and digit != ")":
            post2 += digit
            continue

    # -------------------------

    setTemp = ""
    setTemp2 = ""
    if len(allSets) > 0:
        setTemp = allSets[0].split("r", 1)[1]
        lenSet1 = len(setTemp)

    else:
        lenSet1 = 0

    if len(allSets2) > 0:
        setTemp2 = allSets2[0].split("r", 1)[1]
        lenSet2 = len(setTemp2)

    else:
        lenSet2 = 0

    lcmNum = lcm(lenSet1, lenSet2)
    if operation == "=":
        lcmNum = 1
    operationalLCM = lcmNum

    if len(allSets) != 0:
        setCounter = 0
        for sett in allSets:
            setTemp = sett
            # if we are looking at a repeating digit set, remove the R and repeat the values based on LCM
            if sett.find("r") > -1:
                removeR = allSets[setCounter].split("r", 1)[1]
                allSets[setCounter] = removeR

                while len(allSets[setCounter]) % lcmNum != 0:
                    allSets[setCounter] += removeR
                # now put r back in so we can see which need to be repeated based on RR
                allSets[setCounter] += "r"

            setCounter += 1


    if len(allSets2) != 0:
        setCounter = 0
        for sett in allSets2:
            setTemp = sett
            # if we are looking at a repeating digit set, remove the R and repeat the values based on LCM
            if sett.find("r") > -1:
                removeR = allSets2[setCounter].split("r", 1)[1]
                allSets2[setCounter] = removeR

                while len(allSets2[setCounter]) % lcmNum != 0:
                    allSets2[setCounter] += removeR
                # now put r back in so we can see which need to be repeated based on RR
                allSets2[setCounter] += "r"

            setCounter += 1

    # -------------------------

    # test adding on only the rDigit set
    output = base
    counterRR = 0
    for rset in allSets:
        counter = 0
        temp = ""
        if rset.find("r") != -1:
            rset = rset.split("r", -1)[0]
            # use the index of the number of RDS to get the correct RR
            while counter < time[counterRR]:
                temp += rset
                counter += 1
            counterRR += 1
        if temp == "":
            temp = rset
        output += temp
    output += post


    # -------------------------

    # test adding on only the rDigit set
    output2 = base2
    counterRR2 = 0
    for rset in allSets2:
        counter = 0
        temp = ""
        if rset.find("r") != -1:
            rset = rset.split("r", 1)[0]
            while counter < time2[counterRR2]:
                temp += rset
                counter += 1
            counterRR2 += 1
        if temp == "":
            temp = rset
        output2 += temp
    output2 += post2

    numOfZero = numOfZeroL

    finalOut1 = -1
    finalOut2 = -1

    if output.find(".") == -1:
        finalOut1 = int(output)
    else:
        finalOut1 = float(output)

    if output2.find(".") == -1:
        finalOut2 = int(output2)
    else:
        finalOut2 = float(output2)

    return [finalOut1, finalOut2]



def infiniteXinfinite(s, s2, fRR, sRR, oper):

    x = -1
    counter = 1
    ss = s
    ss2 = s2
    output = ""
    isEstimated = False
    operation = oper
    global exportString
    iterationsToShow = 50 - min(0, 1 * min(min(fRR), min(sRR)))
    timesI = iterationsToShow

    while counter <= timesI:

        # removed "counter + " from RRs
        holder = infTextToInt2(s, fRR, s2, sRR, counter)
        infNum = holder[0]
        infNum2 = holder[1]
        comp = " is equal to "
        # determine the operation to be done
        if operation == "*" or operation == "\*":
            operation = "*"
            x = infNum * infNum2
        elif operation == "+" or operation == "\+":
            operation = "+"
            x = infNum + infNum2
        elif operation == "-" or operation == "\-":
            operation = "-"
            x = infNum - infNum2
        elif operation == "/":
            if infNum2 != 0:
                x = infNum / infNum2
                if int(x) == x and "e" in str(x):
                    isEstimated = True
                    print("[Estimated value due to float decimal conversion]")
                    x = int(x)

            else:
                x = "cannot divide by 0 (yet)"
        elif operation == "//":
            if infNum2 != 0:
                x = infNum // infNum2
            else:
                x = "cannot divide by 0 (yet)"
        elif operation == "%":
            x = infNum % infNum2
        elif operation == "^":
            x = infNum ** infNum2
        elif operation == "=":

            if infNum > infNum2:
                comp = " is greater than "
            if infNum < infNum2:
                comp = " is less than "

        elif operation == "cos":
            x = math.cos(infNum)

        if counter <= timesI and timesI - counter <= iterationsToShow:
            if "e" in str(x):
                xs = extend(x)
                isEstimated = True
            else:
                xs = str(x)

            if operation != "=":
                if "e" in str(infNum):
                    infNum = extend(infNum)
                    isEstimated = True
                print(str(counter) + ") " + str(infNum) + operation + str(infNum2) + " = " + xs)
                exportString += (str(counter) + ") " + str(infNum) + operation + str(infNum2) + " = " + xs) + "\n\n"


            az = 0
            isNeg = xs.startswith("-")
            if isNeg:
                if xs.find(".") == -1:
                    xb = int(xs) * -1
                else:
                    xb = float(xs) * -1
                xs = str(xb)

            while az < numOfZero:
                temp = xs
                xs = "0" + temp
                az += 1
            if isNeg:
                xs = "-" + xs

            if operation != "=":
                print(condense(xs, numOfZero+1, counter, operationalLCM))
                exportString += condense(xs, numOfZero+1, counter, operationalLCM)
                if isEstimated:
                    print("[Estimated value due to float decimal conversion]")
                    exportString += "[Estimated value due to float decimal conversion]"
            else:
                print(str(infNum) + " " + comp + " " + str(infNum2))
                exportString += str(infNum) + " " + comp + " " + str(infNum2)
            exportString += "\n----------------------------------------------------\n"

        counter += 1
    return exportString


mainString = ""
#timesI = 25
repetitionAr = []


# condensing infinite numbers to string notation
def condense(nu, checkOverride, currentCounter, lcm):

    output = ""
    num = nu
    length = len(num)
    counter = checkOverride  # 1
    checkMaker = 1
    nested = False
    endofnum = False
    endnum = ""
    testAna = []
    tempOut = ""
    tempCount = 0
    finalRRoutput = ""
    global exportString

    while counter <= length/2 and output == "":

        # build the ranges that we need to analyze
        checks = []
        checkMaker = 1
        while checkMaker * counter - 1 < length:

            checks.append([counter * (checkMaker - 1), counter * checkMaker - 1])
            # if odd, add 1 more char on the end
            if not length % checkMaker == 0 and (checkMaker + 1) * counter - 1 >= length:
                apnum = counter * checkMaker
                checks.append([apnum, apnum])
            checkMaker += 1

        # using the positions listed in checks, compare the range within the string

        range1ex = ""
        r1c = 0
        while r1c <= checks[0][1]:
            range1ex += num[r1c]
            r1c += 1

        range2ex = ""
        r2c = counter
        while r2c <= checks[1][1]:
            range2ex += num[r2c]
            r2c += 1

        counter += 1

        # found a match, check for others
        if range1ex == range2ex:
            #add numbers for analysis
            testAna.append([range1ex, 2])

            # add what we found to temp output
            tempOut += range1ex + range2ex
            tempCount = 2

            # remove first two ranges. this range ends at checks[1][1]
            newnum = ""
            cutCount = 0
            for n in num:
                if cutCount > checks[1][1]:
                    newnum += n
                cutCount += 1
            num = newnum
            length = len(num)

            # check for more matches to remove, if we are not at the end of the string/current range bigger than next
            while not length == 0 and not checks[0][1] > length - 1:
                # build a new string to check for matches
                range3ex = ""
                r3c = 0
                while r3c <= checks[0][1]:
                    range3ex += num[r3c]
                    r3c += 1

                # now check if the range in the cut string matches
                if range3ex == range1ex:
                    #add to temp
                    tempOut += range3ex
                    tempCount += 1
                    # if so, trim the match
                    newnum = ""
                    cutCount = 0
                    for n in num:
                        if cutCount > checks[0][1]:
                            newnum += n
                        cutCount += 1
                    num = newnum
                    length = len(num)

                    # add to the analyze counter
                    testAna[len(testAna) - 1][1] += 1

                else:
                    break

            #if there are (timesI/2)+ matches, add to output as condensed
            if tempCount*len(range1ex) >= timesI/2:
                output += "(" + range1ex + ")"
                print(f"repetitions for {range1ex} = {tempCount}, "
                      f"for {(tempCount*len(range1ex)  - currentCounter*lcm)} Relative Repetitions")
                exportString += (f"repetitions for {range1ex} = {tempCount}, "
                      f"for {(tempCount*len(range1ex)  - currentCounter*lcm)} Relative Repetitions") + "\n"
                finalRRoutput += " " + f"{(tempCount*len(range1ex)  - currentCounter*lcm)}" + ","

            #add to the repetition array
            else:
                output += tempOut

            tempCount = 0
            tempOut = ""

            # now put the rest back into the function to start over, and add the result to output
            if not num == "":
                nested = True

                output += condense(num, checkOverride, currentCounter, lcm)

    # only if our current range is bigger than the len of num, add the rest of the number to the end of output
    if counter * checkMaker - 1 >= length - 1 and not nested and not num == "":
        output += num[0]
        #trim the first number off of num, then nest
        newnum = ""
        cutCount = 0
        for n in num:
            if cutCount > 0:
                newnum += n
            cutCount += 1
        num = newnum
        length = len(num)
        if not num == "":
            output += condense(num, checkOverride, currentCounter, lcm)


    highLevel = 0

    if len(repetitionAr) == 0:
        highLevel = len(nu)/timesI

    nested = False
    if finalRRoutput == " ":
        finalRRoutput = ""
    return output + finalRRoutput


# turning a number in scientific notation into an estimated extended string
def extend(scienceNum):
    splitter = str(scienceNum)
    numToMultiply = ""
    sign = "+"
    decimalDigitCount = 0
    degreeOf10 = 0
    tempHold = ""
    postE = False
    postPer = False
    output = ""
    isNeg = False

    # split the incoming scientific number into different parts
    for char in splitter:
        if char == "e":
            postE = True
            postPer = False
            numToMultiply = tempHold
            tempHold = ""
            continue
        if postE and (char == "+" or char == "-"):
            sign = char
            continue
        if char == "-" and not postE:
            isNeg = True
            continue
        if char == ".":
            postPer = True
            continue
        if postPer:
            decimalDigitCount += 1
        tempHold += char
    degreeOf10 = tempHold
    print(degreeOf10)
    degreeOf10 = int(degreeOf10)
    tempHold = ""

    # subtract the num of digits behind the decimal from the degree of 10
    degreeOf10 -= decimalDigitCount

    #add zeros in the proper side of num (based on sign) equal to degree of 10
    counter = 0
    stringOfZeros = ""
    while counter < degreeOf10:
        counter += 1
        stringOfZeros += "0"

    # if sign is positive, add zeroes to front, else add to back
    if sign == "+":
        output = numToMultiply + stringOfZeros
    else:
        output = "0." + stringOfZeros + numToMultiply

    # apply negative
    if isNeg:
        output = "-" + output

    return output