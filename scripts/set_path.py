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

print('stage specific config: ', json.dumps(file_config, indent=3))
print('Initial Output Filepath: {}'.format(scene.render.filepath))

# change the filepath to the new format
file_config['render_output'] = file_config['render_output'].rstrip('/')
config['file_output_format'] = config['file_output_format'].lstrip('/').format(
        bfile=bpy.data.filepath.rpartition('.')[0],
        stage=stage
        )
scene.render.filepath = file_config['render_output'] + '/' + config['file_output_format']

print('config: ', json.dumps(config, indent=3))

print('Ending Output Filepath: {}'.format(scene.render.filepath))

#save the file and quit
bpy.ops.wm.save_mainfile()
