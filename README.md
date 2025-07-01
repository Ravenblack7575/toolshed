### 1) split_fasta.py

This little python script is for splitting fasta files downloaded from NCBI Genbank or Refseq containing multiple sequences into individual sequence files named by their accession numbers. The contents of the file would just contain the nucleotide sequence without the header. 

Example use: python3 split_fasta.py -i [pathtoinputfile]/file.fasta -o [pathtoutput]/outputdirectory
