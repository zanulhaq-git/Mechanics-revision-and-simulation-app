import math

def roundHalfUp(n, decimals):
    multiplier = 10**decimals # multiply up to allow the use of floor
    return math.floor(n * multiplier + 0.5) / multiplier # use floor to round, then divide back down

def roundReal(n, decimals):
    roundedAbs = roundHalfUp(abs(n), decimals) # rounds the magnitude of the number half up
    return math.copysign(roundedAbs, n) # takes the rounded number and copies the original sign back in

