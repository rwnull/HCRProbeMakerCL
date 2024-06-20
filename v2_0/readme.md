# [Özpolat lab at WUStL](https://bduyguozpolat.org/research)
[Cite us!](https://doi.org/10.1002/jez.b.23100)

## Hybridization Chain Reaction in situ probe generator for the command line version 2.0
*Generate HCR-3.0-style Probe Pairs for fluorescent* in situ *mRNA visualization*

### Intention of this program:

We were excited to venture into the realm of quick, easy, mutliplexable *in situ* hybridizations presented by the Hybridization Chain Reaction methodology (Choi et al. Development 2018) . We wanted a budget-friendly way of exploring gene expression that allowed for complete control over probe design, while allowing us to also know the exact sequences of our probes to aid publication and reproducibility. As a result, we wrote this program to allow us ease of ordering probes that mesh with the published HCR system of reaction and amplification reagents.

This current iteration has added features that enable users to:
  + Rapidly create probe sets for large libraries of mRNAs of interest with a single command
  + Create multiple versions of the same probe set for use with different amplifiers
  + Change the amplifier of an already produced set of probes for a different amplifier
  + Make probe pairs compatible with the amplifier sets created by Choi et al. (2018), Wang et al. (2020), as well as the short-hairpin paradigm developed by Tsuneoka and Funato (2020).
  + Have properly formatted forms to order probe sets as 
    + A single tube of oligos pooled together for pilot studies (~10 reactions)
    + Individual oligos for routinely used probe sets (~5000 reactions)
  
### What you'll find here:
  + Python scripts compatible with Python versions 3.7 to 3.12

### What you will need to use this software:
  + [Python v3.7 - v3.12](https://www.python.org/downloads)
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
    $ python ./HCR.py -amp B1 -in ./YourFavGene.fasta
    ```
    *Output*
    ```
    $ Amplifier Chosen: B1
        
    $ It looks like we found some probes. Check here.\ProbemakerOut\TXT\B1_YourFavGene_1_Delay0.txt to see the results.
    $ You can find an IDT opool submission form located here .\ProbemakerOut\OPOOL\B1_YourFavGene_1_Delay0oPool.xlsx.
    $ And you can find a bulk primer order here: .\ProbemakerOut\OLIGO\B1_YourFavGene_1_Delay0oligo.xlsx, this is a rare type of submission for generating a lifetime supply.
    ```
  + ### More advanced single probe set
    Optional arguments can be included by entering the appropriate flag and value.

    *Input*
    ```
    $ cd /location/of/the/downloaded/scripts
    $ python ./HCR.py -amp B1 -cg 20-70 -polyAT 5 -polyGC 3 -in YourFavGene.fasta -max 37 -min 10
    ```
    *Output*
    ```
    $ Amplifier(s) Chosen: B1
    $ Percent CG lower limit specified: 20 percent
    $ Percent CG upper limit specified: 70 percent
    $ AT homopolymer limit specified: 5
    $ GC homopolymer limit specified: 3
    $ The maximum number of probe pairs made will be 37.
    $ Transcripts with fewer than 538 base pairs made will be ignored because a lower limit of 10 probe pairs was requested.
    
    $ It looks like we found some probes. Check here .\ProbemakerOut\TXT\B1_YourFavGene_1_Delay0.txt to see the results.
    $ You can find an IDT opool submission form located here .\ProbemakerOut\OPOOL\B1_YourFavGene_1_Delay0oPool.xlsx.
    $ And you can find a bulk primer order here: .\ProbemakerOut\OLIGO\B1_YourFavGene_1_Delay0oligo.xlsx, this is a rare type of submission for generating a lifetime supply.
    ```
  + ### Making probe pairs from a large list of sequences
    When a fasta file with more than one sequence is uploaded, program will produce a probe pool for each one. To indicate where the FASTA file is, use the *-in* flag followed by the file's location.

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

    When working with large sets of data, you may want to filter against sequences that have a small number of potential probe pairs. In this instance, use the  *-min* flag followed by the lower limit of probe pairs you would prefer.

    >*Keep in mind that this lower limit is for potential probe pairs, if you have added other parameters you may find that the final output of probe pairs is less than the limit you've specified.*

    Due to how the program is currently written, the blast feature may be time/resource prohibitive when used with large batch files. Use with care.

    *Input*
    ```
    $ cd /location/of/the/downloaded/scripts

    $ python ./HCR.py -amp b1,b2 -in ./test.fa -min 20 -max 36 -min 10 -polyAT 4 -polyGC 3 -GC 20-65
    ```
  + ### Using BLASTn to flag potentially promiscuous probe pairs
    Though HCR with split initiators is less likely to generate background fluorescence, you may want to check for the potential of off-target binding during the probe design process. We have built in blastn functionality that flags probe pairs that have high coverage of multiple sequences within a fasta file. This function does not remove the sequences, it simply highlights them so that the user can investigate further and choose to remove if they want. Sequences are only flagged if both halves of the probe pair match a target sequence. Perfect alignment of a single half, will not result in flagging as it should not result in background fluorescence. If a probe pair matches a sequence perfectly across the full length of the pair, and the match belongs to a sequence with a different identifier to the input sequence, a flag "! -->" is applied to the probe pair number. It may be that this is a duplicate sequence, an isoform, a paralog, or something else. We leave this to you to intuit whether or not to keep this sequence in the probe submission.

    The "-blast" flag followed by a path to a transcriptome file will initiate a blast search.

    *Input*
    ```
    $ cd /location/of/the/downloaded/scripts
    $ python ./HCR.py -blast ./path/to/reference/transcriptome.fa -in ./YourFavGene.fasta -amp B1 
    ```
    *Output*
    ```
    $ Amplifier Chosen: B1
    $ Transcriptome reference: transcriptome.fa, located in the directory ./path/to/reference
    $ 
    
    $ It looks like we found some probes. Check here ./ProbemakerOut/REPORTS/B1_YourFavGene_1_Delay0.txt to see the results.
    $ You can find an IDT opool submission form located here ./ProbemakerOut/OPOOL/B1_YourFavGene_1_Delay0oPool.xlsx.
    $ And you can find a bulk primer order here: ./ProbemakerOut/OLIGO/B1_YourFavGene_1_Delay0oligo.xlsx, this is a rare type of submission for generating a lifetime supply.
    ```
+ ### Using ampswap to replace the amplifier initiator on one probe oligo pool with another.
    In the course of your experimentation you may wish to remake an oligo pool with a different initiator. To ensure you are maintaining all of the hybridization sequences constant without needing to perfectly recreate the original's inputs, running ampswap.py takes an input opool.xlsx, the current amplifier, and the new desired initiator, and then outputs the order forms required for your order.

  *Input*
  ```
  $ cd /location/of/the/downloaded/scripts
  $ python ./ampswap.py -in ./B1_yourfavgene_36_Delay0opool.xlsx -old B1 -new B2,B3,B4
  ```
  *Output*
  ```
  $ Your new oligos and opool can be found in this directory: /location/of/the/downloaded/scripts/HCRProbeMakerCL/v2_0/ProbemakerOut/OPOOL/AmplifierSwap
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

