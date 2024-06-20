from Bio.Seq import Seq
import subprocess as sp
import numpy as np
import pandas as pd
#import amp
from degenerate import iupacdgen2nt
import io
from max33 import max33

import os, sys

sys.tracebacklimit=0



def variables(fullseq,amplifier,polyAT,polyCG,pause):
    #print("variables")
    #print(amplifier)
    sys.tracebacklimit=0
    ## derived variables from inputs
    fullseq = Seq(fullseq)
    fullseq = fullseq.reverse_complement()
    fullseq = ((fullseq).upper())
    cdna = len(fullseq)
    print("length of input sequence is ",cdna)
    amplifier=(str(amplifier).upper())
    #print(amplifier)
    hpA = "A"*(int(polyAT)+1)
    hpT = "T"*(int(polyAT)+1)
    hpC = "C"*(int(polyCG)+1)
    hpG = "G"*(int(polyCG)+1)  
    position = cdna-pause
    start = np.arange(0,cdna-52,1)
    end = np.arange(52,cdna,1)
    table = np.vstack([start,end])
    new_var = (fullseq,cdna,amplifier,hpA,hpT,hpC,hpG,position,table)
    #print("endVariables")
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
    #print("idPotProbes")
    seqs={}
    pos=[]    
    specchar = "!"+"@"+"#"+"$"+"%"+"^"+"&"+"*"+":"+"("+")"+"+"+"\\"+"|"+"/"+"<"+">"+"~"+"`"+"'"+'"'+"?"+"="+"["+"]"+"{"+"}"+"-->"
    spclchars	= "PQLX0123456789 ->\t\r\n\v"
    ## finding potential probe pairs that fit cg% and homopolymer limits
    a=0
    while a < (position-52):
        ppp = str(fullseq[table[0][a]:table[1][a]])
        b=0
        cg = 0
        
        while b < 52:
            char = str(ppp[b])
            if char in specchar or char in spclchars:
                #print(char)
                b = 52
                #print("b= ",b)
                cg = 1000.0
                #print("cg = ",cg)
                test1 = 1000.0
                #print("test1=",test1)
                test2 = 1000.0
                #print("test2 = ",test2)
            elif char=="C" or char=="G":
                cg+=1
                b+=1
            else:
                b+=1
        test1 = cg/52.0
        test2 = (str(fullseq[table[0][a]:table[1][a]])).find(hpA) + (str(fullseq[table[0][a]:table[1][a]])).find(hpT) + (str(fullseq[table[0][a]:table[1][a]])).find(hpC) + (str(fullseq[table[0][a]:table[1][a]])).find(hpG)
        #print("test1 = ",test1)
        #print("test2 = ",test2)

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
        #print("pos = ",pos)
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
        #print("lists = ",lists)
        #print("listz = ", listz)
        newlist = np.array(lists[0])
        #print("newlist = ",newlist)
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
        #print("newlist = ",newlist)
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
        #print("Passing on this sequence.")
        return [0,[None],None]



def blastnprobes(name,newlist,fullseq,db2,maxprobe,numbr,cdna,MEDIA_FASTA,BLAST_ROOT):
    #print()
    #print("blastnprobes")
    sys.tracebacklimit=0
    #print("name = ",name)
    newlist1,fullseq1,maxprobe1,numbr1,cdna1 = newlist,fullseq,maxprobe,numbr,cdna
    
    if len(newlist) > 0:
        if db2 == None:
            graphic = ['n']*cdna
            seqs = {}
            newlist = max33(maxprobe,newlist,numbr)
            #print("newlistA = ",newlist)
            count = str(len(newlist))
            #print("count= ",count)
            a=0
            while a < len(newlist):
                seqs[a] = [newlist[a][0],str(fullseq[newlist[a][0]:(newlist[a][0]+25)]+"nn"+fullseq[(newlist[a][0]+27):newlist[a][1]]),newlist[a][1]]
                graphic[newlist[a][0]:newlist[a][1]] = str(fullseq[newlist[a][0]:(newlist[a][0]+25)]+"nn"+fullseq[(newlist[a][0]+27):newlist[a][1]])
                a+=1
            g = ''
            g = g.join(graphic)
            g = Seq(g)
            g = g.reverse_complement()
            #print("end_blastnprobes")
            return [count,seqs,g]
        
        else:
            graphic = ['n']*cdna
            seqs={} 
            rmv = pd.DataFrame(columns = ["pos1","seq","pos2","fasta","num"])
            a=0
            b=1
            tmpFA = open(os.path.join(MEDIA_FASTA,(str(name)+"PrelimProbes.fa")), "w")
            #print("newlist = ",newlist)
            #print("len newlist = ",len(newlist))
            #print("Now working on "+str(name))
            #print("seqs= ",seqs)
            while a < len(newlist):
                nm = '>'+str(b) 
                seqs[a] = [newlist[a][0],str(fullseq[newlist[a][0]:(newlist[a][0]+25)]+"nn"+fullseq[(newlist[a][0]+27):newlist[a][1]]),newlist[a][1],nm,a]
                #print('seqs['+str(a)+'] = ',seqs[a])
                rmv.loc[len(rmv.index)]=[newlist[a][0],str(fullseq[newlist[a][0]:(newlist[a][0]+25)]+"nn"+fullseq[(newlist[a][0]+27):newlist[a][1]]),newlist[a][1],nm,a]
                #rmvnewline = pd.DataFrame([newlist[a][0],str(fullseq[newlist[a][0]:(newlist[a][0]+25)]+"nn"+fullseq[(newlist[a][0]+27):newlist[a][1]]),newlist[a][1],nm,a])
                #print("rmvnewline = ",rmvnewline)
                #rmv = pd.concat([rmv,rmvnewline], ignore_index = True) 
                tmpFA.write(nm)
                tmpFA.write('\n')
                tmpFA.write(seqs[a][1])
                tmpFA.write('\n')
                #print("a = ",a)
                a+=1
                b+=1
            nm = '>'+name
            seqs[a] = str(fullseq)
            #print('seqs['+str(a)+'] = ',seqs[a])
            tmpFA.write(nm)
            tmpFA.write('\n')
            tmpFA.write(seqs[a])
            tmpFA.write('\n')
            tmpFA.close()



            
            ## Probe BLAST setup and execution from FASTA file prepared in previous step

            ouf = '"6 delim=& std qlen slen qseq sseq"' #delim=\t 
            cmd = 'blastn -query '+os.path.join(MEDIA_FASTA,(str(name)+'PrelimProbes.fa'))+' -subject '+db2+' -template_type coding -template_length 16 -word_size 11 -dust no -evalue 1e-10 -outfmt '+str(ouf)
            #print("cmd = "+cmd)
            #cline = bn(cmd="blastn", template_type = 'coding', template_length = 16, word_size = 11, query = os.path.join(MEDIA_FASTA,(str(name)+"PrelimProbes.fa")), subject = str(db2), dust='no', outfmt=ouf)
            #print("cline")
            fail = True
            try:
                #print("stout=sp.run")    
                stout=sp.run(cmd, shell=True, capture_output=True,check=True)
                #print(stout)
                if stout:
                    #print("stout == True")
                    fail = False
                    #print("Fail = ",fail)
                #print(str(stout.stdout.splitlines(keepends=True)).split("b'"))#"blastn","-query "+os.path.join(MEDIA_FASTA,(str(name)+"PrelimProbes.fa"),"-subject "+db2))#cmd])##, stderr = cline() #cline() calls the string as a command and passes it to the command line, outputting the blast results to one variable and errors to the other
                dt = [(np.unicode_,100),(np.unicode_,100),(np.int32),(np.int32),(np.int32),(np.int32),(np.int32),(np.int32),(np.int32),(np.int32),(np.float32),(np.float32),(np.int32),(np.int32),(np.unicode_,10000),(np.unicode_,10000)]
                #print(stout)
                blastresult = np.genfromtxt(io.StringIO(stout.stdout.decode(encoding="utf-8")),dtype = dt,delimiter = '&')
                #print("blastresult=",blastresult)
                
            except:
                #print("There is something wrong with the formatting of the fasta file.")
                pass
            else:
                ## This loop takes the data from the blast result and filters out probe pairs that do not meet criteria
                    ## by setting a length match requirement this eliminates off-target pairs and half-pairs
                    ## the e-value threshold ensures that the probe is a good match to the target
                if len(blastresult) > 0:              
                    i=0
                    filterblast = []
                    filterblastbad = []
                    uniques = []
                    uniquesbad = []
                    while i < len(blastresult):
                        # Parsing of blast results to identify potential off target effects begins here.
                        # The final searched element is the full length input sequence, if the blast query is a probe pair it will not be named as the full length query
                            # this first filter separates full length from potential probe pair searches
                        if str(blastresult[i][0]) != name:
                            #print("i,blastresult[i][0],name ",i,blastresult[i][0],name) ##################################################

                            # next filter sets an arbitrary threshold with a raw score > 85 and a matchlength of > 50 
                                # and with a subject name equal to the full length sequence name, ie a good hit
                            if (blastresult[i][11]>=85.0 and blastresult[i][3]>=50 and blastresult[i][1]==name):  
                                filterblast.append(blastresult[i])
                                uniques.append((blastresult[i][0])) 
                                i+=1

                            # this filter maintains the arbitrary "good" threshold above but if the subject name 
                                # isn't the same as the input sequence it will be marked as a potential off-target sequence
                                ### CAVEAT: if the input FASTA and Reference Txptome use different seqIDs all sequences will be marked as potentially off target
                            elif (blastresult[i][11]>=85.0 and blastresult[i][3]>=50 and blastresult[i][1]!=name):
                                for result in blastresult:
                                    #print("OFFTarget: blastresult rawscore, matchlen",blastresult[i][11],blastresult[i][3])
                                    if blastresult[i][0] == result[0]:
                                        result[0] = '--> '+str(result[0])
                                    else:
                                        pass

                                z=0
                                while z < len(seqs):
                                    if '--> '+str(seqs[z][3]) == '>'+str(blastresult[i][0]):
                                        seqs[z][3] = "--> "+str(seqs[z][3])
                                        z+=1
                                    else:
                                        z+=1
                                        pass

                                filterblastbad.append(blastresult[i])
                                uniquesbad.append((blastresult[i][0])) #str
                                i+=1

                            # the following filter marks blast hits that are less perfect but still decent as potential off target hits
                            elif (blastresult[i][11]>=60.0 and blastresult[i][11]<85.0 and blastresult[i][3]>=28):
                                for result in blastresult:
                                    #print("OFFTarget: blastresult rawscore, matchlen",blastresult[i][11],blastresult[i][3])
                                    if blastresult[i][0] == result[0]:
                                        result[0] = str(result[0])+'*'
                                    else:
                                        pass

                                z=0
                                while z < len(seqs):
                                    if str(seqs[z][3])+'*' == '>'+str(blastresult[i][0]):
                                        seqs[z][3] = str(seqs[z][3])+'*'
                                        z+=1
                                    else:
                                        z+=1
                                        pass

                                filterblastbad.append(blastresult[i])
                                uniquesbad.append((blastresult[i][0])) #str
                                i+=1

                            # last if the hit doesn't match any of the above filters it is ignored
                            else:
                                i+=1

                        else:
                            #print(i,blastresult[i][0],name)
                            i+=1

                    fltrblastbad = 0
                    fltrblastok = 0
                    
                    #print(filterblast)
                    
                    
                    if len(filterblast) > 0: #>= 0
                        #print("len(filterblast) > 0")
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
                        print("Probe pairs that had good matches to the provided database were determined to be the following.")
                        print("   Pairs ")
                        print(uniques)
                        print()
                        print()
                        print("Probe pairs that had possible off-target matches to the provided database (lower e-value but with high site coverage). ")
                        print("Pairs marked with '-->' are perfect matches with differing FASTA id from the query FASTA id.")
                        print("Pairs marked with '*' are less perfect matches; at least 28nt match length and between 60 and 85 rawscore.")
                        print("   Pairs ")
                        print(uniquesbad)  
                        print()
                        print()

                        
                        if len(uniquesbad) > 0:
                            #print("len(uniquesbad) > 0")
                            rmv = rmv.to_dict()
                            #print("rmvasDict")
                            a=0
                            seqs={}
                            #print("rmv= ",rmv)
                            #print("len(rmv['pos1'])",len(rmv["pos1"]))
                            while a <len(rmv["pos1"]):
                                seqs[a] = (rmv["pos1"][a],rmv["seq"][a],rmv["pos2"][a],rmv["fasta"][a],rmv["num"][a])
                                a += 1
                                #print(a)
                        #print("seqs= ",seqs)
                        #print("numbr= ",numbr)
                        #print("maxprobes= ",maxprobe)
                        seqs = max33(maxprobe,seqs,numbr)
                        #print("max33,seqs",seqs)
                        #print("count")
                        
                        count = len(list(seqs))
                        
                        
                        #print("count",count)
                        #print(seqs)
                        #print("seqs1")
                        a=0
                        b=0
                        seqs1={}
                        #print(len(seqs))
                        while a < int(count)-1:#while a <= len(seqs)-1:
                            #print("seqs1,a = ",a)
                            tmp = (seqs[a])
                            graphic[tmp[0]:tmp[2]] = str(tmp[1])
                            seqs1[b]=tmp
                            b+=1
                            a+=1

                        #print("seqs1",seqs1)


                        
                        g = ''
                        g = g.join(graphic) 
                        g = Seq(g)                        
                        g = g.reverse_complement()
                        
                        #print("cols")
                        #if len(blastresult) >0 :
                        cols= ["QueryID","SubjectID","PercID","MatchLength","Mismatch","Gaps","Qstart","Qend","S_start","S_end","Evalue","bitscore","Q_length","S_length","Q_MatchSeq","S_MatchSeq"]
                        #print("blst")
                        blst = pd.DataFrame(blastresult)
                        blst = blst.rename(columns={'f0':cols[0],'f1':cols[1],'f2':cols[2],'f3':cols[3],'f4':cols[4],'f5':cols[5],'f6':cols[6],'f7':cols[7],'f8':cols[8],'f9':cols[9],'f10':cols[10],'f11':cols[11],'f12':cols[12],'f13':cols[13],'f14':cols[14],'f15':cols[15]})
                        blst = pd.DataFrame.to_dict(blst)
                        #print("endblastnprobes")
                        return [uniquesbad,uniques,fltrblastbad,fltrblastok,str(count-1),seqs1,g,blst]
                    else:
                        print("WARNING: No BLAST hits were found.")
                        print("WARNING: No BLAST hits were found.")
                        print("WARNING: No BLAST hits were found.")
                        print("WARNING: No BLAST hits were found.")
                        print("WARNING: No BLAST hits were found.")
                        print("WARNING: No BLAST hits were found.")
                        print("WARNING: No BLAST hits were found.")
                        print()
                        print("All preliminary probe pairs will be used.")
                        print()
                        count,seqs,g = noblast(newlist1,fullseq1,maxprobe1,numbr1,cdna1)
                        uniquesbad,uniques,fltrblastbad,fltrblastok,blst = [],[],[],[],None
                        #print("endblastnprobes")
                        return [uniquesbad,uniques,fltrblastbad,fltrblastok,str(count-1),seqs,g,blst]
                else:
                    print("WARNING: No BLAST hits were found.")
                    print("WARNING: No BLAST hits were found.")
                    print("WARNING: No BLAST hits were found.")
                    print("WARNING: No BLAST hits were found.")
                    print("WARNING: No BLAST hits were found.")
                    print("WARNING: No BLAST hits were found.")
                    print("WARNING: No BLAST hits were found.")
                    print()
                    print("All preliminary probe pairs will be used.")
                    print()
                    uniquesbad,uniques,fltrblastbad,fltrblastok,blst = [],[],[],[],None
                    count,seqs,g = noblast(newlist1,fullseq1,maxprobe1,numbr1,cdna1)
                    #print("endblastnprobes")
                    return [uniquesbad,uniques,fltrblastbad,fltrblastok,str(count-1),seqs,g,blst]
            finally:
                if fail != False:
                    print("It seems there was an error with BLAST. The program will try to make probes without running BLAST.")
                    partial = noblast(newlist,fullseq,maxprobe,numbr,cdna)
                    #print("endblastnprobes")
                    return["BLAST Fail","BLAST Fail","BLAST Fail","BLAST Fail",partial,"BLAST Fail"]

    else:
        #print("endblastnprobes")
        pass