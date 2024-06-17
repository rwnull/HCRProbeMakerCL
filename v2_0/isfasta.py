import os
from Bio import SeqIO as fa

#subfunction to determine if a file is a fasta file
## Stolen from stackoverflow https://stackoverflow.com/questions/44293407/how-can-i-check-whether-a-given-file-is-fasta

def is_fasta(filename): 
    with open(filename, "r") as handle: #os.path.abspath
        fasta = list(fa.parse(handle, "fasta"))
        #print("fasta = ",fasta)
        #print("len(list(fasta))",len(list(fasta)))
        if len(fasta) > 0:
            print(filename," is a fasta file.")
            handle.close()
            return(True)  # False when `fasta` is empty, i.e. wasn't a FASTA file
        else:
            handle.close()
            return(None)

#'''def is_fasta(path,filename): 
#    with open(os.path.join(path,filename), "r") as handle:
#        fasta = fa.parse(handle, "fasta")
#        if any(fasta):
#            for entry in fasta:
#                print("entryid = ",str(entry.id))
#            print(filename," is a fasta file.")
#            return any(fasta)  # False when `fasta` is empty, i.e. wasn't a FASTA file
#        else:
#            return(None)'''