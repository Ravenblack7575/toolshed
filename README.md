### 1) split_fasta.py

This little python script is for splitting fasta files downloaded from NCBI Genbank or Refseq containing multiple sequences into individual sequence files named by their accession numbers. The contents of the file would just contain the nucleotide sequence without the header. 

Example use: python3 split_fasta.py -i [pathtoinputfile]/file.fasta -o [pathtoutput]/outputdirectory

### 2) split_fasta_keepheaders.py

Similar to the above, this python script is splits fasta files containing multiple sequences into individual sequence files named by their accession numbers. However, this one preserves the fasta format of the contents, that is it contains accession numbers, description and '>'.

Example use: python3 split_fasta_keepheaders.py -i [pathtoinputfile]/file.fasta -o [pathtoutput]/outputdirectory


### 3) googlemapcoord_from_jpeg_exif.py
It takes a jpeg image with exif GPS data and extracts the GPS data to convert it to Google Map coordinates. 

Example use: python googlemapcoord_from_jpeg.py [pathtoinputfile]/file.jpeg
