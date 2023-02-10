
from pathlib import Path
import os
import py_compile


def compile_file(source_file: Path, delete=False) -> bool:
    target_file = str(source_file) + 'c'
    try:
        ok = py_compile.compile(source_file, target_file)
        if delete:
            source_file.unlink()
    except py_compile.PyCompileError as err:
        print(f'*** Error compiling {source_file}...')
        # escape non-printable characters in msg
        encoding = sys.stdout.encoding or sys.getdefaultencoding()
        msg = err.msg.encode(encoding, errors='backslashreplace').decode(encoding)
        print(msg)
        return False
    except (SyntaxError, UnicodeError, OSError) as e:
        print(f'*** Error compiling {source_file}...')
        print(e.__class__.__name__ + ':', e)
        return False
    else:
        return ok != 0



def main():
    import argparse
    """Script main program."""

    parser = argparse.ArgumentParser(description='Utilities to compile *.py to *.pyc.')
    parser.add_argument('-d', '--delete', action='store_true', dest='delete', default=False, help='delete source files')
    parser.add_argument('compile_dests', metavar='FILE|DIR', nargs='*', help='file or directory names to compile')

    args = parser.parse_args()

    source_files = []

    for dest in args.compile_dests:
        dest = Path(dest)
        if dest.is_file():
            source_files.append(dest)
        if dest.is_dir():
            source_files += list(dest.glob('**/*.py'))

    for file in source_files:
        compile_file(file, delete=args.delete)

    return True


if __name__ == '__main__':
    import sys
    exit_status = int(not main())
    sys.exit(exit_status)
