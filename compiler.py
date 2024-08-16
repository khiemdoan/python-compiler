__author__ = 'Khiem Doan'
__github__ = 'https://github.com/khiemdoan'
__email__ = 'doankhiem.crazy@gmail.com'

from argparse import ArgumentParser
from pathlib import Path
from py_compile import compile
from shutil import copyfile


def compile_file(src_file: Path, dest_file: Path) -> None:
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        if src_file.suffix.lower() == '.py':
            print(f'{src_file} -> {dest_file}c')
            compile(src_file, f'{dest_file}c')
        else:
            print(f'{src_file} -> {dest_file}')
            copyfile(src_file, dest_file)
    except Exception:
        return


def main() -> None:
    """Script main program."""

    parser = ArgumentParser(description='Utilities to compile *.py to *.pyc.')
    parser.add_argument('src', type=str, help='source file or directory to compile')
    parser.add_argument('dest', type=str, help='destination file or directory')

    args = parser.parse_args()

    print(args)

    src_path = Path(args.src)
    dest_path = Path(args.dest)

    if src_path.is_file():
        dest_path = Path(args.dest)
        compile_file(src_path, dest_path)

    if src_path.is_dir():
        dest_path.mkdir(parents=True, exist_ok=True)
        for src_file_path in src_path.glob('**/*'):
            relative = src_file_path.relative_to(src_path)
            dest_file_path = dest_path / relative
            compile_file(src_file_path, dest_file_path)


if __name__ == '__main__':
    main()
