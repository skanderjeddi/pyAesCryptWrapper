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

# Arguments parsing
import argparse

# Path & IO related imports
import os
from os import path, walk
from pathlib import Path
import ntpath

# Random file name generator, should always be unique
import uuid

def main():
    # Get program parameters from the command line
    mode_raw, key, file_path_raw, output_file_name = parse_args()
    # Get absolute path of target file
    file_path = os.path.abspath(file_path_raw)
    try:
        process(mode_raw, key, file_path, output_file_name_raw=output_file_name)
    except FileNotFoundError: # If the path points to a non existing file
        print(f'\n[!] Couldn\'t find file {file_path}, exiting...')
        exit(1)
    except ValueError: 
        '''
        This exception is actually nested in the above FileNotFoundError, 
        which is why we need to handle it separately.
        '''
        print(f'\n[!] An unspecified exception was thrown while trying to process {file_path}.')
        print(f'[!] This can mean 2 things:\n\t1 - The file was not found\n\t2 - The key is incorrect and did not match the encryption key')
        print('[!] Please check your path/key and try again.\n[!] Exiting...')
        exit(1)

# Uses the argparse module
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=[ 'encrypt', 'decrypt' ])
    parser.add_argument('key', help='encryption/decryption key')
    parser.add_argument('path', help='input file path (can be a file or a directory)')
    parser.add_argument('--name', help='output file name (only works when target path points to a file)')
    args = parser.parse_args()
    return (args.mode, args.key, args.path, args.name if args.name else None)

# Copied off StackOverflow, no idea how it works
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

# Process a file
def process_file(mode, key, file_absolute_path, output_file_name=None, delete=True):
    file_path_object = Path(file_absolute_path)
    # Get parent directory to write into
    file_parent = file_path_object.parent.absolute()
    # Keep the extension because it's a hassle otherwise
    input_file_extension = path.splitext(file_absolute_path)[1]
    # If name is unspecified, generate a random UUID
    final_name = str(uuid.uuid4()) if output_file_name is None else output_file_name
    output_file_path = f'{file_parent}/{final_name}{input_file_extension}'
    input_file_name, output_file_name = path_leaf(file_absolute_path), path_leaf(output_file_path)
    if mode == 'encrypt':
        print(f'[~] Encrypting {input_file_name} with {key} as {output_file_name}... ', end='')
        # Encryption is internal to the pyAesCrypt module
        aes.encryptFile(file_absolute_path, output_file_path, key)
    else:
        print(f'[~] Decrypting {input_file_name} with {key} as {output_file_name}... ', end='')
        # Decryption is internal to the pyAesCrypt module
        aes.decryptFile(file_absolute_path, output_file_path, key)
    if delete:
        # Delete the original file - no option to turn it off at the moment - TODO
        os.remove(file_absolute_path)
    print('done.')

def process(mode, key, file_name, output_file_name_raw=None):
    # Print basic info
    print('[.] Pycrypt 1.0.')
    print('[.] Mode: ' + ('encryption' if mode == 'e' else 'decryption') + ".\n[!] All files will be processed in their respective parent directory.")
    if os.path.isdir(file_name): # If the target path points to a directory, process all sub-files, avoiding the sub-directories - TODO: add a recursive switch
        print(f'[-] {file_name} is a directory, processing all sub files...')
        process_directory(mode, key, os.path.abspath(file_name))
    else:
        process_file(mode, key, os.path.abspath(file_name), output_file_name=output_file_name_raw)
    print('[.] Done, exiting...', end='')

def process_directory(mode, key, directory):
    # Get subfiles names avoiding subdirectories
    files_names = next(walk(directory), (None, None, []))[2]
    if len(files_names) == 0:
        print(f'[!] No files found in {directory}, exiting...')
        exit(0)
    else:
        for file_name in files_names:
            process_file(mode, key, os.path.abspath(file_name))
        print('[-] Directory successfully processed.')
            
if __name__ == "__main__":
    main()