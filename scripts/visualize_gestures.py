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
parser.add_argument("--blender_mp4", 						type=Path,		default=SCRIPT_DIR / '..' / 'subsystem4_visualization' / 'Blender' / 'blender_mp4.py',	help="The location of the 'blender_mp4.py' script of Blender.")
parser.add_argument("--blender_fbx", 						type=Path,		default=SCRIPT_DIR / '..' / 'subsystem4_visualization' / 'Blender' / 'blender_fbx.py',	help="The location of the 'blender_fbx.py' script of Blender.")
parser.add_argument("--input", 					"-i",		type=Path,		default=SCRIPT_DIR / ".." / "data" / "demo", 		help="The directory with .bvh files to be processed.")
parser.add_argument("--output", 				"-o",		type=Path,															help="The directory where generated .fbx and .mp4 files should be saved to.")
parser.add_argument("--mp4",								action='store_true',												help="Export an MP4 file.")
parser.add_argument("--fbx",								action='store_true',												help="Export an FBX file. This is generally slow, so use mp4 to see visualizations faster.")
parser.add_argument("--avatar",								type=str, choices=["Lea","Leffe","Majken","Harold"], default="Lea",	help="Which avatar to use for FBX exports.")
args = parser.parse_args()

if not args.mp4 and not args.fbx:
	raise ValueError("You have not indicated anything to export. Specify '--mp4' or '--fbx' (or both).")

if args.output is None:
	args.output = args.input # use input directory as output directory

args.blender_exe = args.blender_exe.resolve()
args.blender_mp4 = args.blender_mp4.resolve()
args.blender_fbx = args.blender_fbx.resolve()
args.input = args.input.resolve()
args.output = args.output.resolve()

if not os.path.exists(args.output):
	os.makedirs(args.output)

# Call Blender
for bvh_file in glob.glob(str(args.input / "*.bvh")):
	wav_file = str(Path(bvh_file).with_suffix('.wav'))
	print(f"Processing BVH animation {bvh_file}...")
	if args.mp4:
		print(f"Exporting MP4 file...")
		time.sleep(3)
		subprocess.run(
			[
				args.blender_exe		,
				'-b'					,
				'--python'				,
				args.blender_mp4		,
				'--'					,
				'--video'				,
				'-i'					,
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
		print(f"Exporting FBX file...")
		time.sleep(3)
		subprocess.run(
			[
				args.blender_exe		,
				'-b'					,
				'--python'				,
				args.blender_fbx		,
				'--'					,
				'-i'					,
				bvh_file				,
				'-o'					,
				args.output				,
				'-a'					,
				args.avatar
			]
		)