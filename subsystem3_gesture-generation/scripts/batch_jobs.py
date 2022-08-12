import os
import subprocess
import argparse
import glob

SCRIPT_DIR = os.getcwd()

parser = argparse.ArgumentParser()
parser.add_argument("--pipeline_script", help="The location of the 'pipeline.py' script for the Audio2Gestures model.", default=os.path.join(SCRIPT_DIR, '..', 'networks', 'Audio2Gestures', 'example_scripts', 'pipeline.py'))
parser.add_argument("--train_ae", "-ae", help="If set, will pretrain all autoencoder variants (specified in script) of the Audio2Gestures network.", action='store_true')
parser.add_argument("--train_gg", "-gg", help="If set, will pretrain all gesture generation model variants for all autoencoder variants (both specified in script) of the Audio2Gestures network.", action='store_true')
parser.add_argument("--predict", "-pred", help="If set, will predict gestures using all autoencoder and gesture generation variants (both specified in script) of the Audio2Gestures network, for all .wav files in the input directory (specified in script).", action='store_true')
parser.add_argument("--predict_epoch", "-epoch", help="Specifies the model epoch to use when predicting gestures. Set to -1 for the last epoch.", type=int, default=-1)

args = parser.parse_args()

PIPELINE_SCRIPT = args.pipeline_script
DATASET = os.path.join(SCRIPT_DIR, "..", "dataset", "33")
PREDICT_DIR_IN = os.path.join(DATASET, "..", "input", "demo")
PREDICT_DIR_OUT_BASE = os.path.join(DATASET, "output")
MODEL_DIR = os.path.join(SCRIPT_DIR, '..', 'models', 'Audio2Gestures')

# train autoencoders
AE_EPOCHS = 80
AE_DIMS = [32] # Available options are : 8, 32, 128, 512
if args.train_ae:
	for adim in AE_DIMS:
		subprocess.run(f'python {PIPELINE_SCRIPT} --dataset {DATASET} -adim {adim} -aeps {AE_EPOCHS} -ae', shell=True)

# train the gesture generators
GG_EPOCHS = 500
GG_DIMS = [128] # Available options are : 8, 32, 128
GG_PERIOD = 10
if args.train_gg:
	for gdim in GG_DIMS:
		for adim in AE_DIMS:
			subprocess.run(f'python {PIPELINE_SCRIPT} --dataset {DATASET} -mdir {MODEL_DIR} -adim {adim} -aeps {AE_EPOCHS} -gdim {gdim} -geps {GG_EPOCHS} -period {GG_PERIOD} -gg', shell=True)

# batch predict
SMOOTHING_MODE = 1 # set to 0 to disable smoothing
SAVGOL_WINDOW_LENGTH = 13
SAVGOL_POLY_ORDER = 3
if args.predict:
	for gdim in GG_DIMS:
		for adim in AE_DIMS:
			e_str = "e-last" if args.predict_epoch == -1 else f"e-{args.predict_epoch}"
			predict_dir_out = os.path.join(PREDICT_DIR_OUT_BASE, f'ad-{adim}_gd-{gdim}_{e_str}')
			for in_file in glob.glob(os.path.join(PREDICT_DIR_IN, "*.wav")):
				in_file = os.path.basename(in_file)
				p_in = os.path.join(PREDICT_DIR_IN, in_file)
				p_out = os.path.join(predict_dir_out, in_file.replace('.wav', '.bvh'))
				m_name = "gg_model.hdf5" if args.predict_epoch == -1 else f"gg_model_epoch{args.predict_epoch}.hdf5"
				subprocess.run(f'python {PIPELINE_SCRIPT} --dataset {DATASET} -mdir {MODEL_DIR} --predict_in {p_in} --predict_out {p_out} -adim {adim} -gdim {gdim} -gname {m_name} -pred --smoothing_mode {SMOOTHING_MODE} --savgol_window_length {SAVGOL_WINDOW_LENGTH} --savgol_poly_order {SAVGOL_POLY_ORDER}', shell=True)
