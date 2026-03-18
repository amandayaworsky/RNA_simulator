# RNA Sequence Simulator

## Description
This project generates synthetic RNA sequences in FASTA format. Each sequence contains a simulated ORF that may be complete or partial, with optional flanking non-coding regions. Output headers include metadata such as sequence length, GC content, ambiguity content, ORF type, and flanking status.

## Features
- Generates complete and partial ORFs
- Adds optional 5' and 3' flanking regions
- Writes valid FASTA output
- Reports metadata in FASTA headers
- Uses a modular design with reusable library functions
- Includes type hints, docstrings, argparse, and conda environment support

## Requirements
- Python 3.11 or later
- Conda (Anaconda or Miniconda)
- Git
- Packages: Biopython, NumPy

## Installation
```bash
git clone https://github.com/yourusername/rna-simulator.git
cd rna-simulator
conda env create -f environment.yml
conda activate rna-simulator
python src/main.py --help
```

## Usage
Default run:
```bash
python src/main.py
```

Example 1:
```bash
python src/main.py -n 5 -o examples/example_output.fasta
```

Example 2:
```bash
python src/main.py -n 50 -o my_seqs.fasta --min-length 198 --max-length 600
```

Example 3:
```bash
python src/main.py -n 12 --flanking-prob 0.8 --flanking-length 30 --completeness 0.4
```

## Command-Line Arguments
- `-n`, `--num-sequences`: Number of sequences to generate. Default: `10`
- `-o`, `--output`: Output FASTA path. Default: `sequences.fasta`
- `--min-length`: Minimum ORF length in nucleotides. Default: `99`
- `--max-length`: Maximum ORF length in nucleotides. Default: `999`
- `--flanking-prob`: Probability of adding flanking regions. Default: `0.5`
- `--flanking-length`: Length of each flank. Default: `50`
- `--completeness`: Ratio of complete ORFs. Default: `0.7`

## Output Format
Each FASTA header includes metadata:
```text
>seq_001 length=186 gc_content=47.31 ambiguity=0.0 type=complete flanked=yes
AUGGCU...
```

## Project Structure
```text
rna-simulator/
├── README.md
├── LICENSE
├── pseudocode.txt
├── environment.yml
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── simulator.py
│   └── sequence_lib.py
└── examples/
    ├── example_output.fasta
    └── example_run.txt
```

## Algorithm Description
1. Parse command-line arguments.
2. Validate numeric ranges and probabilities.
3. For each record, randomly decide whether the ORF is complete or partial.
4. Generate the ORF sequence within the requested length range.
5. Randomly add left and right flanking regions based on probability.
6. Calculate metadata including length, GC content, ambiguity content, type, and flanked status.
7. Write records to a FASTA file.

## Metadata Calculations
- **GC content**: percentage of `G` and `C` nucleotides over total sequence length.
- **Ambiguity content**: percentage of IUPAC ambiguity codes in the sequence.

## References
- Biopython documentation
- FASTA format documentation
- IUPAC ambiguity code reference
- Open reading frame overview

## License
This project uses the MIT License.

## Author
AmandaYaworsky
