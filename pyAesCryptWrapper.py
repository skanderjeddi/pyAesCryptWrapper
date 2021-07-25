'''
MIT License
Copyright (c) 2021 Skander Jeddi
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import pyAesCrypt as pac
import os
import sys
import uuid
from pathlib import Path
from timeit import default_timer as timer
from pyArgs import parse_args

'''
pyAesCrypt is a Python 3 file-encryption module and script that uses AES256-CBC to encrypt/decrypt files and binary streams.
PyPI page: https://pypi.org/project/pyAesCrypt/
GitHub page: https://github.com/marcobellaccini/pyAesCrypt
'''

# TODO: ADD DOCUMENTATION

VERSION = 1.0
VALID_EXTENSIONS = ['*']
KEEP_NAME = True
SILENT_SKIP = False


def gen_params():
    args_map = parse_args(sys.argv, positionals = [ 'mode', 'key', 'path' ], optionals_valueless = [ ('recursive', 'R'), ('silent', 's') ], script_name = 'pyAesCryptWrapper.py', from_sys_argv = True)
    positionals, optionals, optionals_valueless = args_map['positionals'], args_map['optionals'], args_map['optionals_valueless']
    mode, key, path = positionals['mode'], positionals['key'], positionals['path']
    recur, silent = 'recursive' in optionals_valueless, 'silent' in optionals_valueless
    return mode, key, path, recur, silent


def process_file(filepath, mode, key, silent):
    path_object = Path(filepath)
    parent_dir = path_object.parent.absolute()
    if os.getcwd() is not parent_dir:
        os.chdir(parent_dir)
    file_name = path_object.name
    file_ext = file_name.split('.')[-1].lower()
    if file_ext in VALID_EXTENSIONS or '*' in VALID_EXTENSIONS:
        try:
            time_elapsed = 0
            file_uuid = str(uuid.uuid4()) + '.' + file_ext
            if mode == 'encrypt':
                start = timer()
                pac.encryptFile(file_name, file_uuid, key)
                end = timer()
                time_elapsed = end - start
                os.remove(file_name)
                if KEEP_NAME:
                    os.rename(file_uuid, file_name)
            elif mode == 'decrypt':
                start = timer()
                pac.decryptFile(file_name, file_uuid, key)
                end = timer()
                time_elapsed = end - start
                os.remove(file_name)
                if KEEP_NAME:
                    os.rename(file_uuid, file_name)
            if not silent:
                if KEEP_NAME:
                    print(f'\t\t{file_name} -> {file_name} (in {time_elapsed}s)')
                else:
                    print(f'\t\t{file_name} -> {file_uuid} (in {time_elapsed}s)')
            return time_elapsed
        except ValueError as value_error:
            print(f'An error occurred while processing {file_name}: {value_error}')
            exit(-1)
    else:
        if not SILENT_SKIP:
            print(f'\tSkipping file {file_name} with extension {file_ext}')


def process_dir(dirpath, mode, key, recur, silent, files_processed = 0, parent_dir = None):
    total_files = 0
    dirname = Path(dirpath).name
    if not silent:
        if parent_dir:
            print(f'\tProcessing directory {parent_dir}/{dirname}...')
        else:
            print(f'\tProcessing directory {dirname}...')
    os.chdir(dirpath)
    children = os.listdir('.')
    files_to_process, dirs_to_process = [], []
    total_time_elapsed = 0
    for child in children:
        if not os.path.isdir(child):
            path_object = Path(child)
            file_name = path_object.name
            file_ext = file_name.split('.')[-1].lower()
            if file_ext in VALID_EXTENSIONS or '*' in VALID_EXTENSIONS:
                files_to_process.append(child)
            else:
                if not SILENT_SKIP:
                    print(f'\tSkipping file {file_name} with extension {file_ext}')
        else:
            dirs_to_process.append(child)
    for fp in files_to_process:
        total_time_elapsed += process_file(fp, mode, key)
        total_files += 1
    if recur:
        for sub_dir in dirs_to_process:
            sub_time_elapsed, sub_dir_files = process_dir(sub_dir, mode, key, parent_dir = (parent_dir + "/" + Path(dirpath).name if parent_dir is not None else Path(dirpath).name), files_processed = total_files)
            total_time_elapsed += sub_time_elapsed
            total_files += sub_dir_files
    return (total_time_elapsed, total_files)


def main():
    mode, key, path, recur, silent = gen_params()
    if not silent:
        print(f'pyAesCryptWrapper {VERSION} by Skander J. (https://github.com/skanderjeddi/)')
        print(f'Only processing the following extensions: {VALID_EXTENSIONS}')
    if os.path.isdir(path):
        if not silent:
            if mode == 'encrypt':
                print(f'Encrypting {path} recursively...')
            else:
                print(f'Decrypting {path} recursively...')
        total_time_elapsed, total_files = process_dir(path, mode, key, recur, silent)
        if not silent:
            if mode == 'encrypt':
                print(f'\tDone in {total_time_elapsed}s, total files encrypted: {total_files}.')
            else:
                print(f'\tDone in {total_time_elapsed}s, total files decrypted: {total_files}.')
    else:
        if not silent:
            print(f'\tProcessing file {path}...')
        process_file(path, mode, key, silent)
        if not silent:
            print('\tDone.')
    if not silent:
        print('Thanks for using my software!')


if __name__ == "__main__":
    main()
