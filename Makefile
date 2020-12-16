
scene_render: blender/scene.blend
	docker run --rm -v ${PWD}/blender/:/blender/ -v ${PWD}/imgs:/imgs ikester/blender blender/scene.blend -o imgs/buffer/scene_frame_##### -f 1
