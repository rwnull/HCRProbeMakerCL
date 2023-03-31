from operator import delitem
from Bio.Seq import Seq
from Bio.Blast.Applications import NcbiblastnCommandline as bn
import numpy as np
import pandas as pd
#import amp
from degenerate import iupacdgen2nt
from random import random
import io
from max33 import max33
from os import remove
import os, sys

sys.tracebacklimit=0



def variables(fullseq,amplifier,polyAT,polyCG,pause):
    sys.tracebacklimit=0
    ## derived variables from inputs
    fullseq = Seq(fullseq)
    fullseq = fullseq.reverse_complement()
    fullseq = ((fullseq).upper())
    cdna = len(fullseq)
    amplifier=((amplifier).upper())
    hpA = "A"*(int(polyAT)+1)
    hpT = "T"*(int(polyAT)+1)
    hpC = "C"*(int(polyCG)+1)
    hpG = "G"*(int(polyCG)+1)  
    position = cdna-pause
    start = np.arange(0,cdna-52,1)
    end = np.arange(52,cdna,1)
    table = np.vstack([start,end])
    new_var = (fullseq,cdna,amplifier,hpA,hpT,hpC,hpG,position,table)
    return (new_var)


def cleanup(fullseq):
    sys.tracebacklimit=0
    # this function takes in the user's sequence, and formats it
    #removing numbers, whitespace, and fasta symbol
    fullseq     = (fullseq).upper()
    spclchars	= "0123456789 >\t\r\n\v"
    for char in spclchars:
        fullseq	= fullseq.replace(char,"")

    # a loop that removes degenerate bases and converts uracil to thymine
    nt = 0
    fullseq2 = ['a']*len(fullseq)
    while nt < len(fullseq):
        if fullseq[nt]=='A' or fullseq[nt]=='C' or fullseq[nt]=='T' or fullseq[nt]=='G':
            fullseq2[nt] = str(fullseq[nt])
            nt+=1
        else:
            fullseq2[nt] = str(iupacdgen2nt(fullseq[nt]))
            nt+=1
    fullseq = ''.join(fullseq2)
    return fullseq



def cleanup2(name):
    sys.tracebacklimit=0
    specchar = "!"+"@"+"#"+"$"+"%"+"^"+"&"+"*"+":"+"("+")"+"+"+"\\"+"|"+"/"+"<"+">"+"~"+"`"+"'"+'"'+"?"+"="+"["+"]"+"{"+"}"+"-->"
    for value in specchar:
        name = name.replace(str(value),"_")
    if len(name) > 100:
        name=name[0:101]
    return(name)



def idpotentialprobes(position,fullseq,cdna,table,hpA,hpT,hpC,hpG,cgupper,cglower):
    sys.tracebacklimit=0
    seqs={}
    pos=[]    

    ## finding potential probe pairs that fit cg% and homopolymer limits
    a=0
    while a < (position-52):
        ppp = str(fullseq[table[0][a]:table[1][a]])
        b=0
        cg = 0
        
        while b < 52:
            char = str(ppp[b])
            if char=="C" or char=="G":
                cg+=1
                b+=1
            else:
                b+=1
        test1 = cg/52.0
        test2 = (str(fullseq[table[0][a]:table[1][a]])).find(hpA) + (str(fullseq[table[0][a]:table[1][a]])).find(hpT) + (str(fullseq[table[0][a]:table[1][a]])).find(hpC) + (str(fullseq[table[0][a]:table[1][a]])).find(hpG)
        
        if test1 > cgupper or  test1 < cglower or test2 > -4:
            a += 1
        else:
            pos.append([table[0][a],table[1][a]])
            a += 1

    ## Creating the first trace through the sequence looking for max number of probe sequences 
    if pos: 
        a = 0
        newlist = []
        newlista = []
        newlista2 = []
        strt=pos[0][0]
        stp=pos[0][1]
        newlista2.append([cdna-strt,cdna-stp])
        newlista.append([strt,stp])
        
        while a < len(pos):    
            if pos[a][0] > (stp + 2):
                strt = pos[a][0]
                stp  = pos[a][1]
                newlista2.append([cdna-strt,cdna-stp])
                newlista.append([strt,stp])
                a+=1
            else :
                a+=1
        lists = {}
        listz = {}
        listz[0] = newlista2
        lists[0] = newlista
        choice = "Default"
        newlist = np.array(lists[0])
        if newlist.size == 0:
            return[0,0]
        else:
            return [newlist,choice]
    else:
        return[0,0]

def noblast(newlist,fullseq,maxprobe,numbr,cdna):
    sys.tracebacklimit=0
    if len(newlist)>0:
        graphic = ['n']*cdna
        seqs = {}
        newlist = max33(maxprobe,newlist,numbr)
        count = str(len(newlist))
        a=0
        while a < len(newlist):
            seqs[a] = [newlist[a][0],str(fullseq[newlist[a][0]:(newlist[a][0]+25)]+"nn"+fullseq[(newlist[a][0]+27):newlist[a][1]]),newlist[a][1]]
            graphic[newlist[a][0]:newlist[a][1]] = str(fullseq[newlist[a][0]:(newlist[a][0]+25)]+"nn"+fullseq[(newlist[a][0]+27):newlist[a][1]])
            a+=1
        g = ''
        g = g.join(graphic)
        g = Seq(g)
        g = g.reverse_complement()
        return [count,seqs,g]

    else:
        pass



def blastnprobes(name,newlist,fullseq,db2,maxprobe,numbr,cdna,MEDIA_FASTA,BLAST_ROOT):
    sys.tracebacklimit=0
    if len(newlist) > 0:
        if db2 == None:
            graphic = ['n']*cdna
            seqs = {}
            newlist = max33(maxprobe,newlist,numbr)
            count = str(len(newlist))
            a=0
            while a < len(newlist):
                seqs[a] = [newlist[a][0],str(fullseq[newlist[a][0]:(newlist[a][0]+25)]+"nn"+fullseq[(newlist[a][0]+27):newlist[a][1]]),newlist[a][1]]
                graphic[newlist[a][0]:newlist[a][1]] = str(fullseq[newlist[a][0]:(newlist[a][0]+25)]+"nn"+fullseq[(newlist[a][0]+27):newlist[a][1]])
                a+=1
            g = ''
            g = g.join(graphic)
            g = Seq(g)
            g = g.reverse_complement()


            return [count,seqs,g]
        
        else:
            graphic = ['n']*cdna
            seqs={} 
            rmv = pd.DataFrame(columns = ["pos1","seq","pos2","fasta","num"])
            a=0
            b=1
            tmpFA = open(os.path.join(MEDIA_FASTA,(str(name)+"PrelimProbes.fa")), "w")

            while a < len(newlist):
                nm = '>'+str(b) 
                seqs[a] = [newlist[a][0],str(fullseq[newlist[a][0]:(newlist[a][0]+25)]+"nn"+fullseq[(newlist[a][0]+27):newlist[a][1]]),newlist[a][1],nm,a]
                rmv = rmv.append({'pos1' : newlist[a][0], 'seq' : str(fullseq[newlist[a][0]:(newlist[a][0]+25)]+"nn"+fullseq[(newlist[a][0]+27):newlist[a][1]]), 'pos2' : newlist[a][1], 'fasta':nm, 'num':a},  
                ignore_index = True) 
                tmpFA.write(nm)
                tmpFA.write('\n')
                tmpFA.write(seqs[a][1])
                tmpFA.write('\n')
                a+=1
                b+=1
            nm = '>'+name
            seqs[a] = str(fullseq)
            tmpFA.write(nm)
            tmpFA.write('\n')
            tmpFA.write(seqs[a])
            tmpFA.write('\n')
            tmpFA.close()




            ## Probe BLAST setup and execution from FASTA file prepared in previous step


            cline = bn(cmd="blastn", template_type = 'coding', template_length = 16, word_size = 11, query = os.path.join(MEDIA_FASTA,(str(name)+"PrelimProbes.fa")), subject = str(db2), dust='no', outfmt= '6 delim="\\t"  std qlen slen qseq sseq')
            stdout, stderr = cline() #cline() calls the string as a command and passes it to the command line, outputting the blast results to one variable and errors to the other
            dt = [(np.unicode_,100),(np.unicode_,100),(np.int32),(np.int32),(np.int32),(np.int32),(np.int32),(np.int32),(np.int32),(np.int32),(np.float32),(np.float32),(np.int32),(np.int32),(np.unicode_,10000),(np.unicode_,10000)]
            blastresult = (np.genfromtxt(io.StringIO(stdout),delimiter = '\t',dtype = dt))# "qseqid,sseqid,pident,length,mismatch,gapopen,qstart,qend,sstart,send,evalue,bitscore")




            ## This loop takes the data from the blast result and filters out probe pairs that do not meet criteria
                ## by setting a length match requirement this eliminates off-target pairs and half-pairs
                ## the e-value threshold ensures that the probe is a good match to the target

            i=0
            filterblast = []
            filterblastbad = []
            uniques = []
            uniquesbad = []
            while i < len(blastresult):

                if str(blastresult[i][0]) != name:
                    if (blastresult[i][11]>=85.0 and blastresult[i][3]>=50):  
                        filterblast.append(blastresult[i])
                        uniques.append((blastresult[i][0])) 

                        i+=1
                    elif (blastresult[i][11]>=60.0 and blastresult[i][11]<85.0 and blastresult[i][3]>=28):
                        for result in blastresult:
                            if blastresult[i][0] == result[0]:
                                result[0] = str(result[0])+'*'
                            else:
                                pass
                        z=0
                        while z < len(seqs):
                            #print(seqs[z][3],blastresult[i][0])
                            if str(seqs[z][3])+'*' == '>'+str(blastresult[i][0]):
                                seqs[z][3] = str(seqs[z][3])+'*'
                                z+=1
                            else:
                                z+=1
                                pass
                        filterblastbad.append(blastresult[i])
                        uniquesbad.append((blastresult[i][0])) #str
                        i+=1

                    else:
                        i+=1

                else:
                    i+=1

            fltrblastbad = 0
            fltrblastok = 0

            if len(filterblast) >= 0:
                filterblast = np.array(filterblast)
                uniques = np.unique((uniques))     ##
                count = str((len(uniques)))
                filterblastbad = np.array(filterblastbad)
                uniquesbad = np.unique((uniquesbad)) 
                if len(uniquesbad) > 0:
                    for bad in uniquesbad:
                        for good in uniques:
                            if good == bad:
                                good = str(good)+'*'
                                #this is a good place to have an optional dropout
                            else:
                                pass

                print()
                print()
                print("Probe pairs that had possible off-target matches to the provided database (lower e-value but with high site coverage). ")
                print("   Pairs ")
                print(uniquesbad)  
                print()
                print("Probe pairs that had good matches to the provided database were determined to be the following.")
                print("   Pairs ")
                print(uniques)
                print()
                print()

                if len(uniquesbad) > 0:
                    rmv = rmv.to_dict()
                    a=0
                    seqs={}
                    while a <len(rmv["pos1"]):
                        seqs[a] = (rmv["pos1"][a],rmv["seq"][a],rmv["pos2"][a],rmv["fasta"][a],rmv["num"][a])
                        a += 1
            else:
                pass


            seqs = max33(maxprobe,seqs,numbr)
            count = int(len(seqs))

            print()

            a=0
            b=0
            seqs1={}
            while a <= len(seqs)-1:
                tmp = (seqs[a])
                graphic[tmp[0]:tmp[2]] = str(tmp[1])
                seqs1[b]=tmp
                b+=1
                a+=1



            g = ''
            g = g.join(graphic) 
            g = Seq(g)
            g = g.reverse_complement()


            cols= ["QueryID","SubjectID","PercID","MatchLength","Mismatch","Gaps","Qstart","Qend","S_start","S_end","Evalue","bitscore","Q_length","S_length","Q_MatchSeq","S_MatchSeq"]
            
            blst = pd.DataFrame(blastresult)
            blst = blst.rename(columns={'f0':cols[0],'f1':cols[1],'f2':cols[2],'f3':cols[3],'f4':cols[4],'f5':cols[5],'f6':cols[6],'f7':cols[7],'f8':cols[8],'f9':cols[9],'f10':cols[10],'f11':cols[11],'f12':cols[12],'f13':cols[13],'f14':cols[14],'f15':cols[15]})
            blst = pd.DataFrame.to_dict(blst)
            return [uniquesbad,uniques,fltrblastbad,fltrblastok,str(count),seqs1,g,blst]
    else:
        pass