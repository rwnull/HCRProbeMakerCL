import os, sys

def creatorofdirs():
    sys.tracebacklimit=0
    MEDIA_ROOT = str(os.path.abspath(os.path.expandvars(os.path.expanduser(os.path.join(os.curdir,"ProbemakerOut")))))
    MEDIA_FASTA = str(os.path.join(MEDIA_ROOT,"FASTA"))
    MEDIA_OPOOL = str(os.path.join(MEDIA_ROOT,"OPOOL")) 
    MEDIA_OLIGO = str(os.path.join(MEDIA_ROOT,"OLIGO"))
    MEDIA_TXT = str(os.path.join(MEDIA_ROOT,"REPORTS"))
    BLAST_ROOT = "blastn"

    if os.path.exists(MEDIA_ROOT):
        pass
    else:
        MEDIA_ROOT=os.mkdir(MEDIA_ROOT)
    if os.path.exists(MEDIA_FASTA):
        pass
    else:
        MEDIA_FASTA = os.mkdir(MEDIA_FASTA)
    if os.path.exists(MEDIA_OPOOL):
        pass
    else:
        MEDIA_OPOOL = os.mkdir(MEDIA_OPOOL)
    if os.path.exists(MEDIA_OLIGO):
        pass
    else:
        MEDIA_OLIGO = os.mkdir(MEDIA_OLIGO)
    if os.path.exists(MEDIA_TXT):
        pass
    else:
        MEDIA_TXT = os.mkdir(MEDIA_TXT)
    return([str(MEDIA_ROOT),str(BLAST_ROOT),str(MEDIA_FASTA),str(MEDIA_OPOOL),str(MEDIA_OLIGO),str(MEDIA_TXT)])
