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
from os import path, walk
from pathlib import Path
import ntpath
import sys
import uuid
import pyAesCrypt as aes

def main():
    if len(sys.argv) != 4:
        usage()
    else:
        mode, password, filepath = sys.argv[1].lower(), sys.argv[2], sys.argv[3]
        if mode == 'e' or mode == 'd':
            absp = os.path.abspath(filepath)
            process(mode.lower(), password, absp)
        else:
            print(f'[!] Unrecognized operation "{mode}"')
            usage()
    
def usage():
    print('[~] Usage: python3 pycrypt.py [e/d] [pwd] [path]')
    exit(0)

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def process_file(mode, password, filename, dir='.', newfilename=None, delete=True):
    if newfilename == None:
        newfilename = str(uuid.uuid4())
    basefilepath = f'{dir}/{filename}'
    fname, ext = path.splitext(basefilepath)
    resultfilepath = f'{dir}/{newfilename}{ext}'
    basefilename, resultfilename = path_leaf(basefilepath), path_leaf(resultfilepath)
    if mode == 'e':
        print(f'[~] Encrypting {basefilename} with {password} as {resultfilename}... ', end='')
        aes.encryptFile(basefilepath, resultfilepath, password)
    else:
        print(f'[~] Decrypting {basefilename} with {password} as {resultfilename}... ', end='')
        aes.decryptFile(basefilepath, resultfilepath, password)
    if delete:
        os.remove(basefilepath)
    print('done.')

def process(mode, password, filename):
    print('[/] Pycrypt 1.0.')
    print('[/] Mode: ' + ('encryption' if mode == 'e' else 'decryption') + ".\n[/] All files will be processed in their respective parent directory.")
    if os.path.isdir(filename):
        print(f'[-] {filename} is a directory, processing all sub files...')
        process_directory(mode, password, filename)
    else:
        p = Path(filename)
        process_file(mode, password, filename, dir=str(p.parent.absolute()))

def process_directory(mode, password, dirc):
    filenames = next(walk(dirc), (None, None, []))[2]
    if len(filenames) == 0:
        print(f'[!] No files found in {dirc}, exiting...')
        exit(0)
    else:
        for filename in filenames:
            process_file(mode, password, filename, dir=dirc)
        print('[-] Directory successfully processed.')
            
if __name__ == "__main__":
    main()