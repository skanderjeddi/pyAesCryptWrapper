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

'''
pyAesCrypt is a Python 3 file-encryption module and script that uses AES256-CBC to encrypt/decrypt files and binary streams.
PyPI page: https://pypi.org/project/pyAesCrypt/
GitHub page: https://github.com/marcobellaccini/pyAesCrypt
'''

# TODO: ADD DOCUMENTATION

VERSION = 1.0
EXTS = ['png', 'jpg', 'jpeg', 'mov', 'mp4', 'txt', 'heic']


def parseargs():
    validargs = True
    if len(sys.argv) != 4:
        print(
            'Usage: python3 pyAesCryptWrapper.py [encrypt/decrypt] [key] [path]')
        validargs = False
    mode, key, path = sys.argv[1].lower(), sys.argv[2], sys.argv[3]
    if mode != 'encrypt' and mode != 'decrypt':
        print(f'Unrecognized mode: {mode}')
        print('Valid modes: encrypt/decrypt')
        validargs = False
    if not os.path.exists(path):
        print(f'Invalid path: {path} doesn\'t exist on drive')
        validargs = False
    if validargs:
        return mode, key, path
    else:
        print('Some arguments were invalid. Please try again.')
        exit(-1)


def processfile(filepath, mode, key):
    pathobject = Path(filepath)
    parentdir = pathobject.parent.absolute()
    if os.getcwd() is not parentdir:
        os.chdir(parentdir)
    filename = pathobject.name
    fileext = filename.split('.')[-1].lower()
    if fileext in EXTS:
        try:
            filenewname = str(uuid.uuid4()) + '.' + fileext
            print(f'\t\t{filename} -> {filenewname}')
            if mode == 'encrypt':
                pac.encryptFile(filename, filenewname, key)
                os.remove(filename)
            elif mode == 'decrypt':
                pac.decryptFile(filename, filenewname, key)
                os.remove(filename)
        except ValueError as valuerror:
            # TODO: print error
            exit(-1)
    else:
        print(f'\tSkipping file {filename} with extension {fileext}')


def processdir(dirpath, mode, key):
    os.chdir(dirpath)
    children = os.listdir('.')
    toprocess = []
    for child in children:
        pathobject = Path(child)
        filename = pathobject.name
        fileext = filename.split('.')[-1].lower()
        if fileext in EXTS:
            toprocess.append(child)
        else:
            print(f'\tSkipping file {filename} with extension {fileext}')
    for fp in toprocess:
        processfile(fp, mode, key)
    print('\tDone.')


def main():
    print(
        f'pyAesCryptWrapper {VERSION} by Skander J. (https://github.com/skanderjeddi/)')
    print(f'Only processing the following extensions: {EXTS}')
    mode, key, path = parseargs()
    if os.path.isdir(path):
        print(f'\tProcessing directory {path}...')
        processdir(path, mode, key)
    else:
        print(f'\tProcessing file {path}...')
        processfile(path, mode, key)
        print('\tDone.')
    print('Thanks for using my software!')


if __name__ == "__main__":
    main()
