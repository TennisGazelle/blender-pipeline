import filecmp
import yaml
import json

config = {}
sandbox_header_dir = 'sandbox/'

with open ('template_files.yaml', 'r') as template_files:
    config['template_files'] = yaml.load(template_files)

for file in config['template_files']:
    if 'blend' in file:
        continue
    
    print('checking for differences in {}{}'.format(sandbox_header_dir, file))
    areEqual = filecmp.cmp(file, '{}{}'.format(sandbox_header_dir, file))
    if areEqual:
        print(' -- good')
    else:
        print(' -- not equal')


