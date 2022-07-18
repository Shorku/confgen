# confgen: generate and optimize conformers
 
This repository contains a script to generate a set of conformers of a molecule
using RDKit and optimize them using ORCA.  
  
## Contents
 
- [Overview](#overview)
- [Getting started](#quick-start-guide)
   * [Requirements](#requirements)
   * [Setup](#setup)
   * [Run](#run)

## Overview
 
The general workflow is pretty straightforward:

- Generate a set of conformers of a molecule using RDKit
- Remove duplicated conformers geometries using an external script
- Optimize conformers geometries with some semiempirical method using ORCA
- Remove the conformers outside a predefined energy window
- Remove duplicated conformers geometries using an external script
- Optimize conformers geometries with some DFT method using ORCA
- Remove the conformers outside a predefined energy window
- Remove duplicated conformers geometries using an external script

## Getting started

### Requirements
 
To run the script one will need:
- [ORCA](https://orcaforum.kofo.mpg.de/index.php) - An ab initio, DFT and 
semiempirical SCF-MO package
- [RDKit](https://www.rdkit.org/) - Open-Source Cheminformatics Software
- [XTB](https://xtb-docs.readthedocs.io/en/latest/contents.html) - 
Semiempirical Extended Tight-Binding Program Package
- [conformers](http://limor1.nioch.nsc.ru/quant/program/conformers/) - a 
standalone script for identical structures filtering
 
### Setup
 
1. Clone the repository.

   ```bash
   git clone https://github.com/Shorku/confgen
   cd confgen
   ```
 
2. Download and install prerequisites.
     
   ```
   this item is under construction
   ```
  
### Run

The script can consume multiple .mol files from the input directory. 
 
   **Basic:**
   
   ```bash
   python3 main.py --pal <ncores> --mol_dir <input_path> --out_dir <output_path> --conf_path <conf_path>
   ```
   `<ncores>` number of CPU cores to use in geometry optimizations

   `<input_path>` a directory where the script will look for input .mol files 

   `<output_path>` a directory where temporary files and the results will be
stored

   `<conf_path>` a directory where `conformers` script is stored. Can also be
defined in `CONFORMERS` environment variable

   **Other options:**

To see the full list of available options and their descriptions, use the `-h` or `--help` command-line option, for example:
```bash
python main.py --help
```
 
The following example output is printed:
```
usage: main.py [-h] 
               [--mol_dir MOL_DIR] --out_dir OUT_DIR [--pal PAL] 
               [--conf_level {ff,semi,dft,ff_dft}] [--rdkit_thresh RDKIT_THRESH] 
               [--rdkit_nconf RDKIT_NCONF] [--rdkit_thresh_keep RDKIT_THRESH_KEEP] 
               [--orca_thresh_keep ORCA_THRESH_KEEP] [--orca_path ORCA_PATH] 
               [--conf_path CONF_PATH]

confgen

optional arguments:
  -h, --help            show this help message and exit
  --mol_dir MOL_DIR     input .mol or .xyz structures directory
  --out_dir OUT_DIR     directory with output data
  --pal PAL             number of CPU cores to use in calculations
  --conf_level {ff,semi,dft,ff_dft}
                        highest level of conf geometry optimization, 
                        successively optimize at ff, xtb and dft levels by 
                        default. For example xtb option will do ff and
                        xtb optimizations. ff-dft will omit xtb step.
  --rdkit_thresh RDKIT_THRESH
                        conformers energy difference criteria
  --rdkit_nconf RDKIT_NCONF
                        max number of conformers rdkit will generate
  --rdkit_thresh_keep RDKIT_THRESH_KEEP
                        energy window to keep conformers within, kJ/mol
  --orca_thresh_keep ORCA_THRESH_KEEP
                        energy window to keep conformers within, kJ/mol
  --orca_path ORCA_PATH
                        ORCA location, it can also be taken from env
  --conf_path CONF_PATH
                        CONFORMERS location, it can also be taken from env
```

## TODO

- Add RDKit Docker
- Prerequisites setup guide
- RDKit defaults adjustment (so far it keeps warping phenyls)
- get into RDKit duplicate filtering
- logging
