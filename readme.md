# [Özpolat lab at WUStL](https://bduyguozpolat.org/research)
[![DOI](https://zenodo.org/badge/265590174.svg)](https://zenodo.org/badge/latestdoi/265590174)


## Hybridization Chain Reaction in situ probe generator for the command line
*Generate HCR-3.0-style Probe Pairs for fluorescent* in situ *mRNA visualization*

### Intention of this program:

We were excited to venture into the realm of quick, easy, mutliplexable *in situ* hybridizations presented by the Hybridization Chain Reaction methodology (Choi et al. Development 2018) . We wanted a budget-friendly way of exploring gene expression that allowed for complete control over probe design, while allowing us to also know the exact sequences of our probes to aid publication and reproducibility. As a result, we wrote this program to allow us ease of ordering probes that mesh with the published HCR system of reaction and amplification reagents.

This current iteration has added features that enable users to:
  + Rapidly create probe sets for large libraries of mRNAs of interest with a single command
  + Create multiple versions of the same probe set for use with different amplifiers
  + Integrate the probe making tools into the user's own custom Python scripts
  + Change the amplifier of an already produced set of probes for a different amplifier
  + Make probe pairs compatible with the amplifier sets created by Choi et al. (2018), Wang et al. (2020), as well as the short-hairpin paradigm developed by Tsuneoka and Funato (2020).
  + Have properly formatted forms to order probe sets as 
    + A single tube of oligos pooled together for pilot studies (~10 reactions)
    + Individual oligos for routinely used probe sets (~5000 reactions)
  
### What you'll find here:
  + Python scripts compatible with Python versions 3.7 to 3.9

### What you will need to use this software:
  + [Python v3.7 - v3.9](https://www.python.org/downloads)
  + Python libraries
    + Biopython
    + Numpy
    + Openpyxl
    + Pandas
  ```
  pip install Bio numpy openpyxl pandas
  ```
  + [NCBI's BLAST+ local software suite](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/)
  + A reference transcriptome if intending to utilize BLAST
  + Your transcript(s) of interest in FASTA format

### Contact us
  If you have any questions please feel free to contact us. We love HCR and want to help you jump into it. 
  ```
  Ryan W Null        nullr [at] wustl.edu
  B Duygu Özpolat    bdozpolat [at] wustl.edu
  ```

## How to use the software from the command line

### 
  + ### Basic creation of a single probe set
    Required values include the amplifier desired, a name for the probe set, and the sense sequence of the mRNA.

    *Input*
    ```
    $ cd /location/of/the/downloaded/scripts
    $ python ./makeprobes.py -amp B1 -name YourFavGene -seq AAATTTCCGGGGCCCAGAGACGATGAGACCCGTTGCGATATGTTATGGCCGACCACA
    ```
    *Output*
    ```
    $ Amplifier Chosen: B1
    $ Name Chosen: YourFavGene
    $ The sequence given for probe production is: AAATTTCCGGGGCCCAGAGACGATGAGACCCGTTGCGATATGTTATGGCCGACCACA
    
    $ It looks like we found some probes. Check here .\ProbemakerOut\TXT\B1_YourFavGene_1_Delay0.txt to see the results.
    $ You can find an IDT opool submission form located here .\ProbemakerOut\OPOOL\B1_YourFavGene_1_Delay0oPool.xlsx.
    $ And you can find a bulk primer order here: .\ProbemakerOut\OLIGO\B1_YourFavGene_1_Delay0oligo.xlsx, this is a rare type of submission for generating a lifetime supply.
    ```
  + ### More advanced single probe set
    Optional arguments can be included by entering the appropriate flag and value.

    *Input*
    ```
    $ cd /location/of/the/downloaded/scripts
    $ python ./makeprobes.py -amp B1 -cg 30-70 -polyAT 5 -polyGC 3 -name YourFavGene -seq AAATTTCCGGGGCCCAGAGACGATGAGACCCGTTGCGATATGTTATGGCCGACCACA 
    ```
    *Output*
    ```
    $ Amplifier Chosen: B1
    $ Name Chosen: YourFavGene
    $ The sequence given for probe production is: AAATTTCCGGGGCCCAGAGACGATGAGACCCGTTGCGATATGTTATGGCCGACCACA
    $ Percent CG lower limit specified: 30 percent
    $ Percent CG upper limit specified: 70 percent
    $ AT homopolymer limit specified: 5
    $ GC homopolymer limit specified: 3
    
    $ It looks like we found some probes. Check here .\ProbemakerOut\TXT\B1_YourFavGene_1_Delay0.txt to see the results.
    $ You can find an IDT opool submission form located here .\ProbemakerOut\OPOOL\B1_YourFavGene_1_Delay0oPool.xlsx.
    $ And you can find a bulk primer order here: .\ProbemakerOut\OLIGO\B1_YourFavGene_1_Delay0oligo.xlsx, this is a rare type of submission for generating a lifetime supply.
    ```
  + ### Creation of identical probe sets with multiple amplifiers 
    Include the amplifiers as a single, comma-separated list.
    
    *Input*
    ```
    $ cd /location/of/the/downloaded/scripts
    $ python ./makeprobes.py -amp B1,B7,S41 -name YourFavGene -seq AAATTTCCGGGGCCCAGAGACGATGAGACCCGTTGCGATATGTTATGGCCGACCACA
    ```
    *Output*
    ```
    $ [B1,B7,S41]
    $ Name Chosen: YourFavGene
    $ The sequence given for probe production is: AAATTTCCGGGGCCCAGAGACGATGAGACCCGTTGCGATATGTTATGGCCGACCACA
    
    $ It looks like we found some probes. Check here .\ProbemakerOut\TXT\B1_YourFavGene_1_Delay0.txt to see the results.
    $ You can find an IDT opool submission form located here .\ProbemakerOut\OPOOL\B1_YourFavGene_1_Delay0oPool.xlsx.
    $ And you can find a bulk primer order here: .\ProbemakerOut\OLIGO\B1_YourFavGene_1_Delay0oligo.xlsx, this is a rare type of submission for generating a lifetime supply.
        
    $ It looks like we found some probes. Check here .\ProbemakerOut\TXT\B7_YourFavGene_1_Delay0.txt to see the results.
    $ You can find an IDT opool submission form located here .\ProbemakerOut\OPOOL\B7_YourFavGene_1_Delay0oPool.xlsx.
    $ And you can find a bulk primer order here: .\ProbemakerOut\OLIGO\B7_YourFavGene_1_Delay0oligo.xlsx, this is a rare type of submission for generating a lifetime supply.
        
    $ It looks like we found some probes. Check here .\ProbemakerOut\TXT\S41_YourFavGene_1_Delay0.txt to see the results.
    $ You can find an IDT opool submission form located here .\ProbemakerOut\OPOOL\S41_YourFavGene_1_Delay0oPool.xlsx.
    $ And you can find a bulk primer order here: .\ProbemakerOut\OLIGO\S41_YourFavGene_1_Delay0oligo.xlsx, this is a rare type of submission for generating a lifetime supply.
    ```
  + ### Making probe pairs from a large list of sequences
    When called, the "batch.py" program will take in a specified FASTA-formatted file and produce a probe pool for each one. To indicate where the FASTA file is, use the *-batch* flag followed by the file's location.

    When using this function you can provide a comma-separated list of the amplifiers you want to use. The program will start with the first listed and proceed through each of the sequences in the FASTA file. If your FASTA file has more sequences than the number of amplifiers specified, the algorithm will loop back to the beginning of the list.

    If for example the fasta file has 3 sequences:
    
    *fasta_file.fasta*

    >\>Sequence1\
      ATTCGGGAGT...\
    \>Sequence2\
      GCTTTGAACA...\
    \>Sequence3\
      CCTGAGCCTG...

    But we only want to use 2 amplifiers, B7 and S10, the program will produce the following probe pools:

    >B7-TargetGene1\
    S10-TargetGene2\
    B7-TargetGene3  

    It can be useful to also specify the max number of probe pairs you want the program to make by using the *-max* flag followed by an integer.

    For reference the maximum number of probe pairs in a single IDT oPool that can be ordered before incurring an additional per base charge is 36. 

    *Input*
    ```
    $ cd /location/of/the/downloaded/scripts

    $ python .\batch.py -amp b1,b2 -batch ./test.fa -max 36
    ```
  + ### Using BLASTn to flag potentially promiscuous probe pairs
    Though HCR with split initiators is less likely to generate background fluorescence, you may want to check for the potential of off-target binding during the probe design process. We have built in blastn functionality that flags probe pairs that have high coverage of multiple sequences within a fasta file. This function does not remove the sequences, it simply highlights them so that the user can investigate further and choose to remove if they want. Sequences are only flagged if both halves of the probe pair match a target sequence. Perfect alignment of a single half, will not result in flagging as it should not result in background fluorescence.

    The "-b" flag followed by a path to a transcriptome file will initiate a blast search.

    *Input*
    ```
    $ cd /location/of/the/downloaded/scripts
    $ python ./makeprobes.py -b ./path/to/reference/transcriptome.fa -name YourFavGene -amp B1 -seq AAATTTCCGGGGCCCAGAGACGATGAGACCCGTTGCGATATGTTATGGCCGACCACA
    ```
    *Output*
    ```
    $ Amplifier Chosen: B1
    $ Name Chosen: YourFavGene
    $ Transcriptome reference is: transcriptome.fa
    $ The sequence given for probe production is: AAATTTCCGGGGCCCAGAGACGATGAGACCCGTTGCGATATGTTATGGCCGACCACA
    
    $ It looks like we found some probes. Check here .\ProbemakerOut\TXT\B1_YourFavGene_1_Delay0.txt to see the results.
    $ You can find an IDT opool submission form located here .\ProbemakerOut\OPOOL\B1_YourFavGene_1_Delay0oPool.xlsx.
    $ And you can find a bulk primer order here: .\ProbemakerOut\OLIGO\B1_YourFavGene_1_Delay0oligo.xlsx, this is a rare type of submission for generating a lifetime supply.
    ```

## How to use the software in a custom Python script
  We have also created a Python library that can be used in your already existing pipelines. 
  
  #### hcr(amplifier, name, sequence, *kwargs)

  + "name", "amplifier", and "sequence" are required inputs  
  + "pause"   - tells the program to wait X number of 5' bases before creating probes
  + "polyAT"  - sets the upper threshold of homopolymeric runs for A and T
  + "polyCG"  - as above but for C and G
  + "numbr"   - limits the number of probe pairs produced, defaults to max possible. 36 probe pairs is the most a single opool can take before charging a per base surcharge.
  + "cgupper" - The upper limit of CG% for a probe pair
  + "cglower" - The lower limit of CG% for a probe pair
  + "txptome" - The file name of your reference transcriptome
  + "tpath"   - The path to where the transcriptome is on your drive
  ```
  import os
  os.chdir("/path/to/hcr/probe/maker/software")
  
  import hcr

  # Variables are created containing the required values \ 
    as strings and/or lists of strings.

  seq = "AAATTTCCGGGGCCCAGAGACGATGAGACCCGTTGCGATATGTTATGGCCGACCACA"
  amp = ["B1","S10"]
  name = "YFG"

  # This calls the function from the HCR Probe Maker module

  hcr.hcr(amp,name,seq)
  ```

## Citation
  If you use this program to create probe pairs, please cite this paper in your publication.

  ```
  Kuehn, E., Clausen, D. S., Null, R. W., Metzger, B. M., Willis, A. D., & Özpolat, B. D. (2022). 
  Segment number threshold determines juvenile onset of germline cluster expansion in Platynereis dumerilii. 
  Journal of Experimental Zoology Part B: Molecular and Developmental Evolution, 338, 225– 240. 
  ```
  Kindly, consider including the work that this was built upon as well.
  ```
  Choi HMT, Schwarzkopf M, Fornace ME, Acharya A, Artavanis G, Stegmaier J, Cunha A, Pierce NA. 
  Third-generation in situ hybridization chain reaction: multiplexed, quantitative, sensitive, versatile, robust. 
  Development. 2018 Jun 26;145(12):dev165753. doi: 10.1242/dev.165753. PMID: 29945988; PMCID: PMC6031405.
  ```
  ```
  Multiplexed in situ protein imaging using DNA-barcoded antibodies with extended hybridization chain reactions.
  Yu Wang, Yitian Zeng, Sinem K. Saka, Wenxin Xie, Isabel Goldaracena, Richie E. Kohman, Peng Yin, George M. Church
  bioRxiv 274456; doi: https://doi.org/10.1101/274456
  ```
  ```
  Tsuneoka Y, Funato H. 
  Modified in situ Hybridization Chain Reaction Using Short Hairpin DNAs. 
  Front Mol Neurosci. 2020 May 12;13:75. doi: 10.3389/fnmol.2020.00075. PMID: 32477063; PMCID: PMC7235299.
  ```

