"""
Implementation of the interfaces between package-specific functions from
mol_model module and general workflow from run.py module
"""

import os
import tarfile


from datetime import datetime


from mol_model.rdkit_driver import rdkit_gen
from mol_model.conformers_driver import conformers_filter
from mol_model.orca_driver import orca_gen
from utils.utils import sort_xyz_into_jobs, write_conf_from_list


def generate_qc_conf(input_dir, output_dir, level, params):
    """ Sort conformers geometries from .xyz files in input_dir according to
    the chemical compound they belong to, optimize on the requested level of
    theory, filter by energy and write optimized and filtered geometries to
    output_dir

    Args:
        input_dir (str): directory path, contains .xyz files to be optimized
        output_dir (str): directory path, directory to write optimized
                          geometries in
        level (str): level of theory to optimize geometries, can be 'semi' or
                     'dft'
        params (munch.Munch): Command line parameters

    Return:
        None

    """
    job_names = sort_xyz_into_jobs(input_dir)
    thresh_keep = params.orca_thresh_keep
    pal = params.pal
    for job, jobs_files in job_names.items():
        conformers = orca_gen(input_dir, job, jobs_files,
                              thresh_keep, level, pal)
        write_conf_from_list(job, conformers, output_dir)


def generate_ff_conf(input_dir, output_dir, params):
    """ For every compound in .mol files in the input_dir directory generate
    a set of conformers using RDKit module and write every conformer into .xyz
    file in the output_dir directory

    Args:
        input_dir (str): directory path, contains .mol files with individual
                         compounds
        output_dir (str): directory path, directory to write a set of
                          geometries (.xyz files) of the conformers
        params (munch.Munch): Command line parameters

    Return:
        None

    """
    for infile in os.listdir(input_dir):
        if infile.endswith('.mol'):
            job_name = os.path.splitext(infile)[0]
            infile_path = os.path.join(input_dir, infile)
            thresh = params.rdkit_thresh
            thresh_keep = params.rdkit_thresh_keep
            nconf = params.rdkit_nconf

            conformers = rdkit_gen(infile_path, thresh, nconf, thresh_keep)
            write_conf_from_list(job_name, conformers, output_dir)


def remove_duplicates(data_dir):
    """ Sort conformers geometries from .xyz files in data_dir directory
    according to the chemical compound they belong to, write them into a single
    .xyz-file and invoke external conformers script to remove duplicates i.e.
    identical geometries. The non-filtered geometries are archived.

    Args:
        data_dir (str): directory path, contains .xyz files to be filtered

    Return:
        None

    """
    cwd = os.getcwd()
    os.chdir(data_dir)
    label = os.path.split(data_dir)[1]
    job_names = sort_xyz_into_jobs('.')
    now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    for job, jobs_files in job_names.items():
        all_xyz_file = f'{job}.xyz'
        all_xyz_tar = f'{job}_nonfiltered_{label}_{now}.tar.xz'
        with open(all_xyz_file, 'w') as xyz:
            for file in jobs_files:
                file_stream = open(file, 'r')
                xyz.write(file_stream.read())
                file_stream.close()
                os.remove(file)

        conformers = conformers_filter(all_xyz_file)
        write_conf_from_list(job, conformers, '.')

        with tarfile.open(all_xyz_tar, 'w:xz') as tar:
            tar.add(all_xyz_file)
        os.remove(all_xyz_file)

    os.chdir(cwd)
