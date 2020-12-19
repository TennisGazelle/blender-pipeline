all: scene_render edit_render

scene_render: blender/scene.blend
	docker run --rm -v ${PWD}/blender/:/blender/ -v ${PWD}/imgs:/imgs ikester/blender blender/scene.blend -o imgs/buffer/scene_frame_#### -a -E CYCLES -t 8

edit_render: blender/edit.blend imgs/buffer/scene_frame_0001.png imgs/buffer/scene_frame_0090.png
	docker run --rm -v ${PWD}/blender/:/blender/ -v ${PWD}/imgs:/imgs ikester/blender blender/edit.blend -o imgs/buffer/edit_render -a -F AVIRAW

clean:
	rm -rf out/

clean_buffers:
	rm -rf buffer/