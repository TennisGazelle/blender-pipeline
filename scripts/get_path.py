# run this with a blender file
# blender --background file.blend  --python get_path.py ...

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

with open('config.yaml', 'r') as config_file:
    config = yaml.load(config_file)#, Loader=yaml.FullLoader) # fix this

scene = bpy.context.scene
file_config, stage = get_config_for_file()

print('config: ', json.dumps(config, indent=3))
print('Initial Output Filepath: {}'.format(scene.render.filepath))
