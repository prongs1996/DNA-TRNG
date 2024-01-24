# DNA-TRNG: True Random Number Generation as Byproduct of DNA/RNA Sequencing

DNA-TRNG is a true random number generator that generates a random bitstream as a free byproduct of any DNA/RNA sequencing run.

In this repository, we present the implementation of the TRNG proposed in True Random Numbers as Byproduct of DNA/RNA Sequencing [[1]](#1). 

Python 3 is required (we recommend 3.9 or newer)


To try out DNA-TRNG, clone this repository to a directory of your choice with the command:

```shell
$ git clone https://github.com/prongs1996/DNA-TRNG.git
```

To generate a random bitstream, you need to provide the fastq file of any DNA sequencing run. A sample fastq file from our wetlab experiments [[1]](#1) is provided in the *data* directory.

To extract random bits, use the command:
```shell
$ python3 DNA_Sequencing_TRNG.py --i $input_file --o $output_file --ALG $algorithm_number --b $block_size_for_JuelsJakobsson_algorithm
```
**Algortihm Number and Implemented Algorithms**: <br>
        0 - *Juels/Jakobsson* <br>
        1 - *Blockwise Juels/Jakobsson* <br>
        2 - *nCr Extractor* <br>
        3 - *Shrinking Window* <br>
        4 - *Halfbit* <br>
        5 - *Column-wise Peres* <br>
        6 - *Column-wise VNC* <br>
        7 - *Compare Extraction Rates for these 7 Algorithms* <br>


If you wish to observe a sample run of the example discussed in our paper [[1]](#1), use the command:

```shell
$ sh pipeline.sh
```

The truly random output bitstream would be available at */data/ExtractedBits.txt*


## References
<a id="1">[1]</a> 
Puru Sharma, Gary Goh Yipeng, Cheng-Kai Lim, and Djordje Jevdjic. (2024). 
True Random Numbers as Byproduct of DNA/RNA Sequencing. 
bioarxiv link to our paper.
