## Commandline form of hcr probemaker
## Version1.1 2022August

#from dataclasses import is_dataclass
import sys
from vers import vers
from mainscript_core import cleanup
# importing hcr maker subscripts
from clscript import cl, action
from CoD import creatorofdirs as cod

sys.tracebacklimit=0

hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,low = cl()

def hcr(hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,low):
    sys.tracebacklimit=0
    if batchfile == None:
        ampli = list(str(amplifier).split(','))
        if len(list(ampli)) == 1:
            ampli = list(str(amplifier).split(','))
            action(hp,ampli[0],name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,low)

        else:
            for xamp in amplifier:
                action(hp,xamp,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,low)

    else:
        pass


hcr(hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,low)

