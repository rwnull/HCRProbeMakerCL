## Commandline form of hcr probemaker
## Version2.0 2024June

#from dataclasses import is_dataclass
import sys
from vers import vers
from mainscript_core import cleanup
# importing hcr maker subscripts
from clscript import clb, action


sys.tracebacklimit=0

# call cl to assign variable values
'''hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,low = clb()
print("makeprobes,amplifier",amplifier)
# define a function that runs 

def hcr(hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,low):
    print("hcr")
    print(amplifier)
    sys.tracebacklimit=0
#    if batchfile == None:

# for a batch input check to see if there are multiple requested amplifiers
    ampli = list(amplifier)#str(amplifier))#.split(','))
    if len(list(amplifier)) == 1:
        print("len(list(amplifier)) == 1",list(str(amplifier)))
        #ampli = list(str(amplifier).split(','))
        action(hp,ampli,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,low)

    else:
        for xamp in amplifier:
            print("Xamp",xamp)
            action(hp,xamp,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,low)
    print(amplifier)
    print("endHCR")
 #   else:
  #      pass


#hcr(hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,low)
'''
