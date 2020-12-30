#!/usr/bin/python3

import os 
import subprocess
import yaml
import json

with open('config.yaml', 'r') as config_file:
    config = yaml.load(config_file)

def run_cmd(render_cmd):
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

