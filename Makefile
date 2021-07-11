all: set_paths model_render scene_render edit_render

cool_scene_render: blender/cool_scene.blend
	python3 scripts/render.py --stage cool_scene

scene_render: blender/scene.blend
	python3 scripts/render.py --stage SCENE

edit_render: blender/edit.blend imgs/buffer/scene_scene_0001.png imgs/buffer/scene_scene_0090.png
	python3 scripts/render.py --stage EDIT

model_render: blender/models/curve-skeleton-cube.obj
	docker run --rm -v ${PWD}/dump:/tmp -v ${PWD}/blender/:/blender/ -v ${PWD}/scripts:/scripts -v ${PWD}/config.yaml:/config.yaml -v ${PWD}/imgs/:/imgs tennisgazelle/blender-pipeline:latest --python scripts/model-render.py

local_model_render: local_move_common_to_blender_py
	/Applications/Blender.app/Contents/MacOS/Blender -b --python scripts/model-render.py

single_obj_render: blender/models/curve-skeleton-cube.obj
	docker run --rm -v ${PWD}/dump:/tmp -v ${PWD}/blender/:/blender/ -v ${PWD}/scripts:/scripts -v ${PWD}/config.yaml:/config.yaml -v ${PWD}/imgs/:/imgs tennisgazelle/blender-pipeline:latest --python scripts/obj-render.py -- --output_folder imgs/out/ blender/models/curve-skeleton-cube.obj

local_single_obj_render: local_move_common_to_blender_py
	/Applications/Blender.app/Contents/MacOS/Blender -b --python scripts/obj-render.py -- --output_folder imgs/out/ blender/models/curve-skeleton-cube.obj

docker: scripts/Dockerfile
	docker build -t tennisgazelle/blender-pipeline:latest scripts/

get_paths:
	docker run --rm -v ${PWD}/blender/:/blender/ -v ${PWD}/scripts:/scripts -v ${PWD}/config.yaml:/config.yaml tennisgazelle/blender-pipeline:latest blender/cool_scene.blend --python scripts/get_path.py
	docker run --rm -v ${PWD}/blender/:/blender/ -v ${PWD}/scripts:/scripts -v ${PWD}/config.yaml:/config.yaml tennisgazelle/blender-pipeline:latest blender/scene.blend --python scripts/get_path.py
	docker run --rm -v ${PWD}/blender/:/blender/ -v ${PWD}/scripts:/scripts -v ${PWD}/config.yaml:/config.yaml tennisgazelle/blender-pipeline:latest blender/edit.blend --python scripts/get_path.py

set_paths:
	docker run --rm -v ${PWD}/blender/:/blender/ -v ${PWD}/scripts:/scripts -v ${PWD}/config.yaml:/config.yaml tennisgazelle/blender-pipeline:latest blender/cool_scene.blend --python scripts/set_path.py
	docker run --rm -v ${PWD}/blender/:/blender/ -v ${PWD}/scripts:/scripts -v ${PWD}/config.yaml:/config.yaml tennisgazelle/blender-pipeline:latest blender/scene.blend --python scripts/set_path.py
	docker run --rm -v ${PWD}/blender/:/blender/ -v ${PWD}/scripts:/scripts -v ${PWD}/config.yaml:/config.yaml tennisgazelle/blender-pipeline:latest blender/edit.blend --python scripts/set_path.py

local_get_paths: local_move_common_to_blender_py
	/Applications/Blender.app/Contents/MacOS/Blender -b blender/cool_scene.blend --python scripts/get_path.py

local_move_common_to_blender_py:
	cp scripts/common.py /Applications/Blender.app/Contents/Resources/2.81/python/lib/python3.7/

clean:
	rm -rf out/ imgs/out/models/debug/

clean_buffers:
	rm -rf buffer/

docker_build_test:
	echo 'build dockerfile'
	docker build -t blender-pipeline scripts/
	echo 'see if it works with the old frames and whatnot'
	python3 scripts/render.py --stage SCENE
	echo 'if that works, try with the other blender files with yaml'
	docker run --rm -v ${PWD}/blender/:/blender/ -v ${PWD}/scripts:/scripts blender-pipeline:latest blender/scene.blend --python scripts/get_path.py

