# todo:
# parse config
# set inputs/outputs, variables, defaults
# run each model item in config (see obj-render.py)

import os
import re
import argparse
import bpy
import logging
import math
from glob import glob

os.listdir('.')

from common import init_config

config = init_config()

class Renderer():
    """
    Model manager and renderer
    """
    def __init__(self, engine, color_mode, color_depth, depth_scale, file_format, resolution):
        logging.info("initializing Modeler Renderer")
        self.args = {
            'engine': engine,
            'color_mode': color_mode,
            'color_depth': str(color_depth),
            'depth_scale': depth_scale,
            'format': file_format,
            'resolution': resolution
        }

        self.context = bpy.context
        
        self.scene = bpy.context.scene
        self.scene.use_nodes = True
        self.scene.view_layers["View Layer"].use_pass_normal = True
        self.scene.view_layers["View Layer"].use_pass_diffuse_color = True
        self.scene.view_layers["View Layer"].use_pass_object_index = True

        self.render                             = bpy.context.scene.render
        self.render.engine                      = self.args['engine'] # ('CYCLES', 'BLENDER_EEVEE', ...)
        self.render.image_settings.color_mode   = 'RGBA' # ('RGB', 'RGBA', ...)
        self.render.image_settings.color_depth  = str(color_depth) # ('8', '16')
        self.render.image_settings.file_format  = self.args['format'] # ('PNG', 'OPEN_EXR', 'JPEG, ...)
        self.render.resolution_x                = resolution
        self.render.resolution_y                = resolution
        self.render.resolution_percentage       = 100
        self.render.film_transparent            = True

        self.nodes = bpy.context.scene.node_tree.nodes
        self.links = bpy.context.scene.node_tree.links
        # Clear default nodes
        for n in self.nodes:
            self.nodes.remove(n)
        
        self.render_layers = self.nodes.new('CompositorNodeRLayers')

    def setupDepthMapRender(self):
        logging.info("Setting up Depth Map Nodes")
        self.depth_file_output                                  = self.nodes.new(type="CompositorNodeOutputFile")
        self.depth_file_output.label                            = 'Depth Output'
        self.depth_file_output.base_path                        = ''
        self.depth_file_output.file_slots[0].use_node_format    = True
        self.depth_file_output.format.file_format               = self.args['format']
        self.depth_file_output.format.color_depth               = self.args['color_depth']

        if self.args['format'] == 'OPEN_EXR':
            self.links.new(self.render_layers.outputs['Depth'], self.depth_file_output.inputs[0])
        else:
            self.depth_file_output.format.color_mode = "BW"

            # Remap as other types can not represent the full range of depth.
            self.map            = self.nodes.new(type="CompositorNodeMapValue")
            # Size is chosen kind of arbitrarily, try out until you're satisfied with resulting depth map.
            self.map.offset     = [-0.7]
            self.map.size       = [self.args['depth_scale']]
            self.map.use_min    = True
            self.map.min        = [0]

            self.links.new(self.render_layers.outputs['Depth'], self.map.inputs[0])
            self.links.new(self.map.outputs[0], self.depth_file_output.inputs[0])

    def setupNormalMapRender(self):
        logging.info("Setting up Normal Map Nodes")
        # Create normal output nodes
        # Scale Node
        self.scale_node                         = self.nodes.new(type="CompositorNodeMixRGB")
        self.scale_node.blend_type              = 'MULTIPLY'
        # self.scale_node.use_alpha             = True
        self.scale_node.inputs[2].default_value = (0.5, 0.5, 0.5, 1)
        self.links.new(self.render_layers.outputs['Normal'], self.scale_node.inputs[1])

        # Bias Node
        self.bias_node                          = self.nodes.new(type="CompositorNodeMixRGB")
        self.bias_node.blend_type               = 'ADD'
        # self.bias_node.use_alpha              = True
        self.bias_node.inputs[2].default_value  = (0.5, 0.5, 0.5, 0)
        self.links.new(self.scale_node.outputs[0], self.bias_node.inputs[1])

        # Normal Node
        self.normal_file_output                 = self.nodes.new(type="CompositorNodeOutputFile")
        self.normal_file_output.label           = 'Normal Output'
        self.normal_file_output.base_path       = ''
        self.normal_file_output.file_slots[0].use_node_format = True
        self.normal_file_output.format.file_format  = self.args['format']
        self.links.new(self.bias_node.outputs[0], self.normal_file_output.inputs[0])
    
    def setupAlbedoMapRender(self):
        logging.info("Setting up Albedo Map Nodes")
        # Create albedo output nodes
        self.alpha_albedo = self.nodes.new(type="CompositorNodeSetAlpha")
        self.links.new(self.render_layers.outputs['DiffCol'], self.alpha_albedo.inputs['Image'])
        self.links.new(self.render_layers.outputs['Alpha'], self.alpha_albedo.inputs['Alpha'])

        self.albedo_file_output                 = self.nodes.new(type="CompositorNodeOutputFile")
        self.albedo_file_output.label           = 'Albedo Output'
        self.albedo_file_output.base_path       = ''
        self.albedo_file_output.file_slots[0].use_node_format = True
        self.albedo_file_output.format.file_format = self.args['format']
        self.albedo_file_output.format.color_mode = 'RGBA'
        self.albedo_file_output.format.color_depth = self.args['color_depth']
        self.links.new(self.alpha_albedo.outputs['Image'], self.albedo_file_output.inputs[0])
    
    def setupIdMapRender(self):
        logging.info("Setting up Id Map Nodes")
        # Create id map output nodes
        self.id_file_output = self.nodes.new(type="CompositorNodeOutputFile")
        self.id_file_output.label = 'ID Output'
        self.id_file_output.base_path = ''
        self.id_file_output.file_slots[0].use_node_format = True
        self.id_file_output.format.file_format = self.args['format']
        self.id_file_output.format.color_depth = self.args['color_depth']

        if self.args['format'] == 'OPEN_EXR':
            self.links.new(self.render_layers.outputs['IndexOB'], self.id_file_output.inputs[0])
        else:
            self.id_file_output.format.color_mode = 'BW'

            self.divide_node = self.nodes.new(type='CompositorNodeMath')
            self.divide_node.operation = 'DIVIDE'
            self.divide_node.use_clamp = False
            self.divide_node.inputs[1].default_value = 2**int(self.args['color_depth'])

            self.links.new(self.render_layers.outputs['IndexOB'], self.divide_node.inputs[0])
            self.links.new(self.divide_node.outputs[0], self.id_file_output.inputs[0])

    def setupObjInScene(self, filename, modelname):
        logging.info("Importing Obj in Scene")
        # Delete default cube
        self.context.active_object.select_set(True)
        bpy.ops.object.delete()

        # Import textured mesh
        bpy.ops.object.select_all(action='DESELECT')
        self.args['filename'] = filename
        bpy.ops.import_scene.obj(filepath=filename)

        self.obj = bpy.context.selected_objects[0]
        self.obj.name = modelname
        self.context.view_layer.objects.active = self.obj

        # Possibly disable specular shading
        for slot in self.obj.material_slots:
            node = slot.material.node_tree.nodes['Principled BSDF']
            node.inputs['Specular'].default_value = 0.05

        # Set objekt IDs
        self.obj.pass_index = 1

    def setScale(self, scale):
        logging.info("Setting Obj scale")
        if self.obj != bpy.context.selected_objects[0]:
            logging.error("Imported Object isn't selected before scaling")

        bpy.ops.transform.resize(value=(scale, scale, scale))
        bpy.ops.object.transform_apply(scale=True)

    def removeDoubles(self):
        logging.info("Removing Doubles in Obj")
        if self.obj != bpy.context.selected_objects[0]:
            logging.error("Imported Object isn't selected before scaling")

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.object.mode_set(mode='OBJECT')
    
    def handleEdgeSplits(self, edge_split_angle):
        logging.info("Handling Edge Splits")
        if self.obj != bpy.context.selected_objects[0]:
            logging.error("Imported Object isn't selected before scaling")

        bpy.ops.object.modifier_add(type='EDGE_SPLIT')
        self.context.object.modifiers["EdgeSplit"].split_angle = 1.32645
        bpy.ops.object.modifier_apply(modifier="EdgeSplit")

    def setupLightsAndCamera(self):
        logging.info("Setting up Lights and Camera")
        # Make light just directional, disable shadows.
        self.light = bpy.data.lights['Light']
        self.light.type = 'SUN'
        self.light.use_shadow = False
        # Possibly disable specular shading:
        self.light.specular_factor = 1.0
        self.light.energy = 10.0

        # Add another light source so stuff facing away from light is not completely dark
        bpy.ops.object.light_add(type='SUN')
        self.light2 = bpy.data.lights['Sun']
        self.light2.use_shadow = False
        self.light2.specular_factor = 1.0
        self.light2.energy = 0.015
        bpy.data.objects['Sun'].rotation_euler = bpy.data.objects['Light'].rotation_euler
        bpy.data.objects['Sun'].rotation_euler[0] += 180

        # Place camera
        self.cam = self.scene.objects['Camera']
        self.cam.location = (0, 4, 2.4)
        self.cam.data.lens = 35
        self.cam.data.sensor_width = 32

        self.cam_constraint = self.cam.constraints.new(type='TRACK_TO')
        self.cam_constraint.track_axis = 'TRACK_NEGATIVE_Z'
        self.cam_constraint.up_axis = 'UP_Y'

        # Setup empty for camera to follow
        self.cam_empty = bpy.data.objects.new("Empty", None)
        self.cam_empty.location = (0, 0, 0)
        self.cam.parent = self.cam_empty

        self.scene.collection.objects.link(self.cam_empty)
        self.context.view_layer.objects.active = self.cam_empty
        self.cam_constraint.target = self.cam_empty

    def doRender(self, views, output_folder, output_format):
        # calc rotation and num of frames
        stepsize = 360.0 / views
        rotation_mode = 'XYZ'

        if 'filename' not in self.args.keys():
            logging.error("Filename not loaded before render call")

        for i in range(0, views):
            print("Step {} of {}, Rotation {}, {}".format(i, views, (stepsize * i), math.radians(stepsize * i)))

            thisFilename = output_format.replace('{model}', self.obj.name).replace('{angle}', '{0:03d}'.format(int(i * stepsize)))
            render_file_path = os.path.join(os.path.abspath(output_folder), thisFilename)

            print('render_file_path', render_file_path)

            self.scene.render.filepath = render_file_path.replace('{map}', 'color')
            if hasattr(self, 'depth_file_output'):
                self.depth_file_output.file_slots[0].path = render_file_path.replace('{map}', 'depth')

            if hasattr(self, 'normal_file_output'):
                self.normal_file_output.file_slots[0].path = render_file_path.replace('{map}', 'normal')

            if hasattr(self, 'alpha_albedo'):
                self.albedo_file_output.file_slots[0].path = render_file_path.replace('{map}', 'albedo')

            if hasattr(self, 'id_file_output'):
                self.id_file_output.file_slots[0].path = render_file_path.replace('{map}', 'id')

            bpy.ops.render.render(write_still=True)  # render still

            # # remove frame number from file names
            # for n in glob(render_file_path+'_*'):
            #     os.rename(n, re.sub(r'(\d+)\.([^\.]+)$', r'.\2', n))

            self.cam_empty.rotation_euler[2] += math.radians(stepsize)


modelRenderer = Renderer('CYCLES', 'RGBA', 8, 1.4, 'PNG', 600)

for model in config['models']:
    print("rendering model name: ", model)
    modelRenderer.setupObjInScene(config['models'][model]['obj_file'], model)
    modelRenderer.setScale(config['models'][model]['scaling_factor'])

    if config['models'][model]['remove_doubles']:
        modelRenderer.removeDoubles()

    if config['models'][model]['edge_split']:
        modelRenderer.handleEdgeSplits(1.32645)

    print(config['models'][model]['include'])

    if 'color' not in config['models'][model]['include']:
        print('Color map not in includes but will still be rendered by default, you cannot prevent this.')

    if 'depth' in config['models'][model]['include']:
        modelRenderer.setupDepthMapRender()

    if 'normal' in config['models'][model]['include']:
        modelRenderer.setupNormalMapRender()

    if 'albedo' in config['models'][model]['include']:
        modelRenderer.setupAlbedoMapRender()

    if 'id' in config['models'][model]['include']:
        modelRenderer.setupIdMapRender()

    modelRenderer.setupLightsAndCamera()
    modelRenderer.doRender(config['models'][model]['rotation_iterations'], config['models'][model]['render_output'], config['model_output_format'])

