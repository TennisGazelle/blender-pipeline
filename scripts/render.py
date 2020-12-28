#!/usr/bin/python3

import os 
import subprocess
import yaml
import json


with open('config.yaml', 'r') as config_file:
    config = yaml.load(config_file)


def parse_frames(frames_as_string):
    if type(frames_as_string) == int:
        return [ frames_as_string ]

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

def render_frames(frames, render_cmd):
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


## start here:

import argparse

parser = argparse.ArgumentParser(description='Specify which frames to render')
parser.add_argument('--stage', metavar='s', type=str, nargs='?',
                    help='which type of render to create')

args = parser.parse_args()
stage = args.stage.lower()

if args.stage.lower() not in config.keys():
    print('unable to resolve blender render type: ' + str(args.stage))
    exit(0)
else:
    print('executing render for stage {}'.format(stage))
    print('using config: ')
    print(json.dumps(config, indent=3))

config[stage]['buffer_frames'] = parse_frames(config[stage]['buffer_frames'])
frames = config[stage]['buffer_frames']

# docker run --rm -v {cwd}/blender/:/blender/ -v {cwd}/imgs:/imgs ikester/blender blender/{blend_file} -o {output_location} -a -E {engine} -F {format} -t 8
render_cmd = config['docker']['cmd'].format(
    cwd             = os.getcwd(),
    blend_file      = config[stage]['blend_file'],
    output_location = config[stage]['render_output'],
    engine          = config[stage]['engine'],
    format          = config[stage]['render_format'],
    flags           = config[stage]['docker_flags']
)

print('running cmd: ', render_cmd)
render_frames(frames, render_cmd)
