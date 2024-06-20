#from amp import amp
import pandas as pd
import os, argparse,sys
from vers import vers
from CoD import creatorofdirs as cod
import datetime

# establishing options for the script
parser = argparse.ArgumentParser()
 
# Adding optional arguments
parser.add_argument("-old","-oldAmp", "--Old_amplifier", help = "*REQUIRED INPUT*   Indicate the old amplifier initiator sequence you want to replace in these probes. Supports B1-B5,B7,B9,B10,B11,B13,B14,B15,B17,S10,S23,S25,S34,S35, and S41. Example: -oldAmp B1 ")
parser.add_argument("-new","-newAmp", "--New_amplifier", help = "*REQUIRED INPUT*   Indicate the replacement amplifier. Supports B1-B5,B7,B9,B10,B11,B13,B14,B15,B17,S10,S23,S25,S34,S35, and S41. Example: -newAmp B5 ")
parser.add_argument("-in", "--in_file", help = "*REQUIRED INPUT*   Provide the path to the input file is. Example: '/home/PathtoInput/Opool/OldInitiatorProbes.xlsx' Must be in IDT opool submission format.")

# Initialization of optional variables
pause = 0
polyAT = 10000
polyCG = 10000
txpttemp = None
numbr = 10000
cgupper = 1.00
cglower = 0.00
maxprobes = 'y'


amps = {
    "B1" : ["GAGGAGGGCAGCAAACGGAA","TAGAAGAGTCTTCCTTTACG"],
    "B2" : ["CCTCGTAAATCCTCATCAAA","AAATCATCCAGTAAACCGCC"],
    "B3" : ["GTCCCTGCCTCTATATCTT","TTCCACTCAACTTTAACCCG"],
    "B4" : ["CCTCAACCTACCTCCAACAA","ATTCTCACCATATTCGCTTC"],
    "B5" : ["CTCACTCCCAATCTCTATAA","AACTACCCTACAAATCCAAT"],
    "B7" : ["CTTCAACCTCCACCTACCAA","AATCCAATCCCTACCCTCAC"],
    "B9" : ["CACGTATCTACTCCACTCAA","AATCAGCACACTCCCAACCC"],
    "B10" : ["CCTCAAGATACTCCTCTAAA","AACCTACTCGACTACCCTAG"],
    "B11" : ["CGCTTAGATATCACTCCTAA","AAACGTCGACCACACTCATC"],
    "B13" : ["AGGTAACGCCTTCCTGCTAA","AATTATGCTCAACATACAAC"],
    "B14" : ["AATGTCAATAGCGAGCGAAA","AACCCTATATTTCTGCACAG"],
    "B15" : ["CAGATTAACACACCACAAAA","AAGGTATCTCGAACACTCTC"],
    "B17" : ["CGATTGTTTGTTGTGGACAA","AAGCATGCTAATCGGATGAG"],
    "S10" : ["AGCCCATTAGATAA","AACGTCGGATG"],
    "S23" : ["TCGAAGTCGTATAA","AAGGGTGGTCG"],
    "S25" : ["GGGTTCAGTCTAAA","AACGTCGGAGT"],
    "S34" : ["AGCATCTTCCATAA","AACGGTCGGTG"],
    "S35" : ["ACGACATGTACTAA","AAGCTACCACC"],
    "S41" : ["TCCTTTGCAACAAA","AAGCTCGACGT"]
}

roots = cod()
MEDIA_ROOT,BLAST_ROOT,MEDIA_FASTA,MEDIA_OPOOL,MEDIA_OLIGO,MEDIA_TXT = roots[0],roots[1],roots[2],roots[3],roots[4],roots[5]


def newname(names,old,new):
    #sys.tracebacklimit=0
    newname = str(names).replace(str(old),str(new))
    return(newname)

def swap(seq,old,new,dire):
    #sys.tracebacklimit=0
    seq = pd.ExcelFile(seq,"openpyxl")
    seqseq = list(seq.parse()["Sequence"])
    seqnm = list(seq.parse()["Pool name"])
    newseqs = ["a"]*(len(seqseq))
    newoligoseqs = ["a"]*len(seqseq)
    seqs = len(seqseq)
    sc = "25nm"
    pu = "STD"
    
    #print(new)
    for newinit in new:
        p=0
        #print(newinit)
        while p < seqs:
            for sequence in seqseq:
                if str(amps[old][0]) in str(sequence):
                    new0 = str(sequence).replace(str(amps[old][0]),str(amps[newinit][0]))
                    #print(new0)#,seqs)
                    name = newname(seqnm[p],old,newinit)
                    oname1 = str(name+'_'+str(p+1)+'A')
                    newseqs[p] = [str(name),str(new0)]
                    newoligoseqs[p]= [str(oname1),str(new0),sc,pu]
                    p+=1
                elif str(amps[old][1]) in str(sequence):
                    new1 = str(sequence).replace(str(amps[old][1]),str(amps[newinit][1]))
                    #print(new1)
                    name = newname(seqnm[p],old,newinit)
                    oname2 = str(name+'_'+str(p)+'B')
                    newseqs[p] = [str(name),str(new1)]
                    newoligoseqs[p]=[str(oname2),str(new1),sc,pu]
                    p+=1     
                else:
                    name =seqnm[p]
                    newseqs[p] = [str(name),str(sequence)]
                    newoligoseqs[p]= [str(name),str(sequence),sc,pu]
                    p+=1  
        #
        x = pd.DataFrame(data=newseqs, columns=["Pool name","Sequence"])
        x = x.set_index("Pool name")  
        x.to_excel(os.path.join(dire,(name+"_OPool_initiatorswap.xlsx")))

        y = pd.DataFrame(data=newoligoseqs, columns=["Name","Sequence","Scale","Purification"])
        y = y.set_index("Name")
        y.to_excel(os.path.join(dire,(name+"_OligoOrder_initiatorswap.xlsx")))

        with open(os.path.join(dire,(name+"ReadMe_initiatorswap.txt")),"w") as z:
            z.write(vers()+"\r\n\r\n")
            z.write("This file serves as a reminder that oligos for use with "+str(newinit)+" were created from: "+str(old)+", on "+str(datetime.date.today()))
            z.close    

    return(x,y)

args = parser.parse_args()
if args.Old_amplifier:
    old = str(args.Old_amplifier).upper()
if args.New_amplifier:
    if len(list(args.New_amplifier)) == 1:
        new = list(str(args.New_amplifier).upper())
        #print(new)
    else:
        new = list(str(args.New_amplifier).upper().split(','))
        #print(new)
if args.in_file:
    seq = os.path.abspath(str(args.in_file))
    dire,file = os.path.split(seq)
    #print(dire)
    if os.path.exists(os.path.join(dire,"AmplifierSwap")):
        dire = os.path.join(dire,"AmplifierSwap")
    else:
        dire = os.mkdir(str(os.path.join(dire,"AmplifierSwap")))
    


a=swap(seq,old,new,dire)
print("Your new oligos and opool can be found in this directory: "+str(dire))

