## base price of IDT oligoPool as of August 2022 === $99 for up to 3300 bp total across all oligos 
## at 90bp of oligo per HCR-3.0-style probe pair (20bp per 1/2 initiator and spacer plus 25bp per 1/2 annealing site == 45bp per 1/2pair)

## 36 probe pairs of std Choi et al lengths
## @ 66bp/Tsuneoka style probe pair 3300bp == 50 pp

import numpy as np
import sys

def max33(maxprobe,seqs,numbr):
    
    #print("max33")
    sys.tracebacklimit=0
    if maxprobe == 'n':
        if int(numbr) < int(len(seqs)):
            reduced = []
            entry = np.zeros(len(seqs))
            if numbr == 0:
                keep = int(len(seqs))#33
            else:
                keep = numbr             # this is the max number of probe pairs that ensures the cheapest opool at 50pmol
            skip = (len(seqs))-keep
            zeroesperones = int(skip/keep)
            addtnl0s = skip-(keep*zeroesperones)
            a = 0
            c = 0
            pos = 0
            while a < keep:
                entry[pos] += 1
                a += 1
                pos += 1
                if c < addtnl0s:
                    entry[pos] += 0
                    c += 1
                    pos += 1
                b = 0
                while b < zeroesperones:
                    entry[pos] += 0
                    pos += 1
                    b += 1
            a=0
            while a < addtnl0s-c:
                entry[pos] += 0
                pos += 1
                a+=1            
            a = 0
            while a < len(seqs):
                if entry[a] == 1:
                    reduced.append(seqs[a])
                    a+=1
                else:
                    a+=1
                    pass    
            print("The number of probe pairs has been limited by the user.")
            #print("reduced = ",reduced)
            #print("endMax33")
            return(reduced)
        elif  int(numbr) >=  int(len(seqs)):
            print("There were fewer than "+str(numbr)+" pairs, no action to limit the number of probe pairs was taken.")
            #print("endMax33")
            return(seqs)
    else:
        #print("endMax33")
        return(seqs)