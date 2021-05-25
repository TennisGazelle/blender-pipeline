# run this with a blender file
# blender --background file.blend  --python get_path.py ...

import bpy
import yaml
import json
from common import init_config

config = init_config()
scene = bpy.context.scene

def main():
    print('Initial Output Filepath: {}'.format(scene.render.filepath))

    if bpy.data.images:
        for image in bpy.data.images:
            # filter out null strings
            if not image.filepath.strip():
                continue

            print('image: ', image.filepath, '---- {}'.format('OK' if '//../imgs/' in image.filepath else 'NOT OK'))


main()