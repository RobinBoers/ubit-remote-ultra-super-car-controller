# Utility method to map the location of an integer in a
# range to its location in a different range
def mapNum(input, inMin, inMax, outMin, outMax):
    diffFromZero = 0 - inMin
    input += diffFromZero
    inMax += diffFromZero
    factor = input/inMax
    outRange = outMax-outMin
    diffFromZero = 0 - outMin
    output = outRange*factor
    output -= diffFromZero
    return output