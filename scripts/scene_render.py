#!/usr/bin/python3

import os 
import subprocess
import yaml
import json



with open('config.yaml', 'r') as config_file:
    config = yaml.load(config_file)

def parse_frames(frames_as_string):
    frames=[]
    frame_groups = frames_as_string.split(',')

    for group in frame_groups:
        if '-' in group:
            start_end_frames = group.split('-')
            for thisFrame in range(int(start_end_frames[0]), int(start_end_frames[1]) + 1):
                frames.append(int(thisFrame))
        else:
            frames.append(int(group))
    return frames


config['scene_buffer_frames'] = parse_frames(config['scene_buffer_frames'])
config['edit_buffer_frames'] = parse_frames(config['edit_buffer_frames'])

print(config)

frames = config['scene_buffer_frames']


render_cmd = "docker run --rm -v {0}/blender/:/blender/ -v {0}/imgs:/imgs ikester/blender blender/scene.blend -o imgs/buffer/scene_frame_#### -E CYCLES -t 8".format(os.getcwd())

for frame in frames:
    cmd = render_cmd + " -f {0}".format(frame)
    print(cmd.split())

    with open ('logs/render-frame-{}.log'.format(frame), 'w') as f:
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

        while True:
            output = process.stdout.readline()
            line = output.strip().decode()
            print(line)
            f.write(line)

            return_code = process.poll()
            if return_code is not None:
                print('RETURN CODE: ', return_code)
                break

# with open('test.txt', 'w') as f:
#     process = subprocess.Popen(['ls', '-l'], stdout=f)


# while True:
#     output = process.stdout.readline()
#     print(output.strip())
#     # Do something else
#     return_code = process.poll()
#     if return_code is not None:
#         print('RETURN CODE', return_code)
#         # Process has finished, read rest of the output 
#         for output in process.stdout.readlines():
#             print(output.strip())
#         break