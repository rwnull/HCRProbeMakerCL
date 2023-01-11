from genericpath import isdir, isfile
from Bio import SeqIO as fa
import pandas as pd
import numpy as np
import os,sys
from mainscript_core import cleanup2
from clscript import clb, action

sys.tracebacklimit=0

def gnarly(hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,filename,i,low):
    sys.tracebacklimit=0
    protchar = "PQEFLX"
    pdf = pd.DataFrame(columns=["file","id","seq","amp","GC","gcr","atr","delay","blast","out","maxnum"])
            
    with open(os.path.join(batchfile, filename), 'r') as f:    
        print(filename.rpartition(".")[0])
        filename,ext = filename.rpartition(".")[0],filename.split(".")[-1]
        print(filename,ext)
        
        for entry in fa.parse(f,"fasta"):
            print(entry)
            count = 0
            
            for pc in protchar: ## A rough gate to block protein seqs from entering the algo
                count += str(entry.seq).count(pc)
            
            if count == 0:
                name = cleanup2(str(entry.id))

                amp = str(amplifier[i])
                filename2=str(filename+"_"+name)
                print()
                seq = str(entry.seq)
                gc = str(cglower)+"-"+str(cgupper)
                pdf=pdf.append({"file":filename2,"id":name,"seq":seq,"amp":amp,"GC":gc,"gcr":polyCG,"atr":polyAT,"delay":pause,"blast":txptome,"maxnum":maxprobes},ignore_index=True)
                action(hp,amp,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filename2,batchfile,dirslist,savevariable,args,low)

                if i < len(amplifier)-1:
                    i+=1
                else:
                    i=0
            
            else:
                pass


    
    f.close()
    return(hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,filename,i,pdf,low)

def fastbatch(): 
    sys.tracebacklimit=0
    hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,low = clb()
    

    i=0
    if isdir(batchfile):
        for filename in os.listdir(batchfile):
            hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,filename,i,pdf,low = gnarly(hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,filename,i,low)
            
    elif isfile(batchfile):
        
        batchfile,filename = os.path.split(batchfile)
        hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,filename,i,pdf,low = gnarly(hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,filename,i,low)
    else:   
        pass
    return(pdf)



pdf=fastbatch()



