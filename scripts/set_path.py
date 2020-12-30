# run this with a blender file
# blender --background file.blend  --python get_path.py ...

import os
import bpy
import yaml
import json

def get_config_for_file():
    blend_file = bpy.data.filepath
    for stage in config.keys():
        if isinstance(config[stage], dict):
            if config[stage]['blend_file'] in blend_file:
                return config[stage], stage
    
    return None

# loading config
with open('config.yaml', 'r') as config_file:
    config = yaml.load(config_file)#, Loader=yaml.FullLoader) # fix this

scene = bpy.context.scene
file_config, stage = get_config_for_file()
bfile = bpy.data.filepath.split('/')[-1].split('.')[0]

print('config: ', json.dumps(config, indent=3))
print('Initial Output Filepath: {}'.format(scene.render.filepath))

print('changing...')
# change the filepath to the new format
file_config['render_output'] = file_config['render_output'].rstrip('/')
config['file_output_format'] = config['file_output_format'].lstrip('/').format(
        bfile=bfile,
        stage=stage
        )
scene.render.filepath = '//../' + file_config['render_output'] + '/' + config['file_output_format']

print('Ending Output Filepath: {}'.format(scene.render.filepath))

#save the file and quit
bpy.ops.wm.save_mainfile()
