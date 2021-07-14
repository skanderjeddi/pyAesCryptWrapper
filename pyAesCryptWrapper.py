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

import os
import sys
import uuid
from pathlib import Path

'''
pyAesCrypt is a Python 3 file-encryption module and script that uses AES256-CBC to encrypt/decrypt files and binary streams.
PyPI page: https://pypi.org/project/pyAesCrypt/
GitHub page: https://github.com/marcobellaccini/pyAesCrypt
'''
import pyAesCrypt as pac

# TODO: ADD DOCUMENTATION

VERSION = 1.0
VALID_EXTENSIONS = ['png', 'jpg', 'jpeg', 'mov', 'mp4', 'txt', 'heic']


def parse_args():
    valid_args = True
    if len(sys.argv) != 4:
        print(
            'Usage: python3 pyAesCryptWrapper.py [encrypt/decrypt] [key] [path]')
        valid_args = False
    mode, key, path = sys.argv[1].lower(), sys.argv[2], sys.argv[3]
    if mode != 'encrypt' and mode != 'decrypt':
        print(f'Unrecognized mode: {mode}')
        print('Valid modes: encrypt/decrypt')
        valid_args = False
    if not os.path.exists(path):
        print(f'Invalid path: {path} doesn\'t exist on drive')
        valid_args = False
    if valid_args:
        return mode, key, path
    else:
        print('Some arguments were invalid. Please try again.')
        exit(-1)


def process_file(filepath, mode, key):
    path_object = Path(filepath)
    parent_dir = path_object.parent.absolute()
    if os.getcwd() is not parent_dir:
        os.chdir(parent_dir)
    file_name = path_object.name
    file_ext = file_name.split('.')[-1].lower()
    if file_ext in VALID_EXTENSIONS:
        try:
            file_uuid = str(uuid.uuid4()) + '.' + file_ext
            print(f'\t\t{file_name} -> {file_uuid}')
            if mode == 'encrypt':
                pac.encryptFile(file_name, file_uuid, key)
                os.remove(file_name)
            elif mode == 'decrypt':
                pac.decryptFile(file_name, file_uuid, key)
                os.remove(file_name)
        except ValueError as value_error:
            print(f'An error occurred while processing {file_name}: {value_error}')
            exit(-1)
    else:
        print(f'\tSkipping file {file_name} with extension {file_ext}')


def process_dir(dirpath, mode, key):
    os.chdir(dirpath)
    children = os.listdir('.')
    files_to_process = []
    for child in children:
        path_object = Path(child)
        file_name = path_object.name
        file_ext = file_name.split('.')[-1].lower()
        if file_ext in VALID_EXTENSIONS:
            files_to_process.append(child)
        else:
            print(f'\tSkipping file {file_name} with extension {file_ext}')
    for fp in files_to_process:
        process_file(fp, mode, key)
    print('\tDone.')


def main():
    print(
        f'pyAesCryptWrapper {VERSION} by Skander J. (https://github.com/skanderjeddi/)')
    print(f'Only processing the following extensions: {VALID_EXTENSIONS}')
    mode, key, path = parse_args()
    if os.path.isdir(path):
        print(f'\tProcessing directory {path}...')
        process_dir(path, mode, key)
    else:
        print(f'\tProcessing file {path}...')
        process_file(path, mode, key)
        print('\tDone.')
    print('Thanks for using my software!')


if __name__ == "__main__":
    main()
