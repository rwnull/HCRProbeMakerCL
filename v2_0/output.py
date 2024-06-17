
from amp import amp
import numpy as np
import pandas as pd
import os, sys
from os import remove as rm
from decimal import Decimal as Dec

sys.tracebacklimit=0

def output(cdna,g,fullseq,count,amplifier,name,pause,seqs,today,polyAT,polyCG,cgupper,cglower,MEDIA_ROOT,BLAST_ROOT,MEDIA_FASTA,MEDIA_OPOOL,MEDIA_OLIGO,MEDIA_TXT,maxprobes,blst):
    #print("output")
    sys.tracebacklimit=0
    # settings allowing full viewing of dataframes
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    #print(amplifier)
    amplifier=str((amplifier).upper())
    #print(amplifier)
    test=amp(amplifier)
    uspc=test[0]
    dspc=test[1]
    upinit=test[2]
    dninit=test[3]

    def saving(l,line,iterator):
        #print("saving")
        l[int(iterator)]=str(line)
        iterator+=1
        #print("end_Saving")
        return (l,iterator)

    if int(count) > 0:
        l={}
        lllll={}
        m={}
        n={}
        o={}
        p={}
       # q={}
        b={}


        
        
        #print(amplifier,name,str(count),str(pause))

        ## creating an xlsx file and dictionary of lists for opool submission
        lpre = ["IDT OLIGO POOL FORMATTED SAMPLES\nCopy and paste into a .xlsx file to upload to IDT.\n"]
        llpre = ["\nTHIS OUTPUT IS A CONDENSED FORMAT SHOWING THE OLIGOS AS THEIR RESPECTIVE PAIRS\n"]
        store = 0
        ll = {}
        lll = ["a"]*2*len(seqs)
        llll = {}
        a=0
        ll[a] = ['Name','PairNumber','Probe1','Probe2',"\n"]
        llll[a] = ["Pool name","Sequence","\n"]
        
        while a+1 < len(seqs)+1:
            lname = str(amplifier+'_'+name+'_'+str(count)+'_Delay'+str(pause))
            #print(lname+" == results[12]")
            lup = str(upinit+uspc+str(seqs[a][1][27:52]))
            ldn = str((seqs[a][1][0:25])+dspc+dninit)
            ll[a+1] = [lname,str(a+1),lup,ldn,"\n"]
            lll[a] = [lname,lup,"\n"]
            lll[a+len(seqs)] = [lname,ldn,"\n"]
            llll[a+1] = [lname,lup,"\n"]
            llll[a+1+len(seqs)] = [lname,ldn,"\n"]
            a+=1

        l,store = saving(l,ll,store)
        lllll,store = saving(lllll,llll,store)

        


        x = pd.DataFrame(data=lll, columns=["Pool name","Sequence","\n"])
        x = x.set_index("Pool name")
        x.to_excel(os.path.join(MEDIA_OPOOL,(lname+"oPool.xlsx")))
       # x = lname+"oPool.xlsx"
      

        ## creating an xlsx file and dictionary of lists for opool submission
        store = 0
        sc = "25nm"
        pu = "STD"
        yy = ["a"]*2*len(seqs)
        a=0
        
        while a < len(seqs):
            yname1 = str(amplifier+'-'+name+'_'+count+'_'+str(a+1)+'A')
            yname2 = str(amplifier+'-'+name+'_'+count+'_'+str(a+1)+'B')
            yup = str(upinit+uspc+str(seqs[a][1][27:52]))
            ydn = str((seqs[a][1][0:25])+dspc+dninit)
            yy[a] = [yname1,yup,sc,pu,"\n"]
            yy[a+len(seqs)] = [yname2,ydn,sc,pu,"\n"]
            a+=1

        y = pd.DataFrame(data=yy, columns=["Name","Sequence","Scale","Purification","\n"])
        y = y.set_index("Name")
        y.to_excel(os.path.join(MEDIA_OLIGO,(lname+"oligo.xlsx")))
      #  y = lname+"oligo.xlsx"






        ## table dictionary of the probes and initiator seqs for a supplemental fig
        mpre = ["\nRESULTS IN FIGURE FORMAT\n"]
        store = 0
        ml = {}
        i=0
        ml[0] = ['PairNum','Initiator1','Spacer1','Hybridization1','Hybridization2','Spacer2','Initiator2',"\n"]
        while i+1 < len(seqs)+1:
           mpr = i+1
           mup = str(upinit)
           mus = str(uspc)
           mp1 = str(seqs[i][1][27:52])
           mp2 = str(seqs[i][1][0:25])
           mds = str(dspc)
           mdn = str(dninit)
           ml[i+1] = [mpr,mup,mus,mp1,mp2,mds,mdn,"\n"]
           i+=1

        m,store = saving(m,ml,store)
        
        
        ## table dictionary of the probes' hybridization locations
        npre = ["\nSAMPLES WITH cDNA LOCATION\n"]
        store = 0
        i = len(seqs)-1
        if len(seqs[i])>3:
            nl = {}
            i=len(seqs)
            nl[i] = ['PairNum','Coord1','ProbeSeq1','Coord2','Coord3','ProbeSeq2','Coord4','blastID',"\n"]
            i -= 1
            while i >= 0:
                nbpr = seqs[i][3]
                npr = i+1
                nc1 = cdna - int(seqs[i][0])
                np1 = str(seqs[i][1][0:25])	
                nc2 = nc1 - 25		
                np2 = str(seqs[i][1][27:52])
                nc3 = nc2 - 2		
                nc4 = cdna - int(seqs[i][2])
                nl[i] = [npr,nc1,np1,nc2,nc3,np2,nc4,nbpr,"\n"]
                i-=1
        else:
            nl = {}
            i=len(seqs)
            nl[i] = ['PairNum','Coord1','ProbeSeq1','Coord2','Coord3','ProbeSeq2','Coord4',"\n"]
            i -= 1
            while i >= 0:
                npr = i+1
                nc1 = cdna - int(seqs[i][0])
                np1 = str(seqs[i][1][0:25])	
                nc2 = nc1 - 25		
                np2 = str(seqs[i][1][27:52])
                nc3 = nc2 - 2		
                nc4 = cdna - int(seqs[i][2])
                nl[i] = [npr,nc1,np1,nc2,nc3,np2,nc4,"\n"]
                i-=1



        n,store = saving(n,nl,store)

        


        ## create fasta output of the in-place probes
        store = 0
        o,store = saving(o,'',store)
        o,store = saving(o,"\n>"+str(name)+" Sense Strand\n",store)
        i=len(g)
        j=0
        while j < i:
            k = j+60
            o,store = saving(o,str(g[j:k])+"\n",store)
            j = k
        
        o = list(o.values())


        ## create fasta output of the anti-sense strand of the input cDNA
        store=0       
        p,store = saving(p,'',store)
        p,store = saving(p,"\n>"+name+" Anti-Sense Strand\n",store)
        i=len(fullseq)
        j=0
        while j < i:
            k = j+60
            p,store = saving(p,str(fullseq[j:k])+"\n",store)
            j = k
        p = list(p.values())







        ## BLASTn results dictionary
        blpre = ["\n\nRESULTS FOR PROBES BLASTed AGAINST PROVIDED TRANSCRIPTOME\n\nPairs marked with '-->' are perfect matches with differing FASTA id from the query FASTA id.\nPairs marked with '*' are less perfect matches; at least 28nt match length and between 60 and 85 rawscore.\n\n"]
        store = 0
        bl = {}
        i=0
        bl[0] = ["QueryID","SubjectID","PercID","MatchLength","Mismatch","Gaps","Q_start","Q_end","S_start","S_end","evalue","bitscore","Q_MatchSeq","S_MatchSeq","\n"]
        if blst != None:
            while i+1 < len(blst["QueryID"])+1:
                bl[i+1] = [blst["QueryID"][i],blst["SubjectID"][i],blst["PercID"][i],blst["MatchLength"][i],blst["Mismatch"][i],blst["Gaps"][i],blst["Qstart"][i],blst["Qend"][i],blst["S_start"][i],blst["S_end"][i],'%.2E' % Dec(blst["Evalue"][i]),blst["bitscore"][i],blst["Q_MatchSeq"][i],blst["S_MatchSeq"][i],"\n"]
                i+=1
            b,store = saving(b,bl,store)
        else:
            b = "placeholder\n"
            blpre = ""

        if len(bl) == 1:
            bl = ""
        

        
        #print([lname,lpre,llll,llpre,ll,mpre,ml,npre,nl,o,p,blpre,bl,lname])
        #print("end_Output")
        return([lpre,llll,llpre,ll,mpre,ml,npre,nl,o,p,blpre,bl,lname]) #x,y,q
    
    else:
        #print("end_Output")
        return("foobar")



'''if blst != pd.empty() or None:
            p,store = saving(p,'\n',store)
            p,store = saving(p,'\n',store)
            p,store = saving(p,blst,store)
        else:
            pass
'''