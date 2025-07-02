from Bio import SeqIO
import re
import os
import argparse

def split_and_process_fasta(input_fasta_file, output_directory):
    """
    Splits a multi-sequence FASTA file into individual files,
    names them by accession number, and keeps the full FASTA format.

    Args:
        input_fasta_file (str): Path to the input FASTA file.
        output_directory (str): Directory to save the output files.
                                 Will be created if it doesn't exist.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created output directory: {output_directory}")

    processed_count = 0
    try:
        with open(input_fasta_file, "r") as infile:
            for record in SeqIO.parse(infile, "fasta"):
                # Extract accession number from the record ID
                match = re.search(r'([A-Z0-9_]+\.\d+)', record.id)
                if match:
                    accession_number = match.group(1)
                else:
                    print(f"Warning: Could not parse accession number from '{record.id}'. Using cleaned ID for filename.")
                    accession_number = record.id.split()[0].replace('|', '_').replace('>', '').replace(':', '_')

                # Define output filename
                output_filename = os.path.join(output_directory, f"{accession_number}.fasta")

                # Write the full SeqRecord object to the new file in FASTA format
                with open(output_filename, "w") as outfile:
                    SeqIO.write(record, outfile, "fasta")
                
                processed_count += 1

    except FileNotFoundError:
        print(f"Error: Input file '{input_fasta_file}' not found.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    print(f"\nProcessing complete. {processed_count} sequences processed.")
    print(f"Files saved in: {output_directory}")

# --- Command-line argument parsing (no change here) ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Split a multi-sequence FASTA file into individual files, "
                    "named by accession number, and keep the full FASTA format."
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to the input multi-sequence FASTA file."
    )
    parser.add_argument(
        "-o", "--output",
        default="single_sequence_files",
        help="Directory to save the individual sequence files. "
             "Default: 'single_sequence_files'"
    )

    args = parser.parse_args()
    split_and_process_fasta(args.input, args.output)