import sys

def amp(ampl): 
    sys.tracebacklimit=0
    if ampl == "B1":
        upspc= "AA"
        dnspc= "TA"
        up = "GAGGAGGGCAGCAAACGG"
        dn = "GAAGAGTCTTCCTTTACG"
    elif ampl == "B2":
        upspc= "AA"
        dnspc= "AA"
        up = "CCTCGTAAATCCTCATCA"
        dn = "ATCATCCAGTAAACCGCC"
    elif ampl == "B3":
        upspc= "TT"
        dnspc= "TT"
        up = "GTCCCTGCCTCTATATCT"
        dn = "CCACTCAACTTTAACCCG"
    elif ampl == "B4":
        upspc= "AA"
        dnspc= "AT"
        up = "CCTCAACCTACCTCCAAC"
        dn = "TCTCACCATATTCGCTTC"
    elif ampl == "B5":
        upspc= "AA"
        dnspc= "AA"
        up = "CTCACTCCCAATCTCTAT"
        dn = "CTACCCTACAAATCCAAT"
    elif ampl == "B7":
        upspc= "AA" #Spacers were not specified so weak bases chosen; AA being common to the most.
        dnspc= "AA" #Spacers were not specified so weak bases chosen; AA being common to the most.
        up = "CTTCAACCTCCACCTACC"
        dn = "TCCAATCCCTACCCTCAC"
    elif ampl == "B9":
        upspc= "AA" #Spacers were not specified so weak bases chosen; AA being common to the most.
        dnspc= "AA" #Spacers were not specified so weak bases chosen; AA being common to the most.
        up = "CACGTATCTACTCCACTC"
        dn = "TCAGCACACTCCCAACCC"
    elif ampl == "B10":
        upspc= "AA" #Spacers were not specified so weak bases chosen; AA being common to the most.
        dnspc= "AA" #Spacers were not specified so weak bases chosen; AA being common to the most.
        up = "CCTCAAGATACTCCTCTA"
        dn = "CCTACTCGACTACCCTAG"
    elif ampl == "B11":
        upspc= "AA" #Spacers were not specified so weak bases chosen; AA being common to the most.
        dnspc= "AA" #Spacers were not specified so weak bases chosen; AA being common to the most.
        up = "CGCTTAGATATCACTCCT"
        dn = "ACGTCGACCACACTCATC"
    elif ampl == "B13":
        upspc= "AA" #Spacers were not specified so weak bases chosen; AA being common to the most.
        dnspc= "AA" #Spacers were not specified so weak bases chosen; AA being common to the most.
        up = "AGGTAACGCCTTCCTGCT"
        dn = "TTATGCTCAACATACAAC"
    elif ampl == "B14":
        upspc= "AA" #Spacers were not specified so weak bases chosen; AA being common to the most.
        dnspc= "AA" #Spacers were not specified so weak bases chosen; AA being common to the most.
        up = "AATGTCAATAGCGAGCGA"
        dn = "CCCTATATTTCTGCACAG"
    elif ampl == "B15":
        upspc= "AA" #Spacers were not specified so weak bases chosen; AA being common to the most.
        dnspc= "AA" #Spacers were not specified so weak bases chosen; AA being common to the most.
        up = "CAGATTAACACACCACAA"
        dn = "GGTATCTCGAACACTCTC"
    elif ampl == "B17":
        upspc= "AA" #Spacers were not specified so weak bases chosen; AA being common to the most.
        dnspc= "AA" #Spacers were not specified so weak bases chosen; AA being common to the most.
        up = "CGATTGTTTGTTGTGGAC"
        dn = "GCATGCTAATCGGATGAG"
    elif ampl == "S10":
        upspc= "AA"
        dnspc= "AA"
        up = "AGCCCATTAGAT"
        dn = "CGTCGGATG"
    elif ampl == "S23":
        upspc= "AA"
        dnspc= "AA"
        up = "TCGAAGTCGTAT"
        dn = "GGGTGGTCG"
    elif ampl == "S25":
        upspc= "AA"
        dnspc= "AA"
        up = "GGGTTCAGTCTA"
        dn = "CGTCGGAGT"
    elif ampl == "S34":
        upspc= "AA"
        dnspc= "AA"
        up = "AGCATCTTCCAT"
        dn = "CGGTCGGTG"
    elif ampl == "S35":
        upspc= "AA"
        dnspc= "AA"
        up = "ACGACATGTACT"
        dn = "GCTACCACC"
    elif ampl == "S41":
        upspc= "AA"
        dnspc= "AA"
        up = "TCCTTTGCAACA"
        dn = "GCTCGACGT"            
    else:
        print ("Please try again")
    return([upspc,dnspc,up,dn])