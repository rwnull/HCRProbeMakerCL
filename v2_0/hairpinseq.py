def hairpins(hairpin):
    seqs = {
         "H1":{"B1":"CGTAAAGGAAGACTCTTCCCGTTTGCTGCCCTCCTCGCATTCTTTCTTGAGGAGGGCAGCAAACGGGAAGAG",
               "B2":"GGCGGTTTACTGGATGATTGATGAGGATTTACGAGGAGCTCAGTCCATCCTCGTAAATCCTCATCAATCATC",
               "B3":"CGGGTTAAAGTTGAGTGGAGATATAGAGGCAGGGACAAAGTCTAATCCGTCCCTGCCTCTATATCTCCACTC",
               "B4":"GAAGCGAATATGGTGAGAGTTGGAGGTAGGTTGAGGCACATTTACAGACCTCAACCTACCTCCAACTCTCAC",
               "B5":"ATTGGATTTGTAGGGTAGATAGAGATTGGGAGTGAGCACTTCATATCACTCACTCCCAATCTCTATCTACCC",
               "B7":"CCTACCTCCAATCCCTACCCTCACTACATCCTCACCGTGAGGGTAGGGATTGGAGGTAGGTGGAGGTTGAAG",
               "B9":"CCACTCTCAGCACACTCCCAACCCTACTACAAGCTCGGGTTGGGAGTGTGCTGAGAGTGGAGTAGATACGTG",
               "B10":"CCTCTACCTACTCGACTACCCTAGCCGTAACTTCACCTAGGGTAGTCGAGTAGGTAGAGGAGTATCTTGAGG",
               "B11":"ACTCCTACGTCGACCACACTCATCCTGCATGTTCCCGATGAGTGTGGTCGACGTAGGAGTGATATCTAAGCG",
               "B13":"CCTGCTTTATGCTCAACATACAACCAGAAATGCGGCGTTGTATGTTGAGCATAAAGCAGGAAGGCGTTACCT",
               "B14":"GAGCGACCCTATATTTCTGCACAGAAGTTATACCGGCTGTGCAGAAATATAGGGTCGCTCGCTATTGACATT",
               "B15":"CCACAAGGTATCTCGAACACTCTCCAAATTGGCTACGAGAGTGTTCGAGATACCTTGTGGTGTGTTAATCTG",
               "B17":"GTGGACACCTGCTAATCGGATGAGTGTTCGTTATCGCTCATCCGATTAGCAGGTGTCCACAACAAACAATCG",
               "S10":"ATCTAATGGGCTCATCCGACGATCACTTGACGTCGGATGAGC",
               "S23":"ATACGACTTCGACGACCACCCAACTTGAATGGGTGGTCGTCG",
               "S25":"TAGACTGAACCCACTCCGACGATCTGTCTTCGTCGGAGTGGG",
               "S34":"ATGGAAGATGCTCACCGACCGTTCATGCAACGGTCGGTGAGC",
               "S35":"AGTACATGTCGTGGTGGTAGCTTGTATGAAGCTACCACCACG",
               "S41":"TGTTGCAAAGGAACGTCGAGCTGTAATGGTGCTCGACGTTCC"},
         "H2":{"B1":"GAGGAGGGCAGCAAACGGGAAGAGTCTTCCTTTACGCTCTTCCCGTTTGCTGCCCTCCTCAAGAAAGAATGC",
               "B2":"CCTCGTAAATCCTCATCAATCATCCAGTAAACCGCCGATGATTGATGAGGATTTACGAGGATGGACTGAGCT",
               "B3":"GTCCCTGCCTCTATATCTCCACTCAACTTTAACCCGGAGTGGAGATATAGAGGCAGGGACGGATTAGACTTT",
               "B4":"CCTCAACCTACCTCCAACTCTCACCATATTCGCTTCGTGAGAGTTGGAGGTAGGTTGAGGTCTGTAAATGTG",
               "B5":"CTCACTCCCAATCTCTATCTACCCTACAAATCCAATGGGTAGATAGAGATTGGGAGTGAGTGATATGAAGTG",
               "B7":"GGTGAGGATGTAGTGAGGGTAGGGATTGGAGGTAGGCTTCAACCTCCACCTACCTCCAATCCCTACCCTCAC",
               "B9":"GAGCTTGTAGTAGGGTTGGGAGTGTGCTGAGAGTGGCACGTATCTACTCCACTCTCAGCACACTCCCAACCC",
               "B10":"GTGAAGTTACGGCTAGGGTAGTCGAGTAGGTAGAGGCCTCAAGATACTCCTCTACCTACTCGACTACCCTAG",
               "B11":"GGGAACATGCAGGATGAGTGTGGTCGACGTAGGAGTCGCTTAGATATCACTCCTACGTCGACCACACTCATC",
               "B13":"GCCGCATTTCTGGTTGTATGTTGAGCATAAAGCAGGAGGTAACGCCTTCCTGCTTTATGCTCAACATACAAC",
               "B14":"CCGGTATAACTTCTGTGCAGAAATATAGGGTCGCTCAATGTCAATAGCGAGCGACCCTATATTTCTGCACAG",
               "B15":"GTAGCCAATTTGGAGAGTGTTCGAGATACCTTGTGGCAGATTAACACACCACAAGGTATCTCGAACACTCTC",
               "B17":"CGATAACGAACACTCATCCGATTAGCAGGTGTCCACCGATTGTTTGTTGTGGACACCTGCTAATCGGATGAG",
               "S10":"CGTCGGATGAGCCCATTAGATGCTCATCCGACGTCAAGTGAT",
               "S23":"GGGTGGTCGTCGAAGTCGTATCGACGACCACCCATTCAAGTT",
               "S25":"CGTCGGAGTGGGTTCAGTCTACCCACTCCGACGAAGACAGAT",
               "S34":"CGGTCGGTGAGCATCTTCCATGCTCACCGACCGTTGCATGAA",
               "S35":"GCTACCACCACGACATGTACTCGTGGTGGTAGCTTCATACAA",
               "S41":"GCTCGACGTTCCTTTGCAACAGGAACGTCGAGCACCATTACA"}
        }

    return ([str(seqs["H1"][hairpin]),str(seqs["H2"][hairpin])])


hp = str(input("What is the number of the hairpins you want to retreive? ")).upper()

print("The sequences for "+hp+" in 5'-->3' orientation are:\n\r %s\n\r and\n\r %s." % (hairpins(hp)[0],hairpins(hp)[1]))