"""Command line argument parsing"""
import argparse
from munch import Munch

PARSER = argparse.ArgumentParser(description="ConfGen")

PARSER.add_argument('--mol_dir',
                    type=str,
                    default='/mol',
                    help="""input .mol structures directory""")

PARSER.add_argument('--out_dir',
                    type=str,
                    required=True,
                    help="""directory with output data""")

PARSER.add_argument('--pal',
                    type=int,
                    default=1,
                    help="""number of CPU cores to use in calculations""")

PARSER.add_argument('--conf_level',
                    choices=['ff', 'semi', 'dft', 'ff_dft'],
                    type=str,
                    default='dft',
                    help="""highest level of conf geometry optimization,
                    successively optimize at ff, xtb and dft levels by default.
                    For example xtb option will do ff and xtb optimizations.
                    ff-dft will omit xtb step.""")

PARSER.add_argument('--rdkit_thresh',
                    type=float,
                    default=0.1,
                    help="""conformers energy difference criteria""")

PARSER.add_argument('--rdkit_nconf',
                    type=int,
                    default=1000,
                    help="""max number of conformers rdkit will generate""")

PARSER.add_argument('--rdkit_thresh_keep',
                    type=float,
                    default=20,
                    help="""energy window to keep conformers within, kJ/mol""")

PARSER.add_argument('--orca_thresh_keep',
                    type=float,
                    default=5,
                    help="""energy window to keep conformers within, kJ/mol""")

PARSER.add_argument('--orca_path',
                    type=str,
                    help="""ORCA location, can also be taken from env""")

PARSER.add_argument('--conf_path',
                    type=str,
                    help="""CONFORMERS location, can also be taken from env""")


def parse_args(flags):
    return Munch({
        'mol_dir': flags.mol_dir,
        'out_dir': flags.out_dir,
        'pal': flags.pal,
        'conf_level': flags.conf_level,
        'rdkit_thresh': flags.rdkit_thresh,
        'rdkit_nconf': flags.rdkit_nconf,
        'rdkit_thresh_keep': flags.rdkit_thresh_keep,
        'orca_thresh_keep': flags.orca_thresh_keep,
        'orca_path': flags.orca_path,
        'conf_path': flags.conf_path
            })
