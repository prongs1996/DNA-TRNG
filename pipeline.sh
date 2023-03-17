#!/bin/sh
set -x

# ORDERING is the sequencing order that you want to use to generate the random bitstream
# By default, we provide the order in which we received reads in our wetlab experiment.
ORDERING='./data/read_order_alice.txt'

# SIDES is the number of faces of the dice.
SIDES='13'

# We first generate a random bitstream from the sequencing order
python3 ./bitstream_generation/bitstream_from_ordering.py --i $ORDERING --o ./peres_debiasing/to_be_debiased.txt --s $SIDES

# We use Peres debiasing to debias the generated bitstream
python3 ./peres_debiasing/peres.py --i ./peres_debiasing/to_be_debiased.txt --o ./data/random_bitstream.txt --s $SIDES
