all: scene_render edit_render

scene_render: blender/scene.blend
	# docker run --rm -v ${PWD}/blender/:/blender/ -v ${PWD}/imgs:/imgs ikester/blender blender/scene.blend -o imgs/buffer/scene_frame_#### -a -E CYCLES -t 8
	python3 scripts/render.py --stage SCENE

edit_render: blender/edit.blend imgs/buffer/scene_frame_0001.png imgs/buffer/scene_frame_0090.png
	# docker run --rm -v ${PWD}/blender/:/blender/ -v ${PWD}/imgs:/imgs ikester/blender blender/edit.blend -o imgs/buffer/edit_render -a -F AVIRAW
	python3 scripts/render.py --stage EDIT

get_paths:
	docker run --rm -v ${PWD}/blender/:/blender/ -v ${PWD}/scripts:/scripts -v ${PWD}/config.yaml:/config.yaml blender-pipeline:latest blender/scene.blend --python scripts/get_path.py

set_paths:
	docker run --rm -v ${PWD}/blender/:/blender/ -v ${PWD}/scripts:/scripts -v ${PWD}/config.yaml:/config.yaml blender-pipeline:latest blender/scene.blend --python scripts/set_path.py

clean:
	rm -rf out/

clean_buffers:
	rm -rf buffer/

docker_build_test:
	echo 'build dockerfile'
	docker build -t blender-pipeline -f scripts/Dockerfile.test scripts/
	echo 'see if it works with the old frames and whatnot'
	python3 scripts/render.py --stage SCENE
	echo 'if that works, try with the other blender files with yaml'
	docker run --rm -v ${PWD}/blender/:/blender/ -v ${PWD}/scripts:/scripts blender-pipeline:latest blender/scene.blend --python scripts/get_path.py
