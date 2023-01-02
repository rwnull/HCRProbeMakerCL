from clscript import action
from CoD import creatorofdirs as cod
import os,sys


initializevals = {
    "hp": None, 
    "txptome": None,
    "tpath" :None,
    "txpttemp": None,
    "outtemp" : None,
    "opath": None,
    "filenm": None,
    "batchfile":None,
    "pause" :0,
    "polyAT": 10000,
    "polyCG": 10000,
    "numbr": 10000,
    "cgupper": 1.00,
    "cglower": 0.00,
    "maxprobes": 'y',
    "dirslist": cod(),
    "savevariable":'f',
    }


def hcr(amplifier,name,seq,**kwargs):
    sys.tracebacklimit=0
    l=initializevals
    l["ampli"] = amplifier
    l["name"] = name
    l["seq"] = seq
    if kwargs:
        for k in kwargs:
            print(k)
            if str(k) == "o" or str(k) == "outpath" or str(k) == "opath" or str(k)=="out_file":
                opath,filenm = os.path.split(os.path.abspath(str(kwargs[k])))
                l["opath"] = opath
                l["filenm"] = filenm
            else:
                l[k] = kwargs[k]
            print(l)

    args = l
    hp,ampli,name,seq,cglower,cgupper,polyAT,polyCG,pause,numbr,maxprobes,txptome,tpath,txpttemp,outtemp,opath,filenm,batchfile,dirslist,savevariable,args = l["hp"],l["ampli"],l["name"],l["seq"],l["cglower"],l["cgupper"],l["polyAT"],l["polyCG"],l["pause"],l["numbr"],l["maxprobes"],l["txptome"],l["tpath"],l["txpttemp"],l["outtemp"],l["opath"],l["filenm"],l["batchfile"],l["dirslist"],l["savevariable"],args
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

    return()