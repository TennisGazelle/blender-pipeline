#!/usr/bin/python3

import os 
import subprocess
import yaml
import json
from common import init_config

config = init_config()

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
                f.write(line + '\n')

                return_code = process.poll()
                if return_code is not None:
                    print('RETURN CODE: ', return_code)
                    break

def render_animation(render_cmd):
    print(render_cmd.split())

    process = subprocess.Popen(render_cmd.split(), stdout=subprocess.PIPE)

    while True:
        output = process.stdout.readline()
        line = output.strip().decode()
        print(line)

        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE: ', return_code)
            break

## start here:
import argparse

parser = argparse.ArgumentParser(description='Specify which stage to render')
parser.add_argument('--stage', metavar='s', type=str, nargs='+',
                    help='which type of render to create')

args = parser.parse_args()
if not args.stage:
    print('param not set')
    parser.print_help()
    exit(1)

print(config)

for thisStage in args.stage:
    # if this stage doesn't show up in the list, call it out
    if thisStage.lower() not in config['stages']:
        print('Stage {} not recognized in your config file'.format(thisStage))
        exit(1)
    else:
        print('initializing rendering for stage: {}'.format(thisStage))

for thisStage in args.stage:
    stage = thisStage.lower()

    render_cmd = config['docker']['render_cmd'].format(
        cwd             = os.getcwd(),
        blend_file      = config['stages'][stage]['blend_file'],
        output_location = config['stages'][stage]['render_output'],
        image           = config['docker']['image'],
        engine          = config['stages'][stage]['engine'],
        format          = config['stages'][stage]['render_format'],
        flags           = config['stages'][stage]['blender_flags']
    )

    print('rendering frames', config['stages'][stage]['buffer_frames'])


    print('running cmd: ', render_cmd)
    if '-a' in render_cmd:
        render_animation(render_cmd)
    else:
        render_frames(config['stages'][stage]['buffer_frames'], render_cmd)


print('====> QUIT')
exit(0)

#

# config[stage]['buffer_frames'] = parse_frames(config[stage]['buffer_frames'])
# frames = config[stage]['buffer_frames']
# # todo: if config[stage]['force_update'] is off, eliminate frames that already exist from being rerendered

# # docker run --rm -v {cwd}/blender/:/blender/ -v {cwd}/imgs:/imgs ikester/blender blender/{blend_file} -o {output_location} -a -E {engine} -F {format} -t 8
# render_cmd = config['docker']['render_cmd'].format(
#     cwd             = os.getcwd(),
#     blend_file      = config[stage]['blend_file'],
#     output_location = config[stage]['render_output'],
#     engine          = config[stage]['engine'],
#     format          = config[stage]['render_format'],
#     flags           = config[stage]['blender_flags']
# )

# print('running cmd: ', render_cmd)
# if '-a' in render_cmd:
#     render_animation(render_cmd)
# else:
#     render_frames(frames, render_cmd)
