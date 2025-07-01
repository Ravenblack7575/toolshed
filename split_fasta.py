from Bio import SeqIO
import re
import os
import argparse # Import the argparse module

def split_and_process_fasta(input_fasta_file, output_directory): # Modified to accept arguments
    """
    Splits a multi-sequence FASTA file into individual files,
    names them by accession number, and removes the header.

    Args:
        input_fasta_file (str): Path to the input FASTA file.
        output_directory (str): Directory to save the output files.
                                 Will be created if it doesn't exist.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created output directory: {output_directory}")

    processed_count = 0
    try: # Add try-except for robust file handling
        with open(input_fasta_file, "r") as infile:
            for record in SeqIO.parse(infile, "fasta"):
                # Extract accession number from the record ID
                match = re.search(r'([A-Z0-9_]+\.\d+)', record.id) # Matches common accession.version like "AB123456.1"
                if match:
                    accession_number = match.group(1)
                else:
                    print(f"Warning: Could not parse accession number from '{record.id}'. Using cleaned ID for filename.")
                    accession_number = record.id.split()[0].replace('|', '_').replace('>', '').replace(':', '_') # More robust cleanup

                # Define output filename
                output_filename = os.path.join(output_directory, f"{accession_number}.fasta")

                # Write only the sequence to the new file
                with open(output_filename, "w") as outfile:
                    outfile.write(str(record.seq))

                processed_count += 1
    except FileNotFoundError:
        print(f"Error: Input file '{input_fasta_file}' not found.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    print(f"\nProcessing complete. {processed_count} sequences processed.")
    print(f"Files saved in: {output_directory}")

# --- Command-line argument parsing ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Split a multi-sequence FASTA file into individual files, "
                    "named by accession number, with headers removed."
    )
    parser.add_argument(
        "-i", "--input",
        required=True, # This makes the input file argument mandatory
        help="Path to the input multi-sequence FASTA file."
    )
    parser.add_argument(
        "-o", "--output",
        default="single_sequence_files", # Still provide a default, but allow override
        help="Directory to save the individual sequence files. "
             "Default: 'single_sequence_files'"
    )

    args = parser.parse_args()

    # Call the function with arguments from the command line
    split_and_process_fasta(args.input, args.output)