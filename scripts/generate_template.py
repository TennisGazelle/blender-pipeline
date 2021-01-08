import yaml
import json
import os
import shutil

config = {}
sandbox_header_dir = 'sandbox/'

with open ('template_files.yaml', 'r') as template_files:
    config['template_files'] = yaml.load(template_files)

print(json.dumps(config, indent=3))

print('refreshing sandbox/')
shutil.rmtree(sandbox_header_dir)
os.mkdir(sandbox_header_dir)
os.mkdir(sandbox_header_dir + 'blender/')
os.mkdir(sandbox_header_dir + 'scripts/')
os.mkdir(sandbox_header_dir + 'logs/')

for file in config['template_files']:
    shutil.copy(file, '{}{}'.format(sandbox_header_dir, file))
    print('file created in sandbox: {}{}'.format(sandbox_header_dir, file))

