import os,argparse,sys
from vers import vers
from mainscript_core import cleanup, cleanup2
# importing hcr maker subscripts
from hairpinseq import hairpins
from CoD import creatorofdirs as cod
import maker37
import datetime
from pathlib import Path
from output import output

sys.tracebacklimit=0


def cl():
    sys.tracebacklimit=0
    parser = argparse.ArgumentParser()
    
    # Adding optional arguments
    parser.add_argument("-amp", "--amplifier", help = "Which amplifier you intend to use with these probes. Supports B1-B5,B7,B9,B10,B11,B13,B14,B15,B17,S10,S23,S25,S34,S35, and S41. Example: -amp B1 ")
    parser.add_argument("-name", "--seq_name", help = "*REQUIRED INPUT*   What is the gene name? Example: eGFP")
    parser.add_argument("-seq", "--full_target_seq", help = "*REQUIRED INPUT*   Enter the sense sequence of your cDNA.")
    parser.add_argument("-cg", "-gc", "--gc_range", help = "Set the lower and upper limits of target sequence GC content from lowest to highest allowable.  Example: -gc 20-75")
    parser.add_argument("-polyAT","-polyTA", "--polyAT_run_max", help = "Longest permitted homopolymeric run of A or T.  Example: -polyAT 5  <-- largest run of A or T will be AAAAA or TTTTT")
    parser.add_argument("-polyCG","-polyGC", "--polyGC_run_max", help = "Longest permitted homopolymeric run of G or C.  Example: -polyCG 4  <-- largest run of G or C will be GGGG or CCCC")
    parser.add_argument("-pause", "--five_prime_delay", help = "How many bases from 5' end of the sequence before starting to design probes hybridize? ex. 100 ")
    parser.add_argument("-b", "--blastn_ref", help = "Provide the path to your transcriptome. Using this optional (not required to run the script) command indicates that you want to blast potential probe pairs against a reference. Example: 'C:\Transcriptomes\mytranscriptome.fasta' or '/home/Transcriptomes/mytranscriptome.fa' ")
    parser.add_argument("-prnum", "-maxpr", "--max_num_probepairs", help = "Enter an integer if you want to limit the number of probe pairs reported. If the value entered is greater than what is possible to be made, all pairs will be returned. Not entering a value will always return the maximum number of probes found that meet the other criteria specified. ")
    parser.add_argument("-hairpinseqs","-hpseqs", "--Hairpin_Sequences", help="List the sequences of the hairpins. Example: -hairpinseqs 'B13' ")




    # Initialization of optional variables
    hp = None 
    amplifier = None
    name = None
    seq = None
    txptome = None
    tpath = None
    txpttemp = None
    outtemp = None
    opath = None
    filenm = None
    batchfile = None
    pause = 0
    polyAT = 10000
    polyCG = 10000
    numbr = 10000
    cgupper = 1.00
    cglower = 0.00
    maxprobes = 'y'




    dirslist = cod()

    # Read arguments from command line and create variables
    args = parser.parse_args()
    savevariable = 'f'


    if args.Hairpin_Sequences:
        try:
            hp = args.Hairpin_Sequences.upper()
            print(hairpins(hp))
        except:
            print()
            print()
            print("You must choose an amplifier from the following list. B1-B5,B7,B9-B11,B13-B15,B17,S10,S23,S25,S34,S35, or S41  Example: -amp B7")
            print()
            raise AssertionError  
    else:
        hp = None
    if args.amplifier:
        amps = ['B1','B2','B3','B4','B5','B7','B9','B10','B11','B13','B14','B15','B17','S10','S23','S25','S34','S35','S41']
        if (str(args.amplifier).upper()).count("B") + (str(args.amplifier).upper()).count("S")<=1:
            #print((str(args.amplifier).upper()).count("B") + (str(args.amplifier).upper()).count("S"))
            try:
                amplifier = args.amplifier.upper()
                
                if amplifier in amps:
                    print("Amplifier Chosen: % s" % (str(amplifier)))
                else:
                    print()
                    print()
                    print("You must choose one of the following amplifiers, please make sure you have elected one. B1-B5,B7,B9-B11,B13-B15,B17,S10,S23,S25,S34,S35, or S41  Example: -amp B7")
                    print()
                    raise AssertionError
            except:
                print()
                print()
                print("You must choose an amplifier from the following list. B1-B5,B7,B9-B11,B13-B15,B17,S10,S23,S25,S34,S35, or S41  Example: -amp B7")
                print()
                raise AssertionError   
        else:
            amplifier = list(((str(args.amplifier).upper()).split(',')))
            amplifier2 = list("a"*len(amplifier))
            i=0
            print(amplifier)
            for option in amplifier:
                if option in amps:
                    amplifier2[i] = option
                    i+=1
                else:
                    whoops = str(option) + " is not a valid amplifier. Do you want to continue with the program using the other valid amplifiers? Y/n   "
                    stop = str(input(whoops)).upper()
                    if stop == "Y":
                        pass
                    else:
                        whoops2 = "Would you like to replace "+str(option)+" with a valid amplifier? Y/n   "
                        whoops2 = input(whoops2)
                        if str(whoops2).upper() == "Y":
                            new = str(input("Which amplifier do you want to use?  ")).upper()
                            amplifier.append(new)
                        else:
                            exit()
            for option in amplifier2:
                if "a" in amplifier2:
                    amplifier2.remove('a')
            amplifier = amplifier2
    else:
            print()
            print()
            print("You must select an amplifier from the following list. B1-B5,B7,B9-B11,B13-B15,B17,S10,S23,S25,S34,S35, or S41")
            print()
            raise AssertionError   
    if args.seq_name:
        try:
            name = str(args.seq_name)
            name = str(cleanup2(name))
            print("Name Chosen: % s" % (str(name)))
        except:
            print()
            print()
            print('There must be an ID given for the sequence. Please try again using the flag -name YourSequenceName')
            print()
            raise AssertionError
    else:
            print()
            print()
            print('There must be an ID given for the sequence. Please try again using the flag -name YourSequenceName')
            print()
            raise AssertionError
    if args.full_target_seq:
        try:
            seq = args.full_target_seq.upper()
            seq = cleanup(seq)
            print("The sequence given for probe production is: % s" % (str(seq)))
        except:
            print()
            print()
            print('There must be a cDNA or mRNA sequence provided. Please try again using the flag "-seq". For example: -seq ATTGCGGAGC or -seq AUGGCUAAUCG')
            print()
            raise AssertionError           
    else:
        print()
        print()
        print('There must be a cDNA or mRNA sequence provided. Please try again using the flag "-seq". For example: -seq ATTGCGGAGC or -seq AUGGCUAAUCG')
        print()
        raise AssertionError
    if args.gc_range:
        try:
            cglower, cgupper = args.gc_range.split("-")
            cglower = float(int(cglower)/100.0)
            cgupper = float(int(cgupper)/100.0)
            if cglower < cgupper:
                pass
            else:
                tem = cglower
                cglower = cgupper
                cgupper = tem    
                tem = None 
            print("Percent CG lower limit specified: % s percent" % (str(int(cglower*100)))) 
            print("Percent CG upper limit specified: % s percent" % (str(int(cgupper*100))))
        except:
            print()
            print()
            print('There should be two numerical values (the lower and upper limits) that are separated by a single hyphen. Example: 23-45 ')
            print()
            raise AssertionError 
    if args.polyAT_run_max:
        polyAT = args.polyAT_run_max
        print("AT homopolymer limit specified: % s" % (str(polyAT)))
    if args.polyGC_run_max:
        polyCG = int(args.polyGC_run_max)
        print("GC homopolymer limit specified: % s" % (str(polyCG)))
    if args.five_prime_delay:
        pause = int(args.five_prime_delay)
        print("Probes will begin to be made after the first % s bases." % (str(pause)))
    if args.max_num_probepairs:
        numbr = int(args.max_num_probepairs)
        maxprobes = 'n'
        print("The maximum number of probe pairs made will be % s." % (str(numbr)))
    if args.blastn_ref:
        txpttemp = os.path.abspath(os.path.expandvars(os.path.expanduser(args.blastn_ref)))
        tpath, txptome = os.path.split(txpttemp) #args.blastn_ref)
        ext = ["fa","fasta"]
        if str(txptome.split(".")[-1]) in ext :
            print("Transcriptome reference: % s, located in the directory % s" % (str(txptome),str(tpath)))
            print("Full path is "+txpttemp)
        else:
            print()
            print()
            print("The use of the blast function requires a .fa or .fasta file format. Please choose a different file.")
            print()
            raise AssertionError




    return(hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args)



def clb():
    sys.tracebacklimit=0
    # Initialization of optional variables
    hp = "" 
    amplifier = ""
    name = ""
    seq = ""
    txptome = None
    tpath = None
    txpttemp = None
    outtemp = ""
    opath = ""
    filenm = ""
    batchfile = ""
    pause = 0
    polyAT = 10000
    polyCG = 10000
    numbr = 10000
    cgupper = 1.00
    cglower = 0.00
    maxprobes = 'y'



    parser = argparse.ArgumentParser()
    
    # Adding optional arguments
    parser.add_argument("-amp", "--amplifier", help = "Which amplifier you intend to use with these probes. Supports B1-B5,B7,B9,B10,B11,B13,B14,B15,B17,S10,S23,S25,S34,S35, and S41. Example: -amp B1 ")
    #parser.add_argument("-ramp", "--rand_amplifier", help = "Have the program choose a random amplifier. Supports B1-B5,B7,B9,B10,B11,B13,B14,B15,B17,S10,S23,S25,S34,S35, and S41. Example: -amp B1 ")
    #parser.add_argument("-ordamp", "--ordered_amplifier", help = "The program will take a list of amplifiers and apply them to successive probe sets. Batch processing only. Supports B1-B5,B7,B9,B10,B11,B13,B14,B15,B17,S10,S23,S25,S34,S35, and S41. Example: -amp B1 ")

    #parser.add_argument("-name", "--seq_name", help = "*REQUIRED INPUT*   What is the gene name? Example: eGFP")
    #parser.add_argument("-seq", "--full_target_seq", help = "*REQUIRED INPUT*   Enter the sense sequence of your cDNA.")
    parser.add_argument("-cg", "-gc", "--gc_range", help = "Set the lower and upper limits of target sequence GC content from lowest to highest allowable.  Example: -gc 20-75")
    parser.add_argument("-polyAT","-polyTA", "--polyAT_run_max", help = "Longest permitted homopolymeric run of A or T.  Example: -polyAT 5  <-- largest run of A or T will be AAAAA or TTTTT")
    parser.add_argument("-polyCG","-polyGC", "--polyGC_run_max", help = "Longest permitted homopolymeric run of G or C.  Example: -polyCG 4  <-- largest run of G or C will be GGGG or CCCC")
    parser.add_argument("-pause", "--five_prime_delay", help = "How many bases from 5' end of the sequence before starting to design probes hybridize? ex. 100 ")
    parser.add_argument("-b", "--blastn_ref", help = "Provide the path to your transcriptome. Using this optional (not required to run the script) command indicates that you want to blast potential probe pairs against a reference. Example: 'C:\Transcriptomes\mytranscriptome.fasta' or '/home/Transcriptomes/mytranscriptome.fa' ")
    parser.add_argument("-prnum", "-maxpr", "--max_num_probepairs", help = "Enter an integer if you want to limit the number of probe pairs reported. If the value entered is greater than what is possible to be made, all pairs will be returned. Not entering a value will always return the maximum number of probes found that meet the other criteria specified. ")
    parser.add_argument("-o", "--out_file", help = "Provide the path and file name to where the results should be saved. Example: 'C:\PathtoResult\myresult.txt' or '/home/PathtoResult/myresult.txt' ")
    #parser.add_argument("-hairpinseqs","-hpseqs", "--Hairpin_Sequences", help="List the sequences of the hairpins. Example: -hairpinseqs 'B13' ")
    parser.add_argument("-batch", "--batch", help="If you have a fasta file with multiple sequences you would like to process, insert the path to the file here.")









    dirslist = cod()
    
    # Read arguments from command line and create variables
    args = parser.parse_args()
    
    savevariable = 'f'

    if args.amplifier:
        amps = ['B1','B2','B3','B4','B5','B7','B9','B10','B11','B13','B14','B15','B17','S10','S23','S25','S34','S35','S41']
        if (str(args.amplifier).upper()).count("B") + (str(args.amplifier).upper()).count("S")<=1:
            #print((str(args.amplifier).upper()).count("B") + (str(args.amplifier).upper()).count("S"))
            try:
                amplifier = args.amplifier.upper()
                
                if amplifier in amps:
                    print("Amplifier Chosen: % s" % (str(amplifier)))
                else:
                    print()
                    print()
                    print("You must choose one of the following amplifiers, please make sure you have elected one. B1-B5,B7,B9-B11,B13-B15,B17,S10,S23,S25,S34,S35, or S41  Example: -amp B7")
                    print()
                    raise AssertionError
            except:
                print()
                print()
                print("You must choose an amplifier from the following list. B1-B5,B7,B9-B11,B13-B15,B17,S10,S23,S25,S34,S35, or S41  Example: -amp B7")
                print()
                raise AssertionError   
        else:
            amplifier = list(((str(args.amplifier).upper()).split(',')))
            amplifier2 = list("a"*len(amplifier))
            i=0
            print(amplifier)
            for option in amplifier:
                if option in amps:
                    amplifier2[i] = option
                    i+=1
                else:
                    whoops = str(option) + " is not a valid amplifier. Do you want to continue with the program using the other valid amplifiers? Y/n   "
                    stop = str(input(whoops)).upper()
                    if stop == "Y":
                        pass
                    else:
                        whoops2 = "Would you like to replace "+str(option)+" with a valid amplifier? Y/n   "
                        whoops2 = input(whoops2)
                        if str(whoops2).upper() == "Y":
                            new = str(input("Which amplifier do you want to use?  ")).upper()
                            amplifier.append(new)
                        else:
                            exit()
            for option in amplifier2:
                if "a" in amplifier2:
                    amplifier2.remove('a')
            amplifier = amplifier2
    else:
            print()
            print()
            print("You must select an amplifier from the following list. B1-B5,B7,B9-B11,B13-B15,B17,S10,S23,S25,S34,S35, or S41")
            print()
            raise AssertionError   
    '''#if args.seq_name:
        try:
            name = str(args.seq_name)
            print("Name Chosen: % s" % (str(name)))
        except:
            print()
            print()
            print('There must be an ID given for the sequence. Please try again using the flag -name YourSequenceName')
            print()
            raise AssertionError
    #else:
            print()
            print()
            print('There must be an ID given for the sequence. Please try again using the flag -name YourSequenceName')
            print()
            raise AssertionError
    #if args.full_target_seq:
        try:
            seq = args.full_target_seq.upper()
            seq = cleanup(seq)
            print("The sequence given for probe production is: % s" % (str(seq)))
        except:
            print()
            print()
            print('There must be a cDNA or mRNA sequence provided. Please try again using the flag "-seq". For example: -seq ATTGCGGAGC or -seq AUGGCUAAUCG')
            print()
            raise AssertionError           
    #else:
        print()
        print()
        print('There must be a cDNA or mRNA sequence provided. Please try again using the flag "-seq". For example: -seq ATTGCGGAGC or -seq AUGGCUAAUCG')
        print()
        raise AssertionError'''
    if args.gc_range:
        try:
            cglower, cgupper = args.gc_range.split("-")
            cglower = float(int(cglower)/100.0)
            cgupper = float(int(cgupper)/100.0)
            if cglower < cgupper:
                pass
            else:
                tem = cglower
                cglower = cgupper
                cgupper = tem    
                tem = None 
            print("Percent CG lower limit specified: % s percent" % (str(int(cglower*100)))) 
            print("Percent CG upper limit specified: % s percent" % (str(int(cgupper*100))))
        except:
            print()
            print()
            print('There should be two numerical values (the lower and upper limits) that are separated by a single hyphen. Example: 23-45 ')
            print()
            raise AssertionError 
    if args.polyAT_run_max:
        polyAT = int(args.polyAT_run_max)
        print("AT homopolymer limit specified: % s" % (str(polyAT)))
    if args.polyGC_run_max:
        polyCG = int(args.polyGC_run_max)
        print("GC homopolymer limit specified: % s" % (str(polyCG)))
    if args.five_prime_delay:
        pause = int(args.five_prime_delay)
        print("Probes will begin to be made after the first % s bases." % (str(pause)))
    if args.max_num_probepairs:
        numbr = int(args.max_num_probepairs)
        maxprobes = 'n'
        print("The maximum number of probe pairs made will be % s." % (str(numbr)))
    if args.blastn_ref:
        txpttemp = os.path.abspath(os.path.expandvars(os.path.expanduser(args.blastn_ref)))
        tpath, txptome = os.path.split(txpttemp) #args.blastn_ref)
        ext = ["fa","fasta"]
        if str(txptome.split(".")[-1]) in ext :
            print("Transcriptome reference: % s, located in the directory % s" % (str(txptome),str(tpath)))
            print("Full path is "+txpttemp)
        else:
            print()
            print()
            print("The use of the blast function requires a .fa or .fasta file format. Please choose a different file.")
            print()
            raise AssertionError
    if args.out_file:
        outtemp = os.path.abspath(os.path.expandvars(os.path.expanduser(args.out_file)))
        opath, filenm = os.path.split(outtemp)
        ext = ["txt","rtf"]
        savevariable = 'T'
        if str(filenm).split('.')[-1] in ext:
            print("File with results is known as % s, and is located in the directory % s" % (str(filenm),str(opath)))
        else:
            print()
            print()
            print('The use of the -out or --out_file flag requires a path pointing to a file ending with ".txt" or ".rtf". Example: -o C:/pathtooutput/output.txt or --out_file /home/path/output.rtf')
            print()
            raise AssertionError
    else:
        opath = str(dirslist[5])
    if args.batch:
        batchfile = os.path.abspath(os.path.expandvars(os.path.expanduser(args.batch)))
        print("The directory being used for the batch is: "+str(batchfile))

    #print(type(hp),type(amplifier),type(name),type(seq),type(cglower),type(cgupper),type(polyAT),type(polyCG),type(pause),type(numbr),type(maxprobes),type(txptome),type(tpath),type(txpttemp),type(outtemp),type(opath),type(filenm),type(batchfile),type(dirslist),type(savevariable),type(args))
    return(hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args)


    
def action(hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args):
        ## Sending inputs to the maker algo  
    #print(maker37.maker(name,seq,amplifier,pause,polyAT,polyCG,txpttemp,numbr,cgupper,cglower,dirslist[0],dirslist[1],dirslist[2],dirslist[3],dirslist[4],maxprobes))
    sys.tracebacklimit=0
    MEDIA_ROOT,BLAST_ROOT,MEDIA_FASTA,MEDIA_OPOOL,MEDIA_OLIGO,MEDIA_TXT = str(dirslist[0]),str(dirslist[1]),str(dirslist[2]),str(dirslist[3]),str(dirslist[4]),str(dirslist[5])
    results,count=(maker37.maker(name,seq,amplifier,pause,polyAT,polyCG,txpttemp,numbr,cgupper,cglower,MEDIA_ROOT,BLAST_ROOT,MEDIA_FASTA,MEDIA_OPOOL,MEDIA_OLIGO,MEDIA_TXT,maxprobes))
    #print(results)
    #print((name,seq,amplifier,pause,polyAT,polyCG,txpttemp,numbr,cgupper,cglower,MEDIA_ROOT,BLAST_ROOT,MEDIA_FASTA,MEDIA_OPOOL,MEDIA_OLIGO,MEDIA_TXT,maxprobes))
    #results=list(maker37.maker(name,seq,amplifier,pause,polyAT,polyCG,txpttemp,numbr,cgupper,cglower,MEDIA_ROOT,BLAST_ROOT,MEDIA_FASTA,MEDIA_OPOOL,MEDIA_OLIGO,MEDIA_TXT,maxprobes))
    #print(type(results))
    i=1

    where = os.path.join(str(MEDIA_TXT),str(amplifier+'_'+name+"_"+str(count)+'_Delay'+str(pause)))#str(amplifier)+"_"+str(filenm)+".txt")
    whereopool = os.path.join(str(MEDIA_OPOOL),str(amplifier+'_'+name+"_"+str(count)+'_Delay'+str(pause)))#str(amplifier)+"_"+str(filenm)+".txt")
    whereoligo = os.path.join(str(MEDIA_OLIGO),str(amplifier+'_'+name+"_"+str(count)+'_Delay'+str(pause)))#str(amplifier)+"_"+str(filenm)+".txt")    

    if results != None:
        
        print("It looks like we found some probes. Check here "+str(where)+".txt to see the results.")
        print("You can find an IDT opool submission form located here "+str(whereopool)+"oPool.xlsx.")
        print("And you can find a bulk primer order here: "+str(whereoligo)+"oligo.xlsx, this is a rare type of submission for generating a lifetime supply.")
        with open(where,"w") as f:
            #print(str(f))
            for line in results:#[0:12]:
                if type(line) is dict:
                    for key, value in line.items():
                        if type(value) is dict:
                            for vkey, vvalue in value.items():
                                f.write(str(vvalue))
                        elif type(value) is list:
                            alist = len(value)
                            i=0
                            valuetemp = str()
                            while i < alist:
                                valuetemp = valuetemp + str(value[i]) + "\t"
                                i+=1
                            f.write(str(valuetemp))
                        else:
                            f.write(str(value))

                else:
                    e = len(line)
                    i = 0 
                    while i < e:
                        f.write(str(line[i]))
                        i+=1


        ## Code sending results to a file
            byline = vers()
            if filenm:
                onm = str(amplifier)+'_'+str(name)+'_'+str(filenm)
            else:
                onm = str(amplifier)+'_'+str(name)+'_'+str(batchfile)
            if savevariable == 'T':
                with open(os.path.join(str(opath),onm), 'w') as f2:
                    f2.write(str(datetime.date.today())+"\n\n"+str(byline)+"\n\n\n")
                    for line in results:
                        if type(line) is dict:
                            for key, value in line.items():
                                if type(value) is dict:
                                    for vkey, vvalue in value.items():
                                        f2.write(str(vvalue)+'\n')
                                elif type(value) is list:
                                    alist = len(value)
                                    i=0
                                    valuetemp = ""
                                    while i < alist:
                                        valuetemp = valuetemp + str(value[i]) + '\t' 
                                        i+=1
                                    f2.write(str(valuetemp)+'\n')
                                else:
                                    f2.write(str(value)+'\n')

                        else:
                            e = len(line)
                            i = 0 
                            while i < e:
                                f2.write(str(line[i])+'\n')
                                i+=1
                    f2.write('\n')
                    f2.write('\n')
                    f2.write('INPUTS USED FOR THESE RESULTS')
                    f2.write('\n\r')
                    argstemp = str(args).split(',')
                    for line in list(argstemp):    
                        line = ((str(line).strip(")")).replace("=","\t")).replace("Namespace(","\t")     
                        f.write(line+'\n\t')
                f.close()
                f2.close()

                print("Huzzah! We are done. Find your results here: "+str(where))

            else:
                pass
    else:
        print("Sorry there were no probes that we could make. Double check your sequence and/or loosen your constraints.")
