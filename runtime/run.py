"""Implementation of conformers and densities generation functions"""

import os

from runtime.wrapers import generate_qc_conf
from runtime.wrapers import generate_ff_conf
from runtime.wrapers import remove_duplicates
from utils.utils import dump_temp_files


def generate_conf(params):
    """ Read molecular geometry from .mol files in params.mol_dir directory,
    generate multiple conformations, sequentially optimize them on different
    quantum chemical levels, filter by energy and remove duplicates

    Args:
        params (munch.Munch): Command line parameters

    Return:
        output_dir (str): directory path, where the final conformers geometries
                          are stored

    """

    # First stage: generate conformers using some generator, remove duplicates
    input_ff_dir = params.mol_dir
    output_ff_dir = os.path.join(params.out_dir, 'ff_geom')
    input_dir = input_ff_dir
    output_dir = output_ff_dir
    generate_ff_conf(input_dir, output_dir, params)
    remove_duplicates(output_dir)
    input_dir = output_dir
    # Second stage: optimize the conformers using cheap semi-empirical method,
    # filter by energy, remove duplicates, archive conformers from prev. step
    if 'semi' == params.conf_level or 'dft' == params.conf_level:
        output_dir = os.path.join(params.out_dir, 'semi_geom')
        generate_qc_conf(input_dir, output_dir, 'semi', params)
        remove_duplicates(output_dir)
        dump_temp_files(input_dir, '.xyz')
        input_dir = output_dir
    # Third stage: optimize the conformers using DFT, filter by energy, remove
    # duplicates, archive conformers from prev. step
    if 'dft' == params.conf_level or 'ff_dft' == params.conf_level:
        output_dir = os.path.join(params.out_dir, 'dft_geom')
        generate_qc_conf(input_dir, output_dir, 'dft', params)
        remove_duplicates(output_dir)
        dump_temp_files(input_dir, '.xyz')

    return output_dir
