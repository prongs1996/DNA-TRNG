# DNA-TRNG
True Random Number Generation using DNA Sequencing

DNA-TRNG is a true random number generator that generates a random bitstream as a free byproduct of every data retrieval operation in any DNA-based data storage system.

In this repository, we present the implementation of the TRNG proposed in BIOARXIV LINK [[1]](#1). 

Python 3 is required (we recommend 3.9 or newer)


To try out DNA-TRNG, clone this repository to a directory of your choice with the command:

```shell
$ git clone https://github.com/prongs1996/DNA-TRNG.git
```

To generate a random bitstream, you need to provide the read order/sequencing order of any read operation performed during a DNA-based data storage experiment. A sample ordering from our wetlab experiments [[1]](#1) is provided in the *data* directory.

The code to generate a random bitstream from the sequencing order is provided in the *bistream_generation* directory and our implementation of the Peres debiaser [[2]](#2) is provided in the *peres_debiasing* directory.

If you wish to run the pipeline discussed in our paper, use the command:

```shell
$ sh pipeline.sh
```

The truly random output bitstream would be available at */data/random_bitstream.txt*


## References
<a id="1">[1]</a> 
Our names. (2023). 
Our paper title. 
bioarxiv link to our paper.

<a id="2">[2]</a> 
Peres, Y. (1992).
Iterating von Neumann's procedure for extracting random bits.
The Annals of Statistics, 590-597.