# blender-pipeline

Template pipeline for individual, small-team sized Blender project development.

This uses Docker to run a small image of blender into a Github Action that has staged rendering.
The Stages in rendering are tightly coupled with the animator's workflow in mind.

![Diagram of Blender Pipeline](docs/blender-pipeline-flowchart.png)

# Quick start

## Prerequsite
Needed to be installed/configured on your local machine.
 - python3
    - pip install pyyaml
 - blender (as cli)
 - docker

## Set Up
A stage is a specific rendering configuration, details in `config.yaml`, consisting of at least one blender file to be rendered.
The information held in such a stage includes:

```yaml
scene:
  buffer_frames: 1-9
  force_update: false
  render_output: 'imgs/buffer/'
  engine: CYCLES # EEVEE support coming soon
  blend_file: scene.blend
  render_format: PNG
  docker_flags: ''
```

In this project, Stage `scene` refers to the blend file that contains the models/textures to be build, and stage `edit` includes the blender file with post processing.

## Render
1. If you just downloaded this project, first set the paths of your working directory.

```bash
make set_paths
# or make set_paths_mac (for mac users)
```

You can verify the output of this with `make get_paths` and `make get_paths_mac`

2. Render the scene stage
```bash
make scene_render
```

3. Render the post processing stage (edit)
```bash
make edit_render
```
