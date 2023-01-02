# [Ozpolat lab at WUStL](https://bduyguozpolat.org/research)
[![DOI](https://zenodo.org/badge/265590174.svg)](https://zenodo.org/badge/latestdoi/265590174)

Welcome!

## Hybridization Chain Reaction in situ probe generator for the command line
Generate HCR-3.0-style Probe Pairs for fluorescent *in situ* mRNA visualization

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
  From your terminal window type the following:
  ```
  pip install Bio numpy openpyxl pandas
  ```
  + [NCBI's BLAST+ local software suite](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/)
  + A reference transcriptome if intending to utilize BLAST
  + Your transcript(s) of interest in FASTA format
