"""ORCA input files templates"""


def orca_xtb(pal):
    """ Returns a template for an input file for geometry optimization using
    XTB

    Args:
        pal (int): the number of processes ORCA will use

    Return:
        (str): a string to be written in the input file
    """
    return f'''! XTB2 verytightopt
%pal nprocs {pal} end
*xyz 0 1
{{}}
*'''


def orca_dft(pal):
    """ Returns a template for an input file for geometry optimization using
    DFT

    Args:
        pal (int): the number of processes ORCA will use

    Return:
        (str): a string to be written in the input file
    """
    return f'''! RKS r2SCAN-3c tightscf tightopt
%pal nprocs {pal} end
*xyz 0 1
{{}}
*
'''
