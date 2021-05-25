import yaml
import json
import os
import shutil

config = {}
def load_files_to_gen():
    with open ('template_files.yaml', 'r') as template_files:
        config['template_files'] = yaml.load(template_files)

    print(json.dumps(config, indent=3))

def make_files(sandbox_header_dir):
    print('refreshing sandbox/')
    shutil.rmtree(sandbox_header_dir)
    os.mkdir(sandbox_header_dir)
    os.mkdir(sandbox_header_dir + 'blender/')
    os.mkdir(sandbox_header_dir + 'scripts/')
    os.mkdir(sandbox_header_dir + 'logs/')

    for file in config['template_files']:
        shutil.copy(file, '{}{}'.format(sandbox_header_dir, file))
        print('file created in sandbox: {}{}'.format(sandbox_header_dir, file))

## start here:

import argparse

parser = argparse.ArgumentParser(description='Generate a template in the indicated directory')
parser.add_argument('out', metavar='o', type=str,
                    help='the output dir location (will create it if not there already)')

args = parser.parse_args()

load_files_to_gen()
make_files(args.out + "/")