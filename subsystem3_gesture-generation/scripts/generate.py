import os
import glob
import argparse
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()

parser = argparse.ArgumentParser()
# parser.add_argument("--epoch", "-e",				help="Specifies the model epoch to use when predicting gestures. Set to -1 for the last epoch.", type=int, default=-1)
parser.add_argument("--pipeline_script", 					type=Path, 								default=SCRIPT_DIR / '..' / 'networks' / 'Audio2Gestures' / 'example_scripts' / 'pipeline.py',	help="The location of the 'pipeline.py' script for the Audio2Gestures model.")
parser.add_argument("--input", 					"-i",		type=Path, 	 							default=SCRIPT_DIR / ".." / "_input" / "demo", 		help="The directory with .wav files to generate gesture for.")
parser.add_argument("--output", 				"-o",		type=Path, 					 			default=SCRIPT_DIR / ".." / "_output" / "demo", 	help="The directory where generated .bvh files should be output to.")
parser.add_argument("--data_size", 				"-data",	type=int, 	choices=[33, 100], 			default=100, 	help="The amount of data in % on which the gesture model was trained on.")
parser.add_argument("--autoencoder", 			"-aedim",	type=int, 	choices=[8, 32, 128, 512], 	default=32, 	help="The representation dimensionality of the autoencoder.")
parser.add_argument("--encoder", 				"-edim",	type=int, 	choices=[8, 32, 128], 		default=128, 	help="The hidden layer size of the encoder.")
parser.add_argument("--smoothing_poly_order", 	"-spo",		type=int, 	 							default=3, 		help="The polynomial order of the Savitsky-Golay digital filter.")
parser.add_argument("--smoothing_window_size", 	"-sws",		type=int, 							 	default=13, 	help="The window size of the Savitsky-Golay digital filter.")
# parser.add_argument("--verbose", 				"-v",		type=int, 							 	default=13, 	help="The window size of the Savitsky-Golay digital filter.")
args = parser.parse_args()

args.input = args.input.resolve()
args.output = args.output.resolve()

if not os.path.exists(args.output):
	os.makedirs(args.output)

fingerprint_str = f"{args.smoothing_poly_order}-{args.smoothing_window_size}-{args.autoencoder}-{args.encoder}-{args.data_size}"
fingerprint_dir = args.output / fingerprint_str
if not os.path.exists(fingerprint_dir):
	os.mkdir(fingerprint_dir)
	
for wav_file in glob.glob(str(args.input / "*.wav")):
	input_file = args.input / Path(wav_file).name
	output_file = fingerprint_dir / Path(wav_file).with_suffix(".bvh").name
	model_dir = SCRIPT_DIR / '..' / 'models' / 'Audio2Gestures'
	data_dir = SCRIPT_DIR / '..' / 'dataset' / str(args.data_size)
	
	command = (
		f"python "
		f"{args.pipeline_script} "									# specifies the location of the 'pipeline.py' script of the Audio2Gestures model
		f"--dataset {data_dir} "									# specifies the data size
		f"-mdir {model_dir} "										# specifies the directory with pretrained autoencoder and encoder models
		f"--predict_in {input_file} "								# specified the path and name of an input .wav file
		f"--predict_out {output_file} "								# specifies the path and name of an output .bvh file
		f"-adim {args.autoencoder} "								# specifies the representation dimensionality of the autoencoder
		f"-gdim {args.encoder} "									# specifies the hidden layer size of the encoder
		f"--savgol_poly_order {args.smoothing_poly_order} "			# specifies the Savitsky-Golay polynomial order
		f"--savgol_window_length {args.smoothing_window_size} "		# specifies the Savitsky-Golay window size
		f"-gname gg_model.hdf5 "									# specifies the name of the pretrained encoder model to use
		f"-pred " 													# instruct Audio2Gestures to predict gestures

	)

	print(f'Processing "{input_file.name}" ...')
	subprocess.run(command, shell=True)