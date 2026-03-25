import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('module_name', type=str)
args = parser.parse_args()

path_to_modules = 'src/modules/'
os.mkdir(path_to_modules + args.module_name)
open(path_to_modules + args.module_name + '/' + args.module_name + '.module.py', 'x')
open(path_to_modules + args.module_name + '/' + args.module_name + '.keyboard.py', 'x')
open(path_to_modules + args.module_name + '/' + args.module_name + '.db.py', 'x')