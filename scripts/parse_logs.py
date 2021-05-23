#!/usr/bin/python3

import re
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dts
import matplotlib
import pylab

# example log format

# Fra:1 Mem:79.96M (0.00M, Peak 79.96M) | 
# Time:00:00.04 | 
# Mem:0.00M, Peak:0.00M | 
# Scene, View Layer | 
# Synchronizing object | 
# Cube

# Fra:1 Mem:358.05M (0.00M, Peak 702.70M) | 
# Time:00:54.02 | 
# Remaining:05:36.30 | 
# Mem:276.06M, Peak:620.72M | 
# Scene, View Layer | 
# Rendered 57/510 Tiles, Denoised 26 tiles

re_log_header = re.compile('Fra:([0-9]+) Mem:([0-9.A-Z]+) \(\S+\, Peak ([0-9.A-Z]+)\)')
re_log_frame_progress = re.compile('Rendered ([0-9]+)\/([0-9]+) Tiles, Denoised ([0-9]+) tiles')


def parse_log_header(log):
    result = re_log_header.match(log.strip())
    if result is None:
        print('error with log: ', log, ',cannot parse header')
        return {
            "memory_used": pylab.nan,
            "peak_memory_used": pylab.nan
        }

    frame = result.group(1)
    memory_used = result.group(2)
    peak_memory_used = result.group(3)
    return {
        "frame": frame, 
        "memory_used": float(memory_used.rstrip('M')),
        "peak_memory_used": float(peak_memory_used.rstrip('M'))
    }


def parse_time(log):
    remainder = log.strip().lstrip('Time:').strip()
    struct_time = datetime.datetime.strptime(remainder, '%M:%S.%f')
    return {
        "time": remainder,
        "time_obj": struct_time
    }


def parse_frame_progress(log):
    result = re_log_frame_progress.match(log.strip())
    if result is None:
        print('error with parsing log footer: ', log, ', cannot parse footer')
        return {
            "tile": pylab.nan,
            "num_tiles": pylab.nan,
            "num_denoised_tiles": pylab.nan
        }

    current_tile = result.group(1)
    num_denoised_tiles = result.group(3)
    all_tiles = result.group(2)
    return {
        "tile": int(current_tile),
        "num_tiles": all_tiles,
        "num_denoised_tiles": int(num_denoised_tiles)
    }


with open('logs/render-frame-1.log', 'r') as log_file:
    logs = log_file.readlines()

chart_data = []
x = -1
for log in logs:
    chunks = log.split('|')
    x += 1
    if len(chunks) <= 1:
        print('skipping parsing for line: ', log)
        continue

    # first chunk
    data = {
        "line": x
    }
    data.update(parse_log_header(chunks[0]))
    data.update(parse_time(chunks[1]))
    data.update(parse_frame_progress(chunks[-1]))
    chart_data.append(data)

    # print(json.dumps(data, indent=3))

    # if x == 100:
    #     break 

# print([ x['memory_used'] for x in chart_data ])


x = np.array([ d['time_obj'] for d in chart_data ])
x_time = dts.date2num(x)

y_mem_used = np.array([ d['memory_used'] for d in chart_data ])
y_tiles = np.array([ d['tile'] for d in chart_data ])
y_tiles_denoised = np.array([ d['num_denoised_tiles'] for d in chart_data ])


fig, ax = plt.subplots()
# Twin the x-axis twice to make independent y-axes.
axes = [ax, ax.twinx(), ax.twinx()]

axes[0].plot_date(x_time, y_tiles, 'b-')
axes[0].set_ylabel('Num Tiles Rendered')

axes[1].plot_date(x_time, y_mem_used, 'r-')
axes[0].set_ylabel('Memory Used (MB)')

axes[2].plot_date(x_time, y_tiles_denoised, 'g-')
axes[0].set_ylabel('Num Tiles Denoised')

# finish to clean up the axis with this:
# https://stackoverflow.com/questions/7733693/matplotlib-overlay-plots-with-different-scales

plt.show()
