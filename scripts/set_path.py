# run this with a blender file
# blender --background file.blend  --python set_path.py ...

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

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

# loading config
with open('config.yaml', 'r') as config_file:
    config = yaml.load(config_file)#, Loader=yaml.FullLoader) # fix this

scene = bpy.context.scene
file_config, stage = get_config_for_file()
bfile = bpy.data.filepath.split('/')[-1].split('.')[0]

print('config: ', json.dumps(config, indent=3))
print('Initial Output Filepath: {}'.format(scene.render.filepath))

if bpy.data.images:
    print('Image reference links:')
    for image in bpy.data.images:
        if not image.filepath.strip():
            continue

        print('image: ', image.filepath)
        if 'resources' in image.filepath and '//../imgs/resources' not in image.filepath:
            print('improper - ', image.filepath)
        else:
            print('  proper - ', image.filepath)

print('\nchanging...\n')
# change the filepath to the new format
file_config['render_output'] = file_config['render_output'].rstrip('/')
config['file_output_format'] = config['file_output_format'].lstrip('/').format(
        bfile=bfile,
        stage=stage
        )
scene.render.filepath = '//../' + file_config['render_output'] + '/' + config['file_output_format']

print('Ending Output Filepath: {}'.format(scene.render.filepath))


# if bpy.data.images:
#     print('Image reference updates:')
#     for image in bpy.data.images:
#         if not image.filepath.strip():
#             continue

#         if '//../imgs/resources' not in image.filepath:
#             print('updating, improper - ', image.filepath)

#             relative_to_absolute_path = image.filepath.replace('//', bpy.data.filepath).replace(bfile.lstrip('/') + '.blend', '')
#             print('looking for', relative_to_absolute_path)
#             if not os.path.isfile(relative_to_absolute_path):
#                 print('image: {} doesn\'t exist, updating and looking'.format(relative_to_absolute_path))
#                 image_name = image.filepath.split('/')[0]
#                 found_image_path = find(image_name, 'imgs/resources')
#                 if found_image_path is None:
#                     print('image: {} not found in `imgs/resources`'.format(image_name))
#                 else:
#                     image.filepath = found_image_path


#save the file and quit
bpy.ops.wm.save_mainfile()
