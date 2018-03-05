import os, json
import glob
import subprocess

path = '.'
wildcard_search = 'avg_rade*.tif'

files = glob.glob(f'{path}/**/*{wildcard_search}', recursive=True)
output_file='file_floored.tif'


for file in files:
    output_dir = file.split('/')[1]
    print(output_dir)
    CMD = f'gdal_calc.py -A {file} --outfile={output_dir}/{output_file} --calc="A*(A>=0)"'
    print(CMD)
    return_code = subprocess.call(CMD, shell=True)  
    print(return_code)
