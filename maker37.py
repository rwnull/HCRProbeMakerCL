## importing dependencies

import os,sys
from output import output
from datetime import date
from mainscript_core import variables,idpotentialprobes,noblast,blastnprobes


sys.tracebacklimit=0

def maker(name,fullseq,amplifier,pause,polyAT,polyCG,txptome,numbr,cgupper,cglower,MEDIA_ROOT,BLAST_ROOT,MEDIA_FASTA,MEDIA_OPOOL,MEDIA_OLIGO,MEDIA_TXT,maxprobes,low):     
    sys.tracebacklimit=0
    fullseq,cdna,amplifier,hpA,hpT,hpC,hpG,position,table = variables(fullseq,amplifier,polyAT,polyCG,pause)
    if low >= cdna:
        return(None,None)
    else:
        pot = idpotentialprobes(position,fullseq,cdna,table,hpA,hpT,hpC,hpG,cgupper,cglower)  
        
        if pot[-1] == "Default":
            newlist,choice = pot[0],pot[1]
            if txptome == None:
                count,seqs,g = noblast(newlist,fullseq,maxprobes,numbr,cdna)
                today = str(date.today())

                return(output(cdna,g,fullseq,count,amplifier,name,pause,seqs,today,polyAT,polyCG,cgupper,cglower,MEDIA_ROOT,BLAST_ROOT,MEDIA_FASTA,MEDIA_OPOOL,MEDIA_OLIGO,MEDIA_TXT,maxprobes,None),count)
            else:
                probs = blastnprobes(name,newlist,fullseq,txptome,maxprobes,numbr,cdna,MEDIA_FASTA,BLAST_ROOT)
                if probs == None:
                    return(None,None)
                else:
                    uniquesbad,uniques,fltrblastbad,fltrblastok,count,seqs,g,blst = probs[0],probs[1],probs[2],probs[3],probs[4],probs[5],probs[6],probs[7]

                today = str(date.today())

                ## creating output data from culled seqs  
                return(output(cdna,g,fullseq,count,amplifier,name,pause,seqs,today,polyAT,polyCG,cgupper,cglower,MEDIA_ROOT,BLAST_ROOT,MEDIA_FASTA,MEDIA_OPOOL,MEDIA_OLIGO,MEDIA_TXT,maxprobes,blst),count)
        else:
            print("maker:idpotprobes")
            return(None,None)
