# run this with a blender file
# blender --background file.blend  --python set_path.py ...

import os
import bpy
import yaml
import json
from common import init_config

config = init_config()
scene = bpy.context.scene
bfile = bpy.data.filepath.split('/')[-1].split('.')[0]
path_header = '//../'

def main():
    print('config: ', json.dumps(config, indent=3))
    print('Initial Output Filepath: {}'.format(scene.render.filepath))

    if bpy.data.images:
        print('Image reference links:')
        for image in bpy.data.images:
            # filter out null strings
            if not image.filepath.strip():
                continue

            print('image: ', image.filepath, '---- {}'.format('OK' if '//../imgs/' in image.filepath else 'NOT OK'))

    print('\nchanging...\n')

    # change the filepath to the new format
    stage_settings = config['stages']['_settings']
    stage_settings['resources'] = stage_settings['resources'].rstrip('/')
    stage_settings['file_output_format'] = stage_settings['file_output_format'].lstrip('/').format(bfile=bfile)
    # scene.render.filepath = '//../' + file_config['render_output'] + '/' + config['file_output_format']

    # print('Ending Output Filepath: {}'.format(scene.render.filepath))

    if bpy.data.images:
        print('Image reference updates:')
        for image in bpy.data.images:
            if not image.filepath.strip():
                continue

            if '//../imgs/resources' not in image.filepath:
                print('updating, improper - ', image.filepath)

                # relative_to_absolute_path = image.filepath.replace('//', bpy.data.filepath).replace(bfile.lstrip('/') + '.blend', '')
                # print('looking for', relative_to_absolute_path)
                # if not os.path.isfile(relative_to_absolute_path):
                #     print('image: {} doesn\'t exist, updating and looking'.format(relative_to_absolute_path))
                #     image_name = image.filepath.split('/')[0]
                #     found_image_path = find(image_name, 'imgs/resources')
                #     if found_image_path is None:
                #         print('image: {} not found in `imgs/resources`'.format(image_name))
                #     else:
                #         image.filepath = found_image_path


    #save the file and quit
    bpy.ops.wm.save_mainfile()

main()