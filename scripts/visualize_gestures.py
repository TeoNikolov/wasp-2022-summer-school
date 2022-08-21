# python3 visualize_gestures.py -i "../data/subsystem3_exercises/exercise_1/3-13-32-128-100/" --blender_script "../../blender_render.py"

import os
import glob
import argparse
import subprocess
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()

parser = argparse.ArgumentParser()
parser.add_argument("--blender_exe", 						type=Path,		default='/blender/blender-2.83.0-linux64/blender',	help="The location of the Blender executable.")
parser.add_argument("--blender_script", 					type=Path,		default=SCRIPT_DIR / '..' / 'subsystem4_visualization' / 'Blender' / 'blender_render.py',	help="The location of the 'blender_render.py' script of Blender.")
parser.add_argument("--input", 					"-i",		type=Path,		default=SCRIPT_DIR / ".." / "data" / "demo", 		help="The directory with .bvh files to be processed.")
parser.add_argument("--output", 				"-o",		type=Path,															help="The directory where generated .fbx and .mp4 files should be saved to.")
parser.add_argument("--mp4",								action='store_true',												help="Export an MP4 file.")
parser.add_argument("--fbx",								action='store_true',												help="Export an FBX file.")
args = parser.parse_args()

if not args.mp4 and not args.fbx:
	raise ValueError("You have not indicated anything to export. Specify '--mp4' or '--fbx' (or both).")

if args.output is None:
	args.output = args.input # use input directory as output directory

args.blender_exe = args.blender_exe.resolve()
args.blender_script = args.blender_script.resolve()
args.input = args.input.resolve()
args.output = args.output.resolve()

if not os.path.exists(args.output):
	os.makedirs(args.output)

# Call Blender

for bvh_file in glob.glob(str(args.input / "*.bvh")):
	wav_file = str(Path(bvh_file).with_suffix('.wav'))
	if args.mp4:
		print(f"Exporting MP4 file for {bvh_file}...")
		time.sleep(3)
		subprocess.run(
			[
				args.blender_exe		,
				'-b'					,
				'--python'				,
				args.blender_script		,
				'--'					,
				'--video'				,
				'--input'				,
				bvh_file				,
				'-a'					,
				wav_file				,
				'--res_x'				,
				'640'					,
				'--res_y'				,
				'480'					,
				'-o'					,
				args.output				,
				'--visualization_mode'	,
				'upper_body'			,
			]
		)
	if args.fbx:
		print(f"Exporting MP4 file for {bvh_file}...")
		raise NotImplementedError("FBX export is currently not implemented.")

# bvh_name = "real_Andrew_Ng_Future_Forum_Youtube.bvh"

# for bvh in glob.glob(os.path.join(INPUT_DIR, "**/*.bvh"), recursive=RECURSE_INPUT_DIR):
	# relative_path = os.path.relpath(bvh, INPUT_DIR)
	# output_dir = os.path.join(OUTPUT_DIR, os.path.dirname(relative_path))
	# bvh_name = os.path.basename(bvh)
	# if not os.path.exists(output_dir):
		# os.makedirs(output_dir)
	
	# print()
	# print(output_dir)
	# print(bvh_name)
	# print(in_file)
# for bvh in INPUT_DIR:
	

# subprocess.run(f'{BLENDER_EXE_PATH} -b --python {BLENDER_SCRIPT_PATH} -- -i {INPUT_DIR} , shell=True)