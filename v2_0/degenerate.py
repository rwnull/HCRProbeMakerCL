from random import random
import sys

def choice(word):
    sys.tracebacklimit=0
    return str(word[int(random()*len(word))])

def iupacdgen2nt(base):
    sys.tracebacklimit=0
    base = str(base).upper() 
    if base == 'U':
        newbase = 'T'
    elif base == 'N':
        newbase = choice('ACGT')
    elif base == 'R':
        newbase = choice('AG')
    elif base == 'Y':
        newbase = choice('CT')
    elif base == 'S':
        newbase = choice('CG')
    elif base == 'W':
        newbase = choice('AT')
    elif base == 'I':
        newbase = choice('ATG')
    elif base == 'K':
        newbase = choice('GT')
    elif base == 'M':
        newbase = choice('AC')
    elif base == 'B':
        newbase = choice('CGT')
    elif base == 'D':
        newbase = choice('AGT')
    elif base == 'H':
        newbase = choice('ACT')
    elif base == 'V':
        newbase = choice('ACG')
    else:
        newbase = 'N'

    return str(newbase)

##'ABCDGHIKMNRSTUVWY'
##GPQLX

