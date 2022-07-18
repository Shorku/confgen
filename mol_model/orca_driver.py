import os
import subprocess


from mol_model.params import orca_xtb, orca_dft
from utils.utils import dump_temp_files


def orca_tmp_clear(data_dir, compress):
    extensions_del = ['.inp', '.txt', '.engrad', '.opt', '.xyz',
                      '.xtbrestart', '.densities', '.tmp', '.cube']
    extensions_dump = ['.out', '.gbw']

    for ext in extensions_dump:
        dump_temp_files(data_dir, ext, compress=compress)

    for ext in extensions_del:
        dump_temp_files(data_dir, ext, compress=False, remove=True)


def orca_gen(input_dir, job, jobs_files, thresh_keep, level, pal):
    qc_input_string = orca_xtb(pal) if level == 'semi' else orca_dft(pal)
    orca_path = f'''{os.environ['ORCA']}/orca'''
    e_dft = []
    for file in jobs_files:
        file_path = os.path.join(input_dir, file)
        with open(file_path, 'r') as xyz:
            xyz_block = ''.join(xyz.readlines()[2:])
            input_string = qc_input_string.format(xyz_block)

        orca_job_name = f'{os.path.splitext(file)[0]}.{level}'
        orca_inp = f'{orca_job_name}.inp'
        orca_out = f'{orca_job_name}.out'
        with open(orca_inp, 'w') as inp:
            inp.write(input_string)

        cli_opts = [orca_path, orca_inp]
        with open(orca_out, 'w') as out:
            subprocess.run(cli_opts, stdout=out)

        e_dft.append(0)
        # Check whether optimization is converged, otherwise assign big energy
        cli_opts = ['grep', 'ORCA TERMINATED NORMALLY', orca_out]  # TODO Fix!
        conv_flag = float(subprocess.run(cli_opts).returncode)
        conv_flag = 1.0 if conv_flag == 0.0 else 0.0
        with open(orca_out) as out:
            for j in out:
                if 'FINAL SINGLE POINT ENERGY' in j:
                    e_dft[-1] = float(j.split()[4]) * conv_flag

    e_dft_min = min(e_dft)
    conformers = []
    for file, e in zip(jobs_files, e_dft):
        orca_xyz_name = f'{os.path.splitext(file)[0]}.{level}.xyz'
        # 2625.5 is a conversion factor Hartree -> kJ/mol
        if (e - e_dft_min) * 2625.5 < thresh_keep:
            with open(orca_xyz_name, 'r') as xyz:
                conformers.append(xyz.read())
    compress = True if level == 'dft' else False
    orca_tmp_clear('.', compress)

    return conformers
