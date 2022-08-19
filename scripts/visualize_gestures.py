import os
import subprocess
import glob

SCRIPT_DIR = os.getcwd()

BLENDER_EXE_PATH = os.path.join("C:", "Program Files (x86)", "Steam", "steamapps", "common", "Blender", "blender.exe")
BLENDER_SCRIPT_PATH = os.path.join(SCRIPT_DIR, "..", "..", "..", "genea_visualizer", "celery-queue", "blender_render.py")
INPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "subsystem3_gesture-generation", "_output", "demo")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "_output", "demo")
RECURSE_INPUT_DIR = True # Set to recursively predict from subdirectories in the input directory ; will replicate dir structure

# bvh_name = "real_Andrew_Ng_Future_Forum_Youtube.bvh"

for bvh in glob.glob(os.path.join(INPUT_DIR, "**/*.bvh"), recursive=RECURSE_INPUT_DIR):
	relative_path = os.path.relpath(bvh, INPUT_DIR)
	output_dir = os.path.join(OUTPUT_DIR, os.path.dirname(relative_path))
	bvh_name = os.path.basename(bvh)
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	
	print()
	print(output_dir)
	print(bvh_name)
	# print(in_file)
# for bvh in INPUT_DIR:
	

# subprocess.run(f'{BLENDER_EXE_PATH} -b --python {BLENDER_SCRIPT_PATH} -- -i {INPUT_DIR} , shell=True)