import os,argparse
import datetime

# importing hcr maker sub-scripts
from CoD import creatorofdirs as cod
import maker37
from vers import vers
from isfasta import is_fasta



tiiiime = datetime.datetime.now()
print(tiiiime)



def writing(openfile,args,results):
    #print("writing")
    tiiime = str(datetime.datetime.now())
    openfile.write(str(vers())+"\n\n\rThis result was created at "+tiiime+'\n\rTHESE WERE THE SETTINGS AND INPUTS USED FOR THESE RESULTS\n\r')
    
    if "amplifier" in str(args).split(',')[0]:
        openfile.write(((str(args).split('gc_range')[0].split("Namespace(")[1].lower().replace("=","\t")).replace(","," ")+'\ngc_range ').replace('amplifier','amplifier(s)'))
    argstemp = str(args).split('gc_range')[1].split(',')
    for line in list(argstemp):
        line = ((str(line).strip(")")).replace("=","\t")).replace("Namespace(","").strip()     
        openfile.write(line+'\n')
    openfile.write("\n\r\n\r")    

# writing the actual results
    for line in results:
        if type(line) is dict:
            for key, value in line.items():
                if type(value) is dict:
                    for vkey, vvalue in value.items():
                        openfile.write(str(vvalue))
                        
            # From a list create a single variable with whitespace characters to be written to the open file;
                elif type(value) is list:
                    alist = len(value)
                    i=0
                    valuetemp = str()    
                # If the value of a position is a return line, omit a tab from the spacing (prevents a leading tab on newlines)
                    while i < alist:
                        if value[i] == "\n":
                            valuetemp = valuetemp + str(value[i])
                            i+=1
                        else:
                            valuetemp = valuetemp + str(value[i]) + "\t"
                            i+=1
                    openfile.write(str(valuetemp))
                else:
                    openfile.write(str(value))
        else:
            e = len(line)
            i = 0 
            while i < e:
                openfile.write(str(line[i]))
                i+=1
    openfile.write('\n\n\r')
    openfile.close()
    #print("end_writing")

# Defining a function that parses the input arguments and 
# establishes the values as variables for batch commands
def clb():
    #print("clb")
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
    low = 0

# Adding optional arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-amp", "--amplifier", help = "Which amplifier you intend to use with these probes. Supports B1-B5,B7,B9,B10,B11,B13,B14,B15,B17,S10,S23,S25,S34,S35, and S41. Example: -amp B1 ")
    parser.add_argument("-cg", "-gc", "--gc_range", help = "Set the lower and upper limits of target sequence GC content from lowest to highest allowable.  Example: -gc 20-75")
    parser.add_argument("-polyAT","-polyTA", "--polyAT_run_max", help = "Longest permitted homopolymeric run of A or T.  Example: -polyAT 5  <-- largest run of A or T will be AAAAA or TTTTT")
    parser.add_argument("-polyCG","-polyGC", "--polyGC_run_max", help = "Longest permitted homopolymeric run of G or C.  Example: -polyCG 4  <-- largest run of G or C will be GGGG or CCCC")
    parser.add_argument("-pause", "--five_prime_delay", help = "How many bases from 5' end of the sequence before starting to design probes hybridize? ex. 100 ")
    parser.add_argument("-blast", "--blastn_ref", help = "Provide the path to your transcriptome. Using this optional (not required to run the script) command indicates that you want to blast potential probe pairs against a reference. Example: 'C:\Transcriptomes\mytranscriptome.fasta' or '/home/Transcriptomes/mytranscriptome.fa' ")
    parser.add_argument("-max", "-maxpr", "--max_num_probepairs", help = "Enter an integer if you want to limit the number of probe pairs reported. If the value entered is greater than what is possible to be made, all pairs will be returned. Not entering a value will always return the maximum number of probes found that meet the other criteria specified. ")
    parser.add_argument("-min", "-minpr", "--soft_min_probepairs", help = "Enter an integer number of probe pairs desired. If the sequence is not long enough to theoretically make this number of probe pairs, the sequence will be skipped. Not entering a value will allow any number of probe pairs that meet the other criteria specified. It is possible that the theoretical limit will not be possible to be made and what is returned may be fewer than requested. ")
    parser.add_argument("-o","-out", "--output", help = "Option specifying a particular path to an output directory. Example: C:\Path\To\Desired\Directory ")
    parser.add_argument("-in", "--filein", help = "Point the program to a fasta file with one or more transcript sequences that you would like to process.")
    #parser.add_argument("-batch", "--batch", help = "If you have a fasta file with multiple sequences you would like to process, insert the path to the file here.")


# Read arguments from command line and create variables
    args = parser.parse_args()
    savevariable = 'f'

# This block will decide where to put the output directory
    if args.output:
        os.chdir(args.output)
        dirslist = cod()
        opath = str(dirslist[5])
    else:
        dirslist = cod()
        opath=str(dirslist[5])
    
# This block reads in what initiator sequence should be placed on the output probe sequences
    if args.amplifier:
        amps = ['B1','B2','B3','B4','B5','B7','B9','B10','B11','B13','B14','B15','B17','S10','S23','S25','S34','S35','S41']
        if (str(args.amplifier).upper()).count("B") + (str(args.amplifier).upper()).count("S")<=1:
            try:
                amplifier = str(args.amplifier).upper()
                amplifier2 = [amplifier]
                amplifier = amplifier2[0]
                #print(amplifier,amplifier2)
                if amplifier in amps:
                    print("Amplifier Chosen: % s" % (str(amplifier)))
                else:
                    print()
                    print()
                    print("You must choose one of the following amplifiers, please make sure you have elected one. B1-B5,B7,B9-B11,B13-B15,B17,S10,S23,S25,S34,S35, or S41  Example: -amp B7")
                    print()
                    
            except:
                print("Please check your inputs and try again.")
                print()
                exit()

        else:
            amplifier = list(((str(args.amplifier).upper()).split(',')))
            #print(len(list(amplifier)),amplifier)
            amplifier2 = list("a"*len(amplifier))
            i=0
            #print(amplifier)
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
             

# Are there any GC content limits?
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
            
        
# What are the homopolymeric run limits for polyA/T and polyC/G?
    if args.polyAT_run_max:
        polyAT = int(args.polyAT_run_max)
        print("AT homopolymer limit specified: % s" % (str(polyAT)))
    if args.polyGC_run_max:
        polyCG = int(args.polyGC_run_max)
        print("GC homopolymer limit specified: % s" % (str(polyCG)))

# Was there a specified delay to the where sequences can be made?
    if args.five_prime_delay:
        pause = int(args.five_prime_delay)
        print("Probes will begin to be made after the first % s bases." % (str(pause)))

# Setting the maximum and minimum number of probe pairs to create.
    if args.max_num_probepairs:
        numbr = int(args.max_num_probepairs)
        maxprobes = 'n'
        print("The maximum number of probe pairs made will be % s." % (str(numbr)))
    if args.soft_min_probepairs:
        low = ((int(args.soft_min_probepairs)-1)*54)+52
        print("Transcripts with fewer than % s base pairs made will be ignored because a lower limit of % s probe pairs was requested." % (str(low),str(args.soft_min_probepairs)))
    
# If a transcriptome is specified, where is it? Set the variables so that blast is triggered.    
    if args.blastn_ref:
        txpttemp = os.path.abspath(os.path.expandvars(os.path.expanduser(args.blastn_ref)))
        args.blastn_ref = txpttemp
        tpath, txptome = os.path.split(txpttemp) #args.blastn_ref)
        if is_fasta(txpttemp):#tpath,txptome):
            print("Transcriptome reference: % s, located in the directory % s" % (str(txptome),str(tpath)))
            print()
        
        else:
            print()
            print()
            print("The use of the blast function requires fasta formatted file. Please choose a different BLAST reference file.")
            print()
            

# This program allows for batch design of sequences, where is the directory containing the FASTAs?    
#    if args.batch:
#        batchfile = os.path.abspath(os.path.expandvars(os.path.expanduser(args.batch)))
#        args.batch = batchfile

# This program allows for batch design of sequences, where is the directory containing the FASTAs?    
    if args.filein:
        batchfile = os.path.abspath(os.path.expandvars(os.path.expanduser(args.filein)))
        args.filein = batchfile
    #print(amplifier)
    #print("end_clb")
    return(hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,low)


## This is a function that sends the variables//inputs to the maker algo
def action(hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args,low):
    #print("action")
    #print(amplifier)
# Create the variables for the output files
    MEDIA_ROOT,BLAST_ROOT,MEDIA_FASTA,MEDIA_OPOOL,MEDIA_OLIGO,MEDIA_TXT = str(dirslist[0]),str(dirslist[1]),str(dirslist[2]),str(dirslist[3]),str(dirslist[4]),str(dirslist[5])
    
# Push the variables to the maker script
    results,count=(maker37.maker(name,seq,amplifier,pause,polyAT,polyCG,txpttemp,numbr,cgupper,cglower,MEDIA_ROOT,BLAST_ROOT,MEDIA_FASTA,MEDIA_OPOOL,MEDIA_OLIGO,MEDIA_TXT,maxprobes,low))

    i=1

    if results:
    
    # creating file names for output
        where = os.path.join(str(MEDIA_TXT),str(amplifier+'_'+name+"_"+str(count)+'_Delay'+str(pause)+".txt"))#str(amplifier)+"_"+str(filenm)+".txt")
        whereopool = os.path.join(str(MEDIA_OPOOL),str(amplifier+'_'+name+"_"+str(count)+'_Delay'+str(pause)))#str(amplifier)+"_"+str(filenm)+".txt")
        whereoligo = os.path.join(str(MEDIA_OLIGO),str(amplifier+'_'+name+"_"+str(count)+'_Delay'+str(pause)))#str(amplifier)+"_"+str(filenm)+".txt")    
    
    # let the user know there was success and where the outputs can be found.
        print("It looks like we found some probes. Check here "+str(where)+" to see the results.")
        print()
        print("You can find an IDT opool submission form located here "+str(whereopool)+"oPool.xlsx.")
        print()
        print("And you can find a bulk primer order here: "+str(whereoligo)+"oligo.xlsx, this is a rare type of submission for generating a lifetime supply.")
        print()

    # Open the files at the specified locations and write the results
        with open(where,"w") as f:
        # writing header and settings
            writing(f,args,results)
            f.close()
            
        print('\n\r\n\r')
        print("Elapsed time was ",datetime.datetime.now()-tiiiime)
        
    else:
        print("Sorry there were no probes that we could make. Double check your sequence and/or loosen your constraints.")
        pass
    
    #print("endAction")
