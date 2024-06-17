from genericpath import isdir, isfile
from Bio import SeqIO as fa
import pandas as pd
from isfasta import is_fasta
import os
from mainscript_core import cleanup2
from clscript import clb, action
from CoD import creatorofdirs


# if an output folder doesn't exist, this will make it
creatorofdirs()



def gnarly(hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,filename,i,low):
    #print()
    #print("gnarly")
    filename = batchfile
    protchar = "PQEFLX"
      
    with open(os.path.join("./",filename), 'r') as f: 
        filename,ext = filename.rpartition(".")[0],filename.split(".")[-1]

        for entry in fa.parse(f,"fasta"):
            pdf = pd.DataFrame(columns=["file","id","seq","amp","GC","gcr","atr","delay","blast","out","maxnum"])
        # A rough gate to block protein seqs from entering the algo // 
        ## every protein-related character increases entrycount from 0, 
        ## if entrycount > 0, the remaining steps are skipped
            entrycount = 0
            for pc in protchar:
                entrycount += str(entry.seq).count(pc)

            if entrycount == 0:
                name = cleanup2(str(entry.id))
                if amplifier[i] == 'B' or amplifier[i] == 'S' or len(amplifier[i])==1:
                    amp = amplifier
                else:
                    amp = str(amplifier[i])
                filename2=str(filename+"_"+name)
                seq = str(entry.seq)
                gc = str(cglower)+"-"+str(cgupper)
                
                pdf.loc[len(pdf.index)] = {"file":filename2,"id":name,"seq":seq,"amp":amp,"GC":gc,"gcr":polyCG,"atr":polyAT,"delay":pause,"blast":txptome,"maxnum":maxprobes}
                
                action(hp,amp,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filename2,batchfile,dirslist,savevariable,args,low)
                
                if i < len(amplifier)-1:
                    i+=1
                else:
                    i=0
            
            else:
                pass
    
    f.close()
    #print("endGnarly")
    return(hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,filename,i,pdf,low)

    
def fastbatch():
    #print()
    #print("fastbatch")
    
    hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,low = clb()
    #print(amplifier) 
    filename = ""
    i=0
    if isfile(batchfile):
        path2,batchfile2 = (os.path.split(batchfile))
        #print("is_fasta(batchfile)",is_fasta(batchfile))
        if is_fasta(batchfile):#path2,batchfile2):
            hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,filename,i,pdf,low = gnarly(hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,filename,i,low)
            #print("endFastBatch-IsFasta")
            return(pdf)
                
        else:
            print("The file provided is not recognized as a '.fasta' formatted file.")
            #raise(Exception.with_traceback)
            
    elif isdir(batchfile):
        for path,di,fl in os.walk(batchfile):
            for subf in fl:
            #path is the path, fl is a list of files within path, subf is one of the files in fl
                if isfile(os.path.join(path,subf)):
                    if is_fasta(os.path.join(path,subf)) and 1 > gnarly(hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,os.path.join(path,subf),dirslist,savevariable,args,filename,i,low):
                        hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,filename,i,pdf,low = gnarly(hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,os.path.join(path,subf),i,low)
                        #print("BatchFile isdir; endFastBatch")
                        return(pdf)
                    else:
                        print(str(subf)," is not in fasta format or is not a fasta file.")
                else:
                    pass
    else:
        pass       




pdf=fastbatch() 
