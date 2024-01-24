#!/bin/sh
set -x

# INPUT_FILE is the fastq file of the sequencing run that we wish to generate random numbers from
# By default, we provide the INPUT_FILE illumina1.fastq from our wetlab experiment.
INPUT_FILE = 'SRR8073713.fastq'
OUTPUT_FILE = 'ExtractedBits.txt' # Name of the output file
BLOCK_SIZE = 10000 # Block Size for Blockwise Juels/Jakobsson
ALOGRITHM = 0 # Generation algorithm 0-6, 7 is for evaluation


# We generate a random bitstream from the fastq file
python3 DNA_Sequencing_TRNG.py --i $INPUT_FILE --o ./data/$OUTPUT_FILE --ALG $ALOGRITHM --b $BLOCK_SIZE