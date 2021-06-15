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

'''
pyAesCrypt is a Python 3 file-encryption module and script that uses AES256-CBC to encrypt/decrypt files and binary streams.
PyPI page: https://pypi.org/project/pyAesCrypt/
GitHub page: https://github.com/marcobellaccini/pyAesCrypt
'''
import pyAesCrypt as aes

# Path & IO related imports
import os
from os import path, walk
from pathlib import Path
import ntpath

# Random file name generator, should always be unique
import uuid

from sys import argv

def main():
    if len(argv) != 4:
        usage()
    else:
        mode, password, file_path = argv[1].lower(), argv[2], os.path.abspath(argv[3])
        if mode == 'e' or mode == 'd':
            try:
                process(mode, password, file_path)
            except FileNotFoundError:
                print(f'\n[!] Couldn\'t find file {file_path}, exiting...')
                exit(1)
            except ValueError:
                print(f'\n[!] An unspecified exception was thrown while trying to process {file_path}.')
                print(f'[!] This often means that the input file could not be located. Check your path and try again.')
                print('[!] Exiting...')
                exit(1)
        else:
            print(f'[!] Unrecognized operation "{mode}"')
            usage()
    
def usage():
    print('[~] Usage: python3 pycrypt.py [e/d] [pwd] [path]')
    exit(0)

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def process_file(mode, password, file_absolute_path, delete=True):
    file_path_object = Path(file_absolute_path)
    file_parent = file_path_object.parent.absolute()
    random_uuid = str(uuid.uuid4())
    input_file_extension = path.splitext(file_absolute_path)[1]
    output_file_path = f'{file_parent}/{random_uuid}{input_file_extension}'
    input_file_name, output_file_name = path_leaf(file_absolute_path), path_leaf(output_file_path)
    if mode == 'e':
        print(f'[~] Encrypting {input_file_name} with {password} as {output_file_name}... ', end='')
        aes.encryptFile(file_absolute_path, output_file_path, password)
    else:
        print(f'[~] Decrypting {input_file_name} with {password} as {output_file_name}... ', end='')
        aes.decryptFile(file_absolute_path, output_file_path, password)
    if delete:
        os.remove(file_absolute_path)
    print('done.')

def process(mode, password, file_name):
    print('[.] Pycrypt 1.0.')
    print('[.] Mode: ' + ('encryption' if mode == 'e' else 'decryption') + ".\n[!] All files will be processed in their respective parent directory.")
    if os.path.isdir(file_name):
        print(f'[-] {file_name} is a directory, processing all sub files...')
        process_directory(mode, password, os.path.abspath(file_name))
    else:
        process_file(mode, password, os.path.abspath(file_name))
    print('[.] Done, exiting...')

def process_directory(mode, password, directory):
    files_names = next(walk(directory), (None, None, []))[2]
    if len(files_names) == 0:
        print(f'[!] No files found in {directory}, exiting...')
        exit(0)
    else:
        for file_name in files_names:
            process_file(mode, password, os.path.abspath(file_name))
        print('[-] Directory successfully processed.')
            
if __name__ == "__main__":
    main()