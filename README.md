# blender-<as a>-pipeline (BAP)

Template pipeline for individual, small-team sized Blender project development.

This uses Docker to run a small image of blender into a Github Action that has staged rendering.
The Stages in rendering are tightly coupled with the animator's workflow in mind.

![Diagram of Blender Pipeline](docs/blender-pipeline-flowchart.png)

# Quick start

## Prerequisites:
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
0. Set up the Docker image locally (this will take some time).
```bash
docker build -t blender-pipeline scripts/
```

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

Raw, individual frames will populate in imgs/buffer/ without post processing.
A video file will be found in imgs/out/ with post processing.

## Acknowledgements
 - [**ikester/blender**](https://hub.docker.com/r/ikester/blender) - Dockerfile that has Blender in it
 - [**dolphinkiss/blender-python-docker**](https://github.com/dolphinkiss/blender-python-docker/blob/master/Dockerfile) - Similar to above; Dolphin Kiss's implementation is also simple and easy to understand.
 - [**Raymond Lo**](https://dis.co/blog/build-a-blender-docker-container-for-distributing-rendering/) - Article helping detail how to write one's own blender-based dockerfile and how to get dependencies in it.
 - [**Amber Wilkie - FreeCodeCamp**](https://www.freecodecamp.org/news/how-to-use-github-actions-to-call-webhooks/) - Calling webhooks from Github Actions.