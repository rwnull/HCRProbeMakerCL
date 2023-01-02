## Commandline form of hcr probemaker
## Version1.1 2022August

#from dataclasses import is_dataclass
import os,datetime, sys
from vers import vers
from mainscript_core import cleanup
# importing hcr maker subscripts
#from batch import fastbatch as fstbtch
import maker37
from clscript import cl, action
from CoD import creatorofdirs as cod

sys.tracebacklimit=0

'''if batchfile == None:
    ampli = list(str(amplifier).split(','))
    if len(list(ampli)) == 1:
        ampli = list(str(amplifier).split(','))
        action(hp,ampli[0],name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args)

    else:
        for xamp in amplifier:
            action(hp,xamp,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args)

else:
    pass'''




hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args = cl()

def hcr(hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args):
    sys.tracebacklimit=0
    if batchfile == None:
        ampli = list(str(amplifier).split(','))
        if len(list(ampli)) == 1:
            ampli = list(str(amplifier).split(','))
            action(hp,ampli[0],name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args)

        else:
            for xamp in amplifier:
                action(hp,xamp,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args)

    else:
        pass


hcr(hp,amplifier,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args)

'''    ## Sending inputs to the maker algo  
    #print(maker37.maker(name,seq,amplifier,pause,polyAT,polyCG,txpttemp,numbr,cgupper,cglower,dirslist[0],dirslist[1],dirslist[2],dirslist[3],dirslist[4],maxprobes))
        results = maker37.maker(name,seq,amplifier,pause,polyAT,polyCG,txpttemp,numbr,cgupper,cglower,dirslist[0],dirslist[1],dirslist[2],dirslist[3],dirslist[4],maxprobes)

        for line in results:
            if type(line) is dict:
                for key, value in line.items():
                    if type(value) is dict:
                        for vkey, vvalue in value.items():
                            print(vvalue)
                    elif type(value) is list:
                        alist = len(value)
                        i=0
                        valuetemp = ""

                        while i < alist:
                            valuetemp = valuetemp + str(value[i]) + '\t' 
                            i+=1
                        print(valuetemp)
                    else:
                        print(value)

            else:
                e = len(line)
                i = 0 
                while i < e:
                    print(line[i])
                    i+=1


    ## Code sending results to a file
        byline = vers()
        onm = str(amplifier)+'_'+str(name)+'_'+str(filenm)

        if savevariable == 'T':
            with open(os.path.join(str(opath),onm), 'w') as f:
                f.write(str(datetime.date.today())+"\n\n"+str(byline)+"\n\n\n")
                for line in results:
                    if type(line) is dict:
                        for key, value in line.items():
                            if type(value) is dict:
                                for vkey, vvalue in value.items():
                                    f.write(str(vvalue)+'\n')
                            elif type(value) is list:
                                alist = len(value)
                                i=0
                                valuetemp = ""
                                while i < alist:
                                    valuetemp = valuetemp + str(value[i]) + '\t' 
                                    i+=1
                                f.write(str(valuetemp)+'\n')
                            else:
                                f.write(str(value)+'\n')

                    else:
                        e = len(line)
                        i = 0 
                        while i < e:
                            f.write(str(line[i])+'\n')
                            i+=1
                f.write('\n')
                f.write('\n')
                f.write('INPUTS USED FOR THESE RESULTS')
                f.write('\n\r')
                argstemp = str(args).split(',')
                for line in list(argstemp):    
                    line = ((str(line).strip(")")).replace("=","\t")).replace("Namespace(","\t")     
                    f.write(line+'\n\t')
            f.close()'''


