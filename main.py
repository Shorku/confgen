"""Entry point of automatic conformers generation application.

Example:
    python3 main.py --mol_dir <path> --out_dir <path> --conf_path <path>

"""


from runtime.arguments import PARSER, parse_args
from runtime.run import generate_conf
from runtime.setup import set_env, prepare_dir


def main():
    """
    Starting point of the application
    """
    params = parse_args(PARSER.parse_args())
    set_env(params)
    prepare_dir(params)
    generate_conf(params)


if __name__ == '__main__':
    main()
