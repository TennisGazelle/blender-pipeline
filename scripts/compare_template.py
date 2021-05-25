import filecmp
import yaml
import json

config = {}
sandbox_header_dir = 'sandbox/'

def load_files_to_gen():
    with open ('template_files.yaml', 'r') as template_files:
        config['template_files'] = yaml.load(template_files)

    print(json.dumps(config, indent=3))


## start here:

import argparse

parser = argparse.ArgumentParser(description='Generate a template in the indicated directory')
parser.add_argument('--template', metavar='-t', type=str, required=True,
                    help='the generated template dir')
parser.add_argument('--yours', metavar='-y', type=str, required=True,
                    help='your project root dir')
args = parser.parse_args()

load_files_to_gen('sandbox/')


# preview of file diffing
for file in config['template_files']:
    if 'blend' in file:
        continue
    
    print('checking for differences in {}{}'.format(sandbox_header_dir, file))
    areEqual = filecmp.cmp(file, '{}{}'.format(sandbox_header_dir, file))
    if areEqual:
        print(' -- good')
    else:
        print(' -- not equal')