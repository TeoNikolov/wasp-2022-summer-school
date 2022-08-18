
# Subsystem 3: Gesture Generation

 - [Exercise 1 : Setup and get the base model to work](#exercise-1--setup-and-get-the-base-model-to-work)
   * [Setting up the environment](#setting-up-the-environment)
   * [Generating gestures](#generating-gestures)
 - [Exercise 2 : Explore smoothing parameters](#exercise-2--explore-smoothing-parameters)
 - [Exercise 3 : Explore representation dimensionality of the AE](#exercise-3--explore-representation-dimensionality-of-the-ae)
 - [Exercise 4 : Explore the hidden layer size of the encoder](#exercise-4--explore-the-hidden-layer-size-of-the-encoder)
 - [Exercise 5 : Play with the dataset size](#exercise-5--play-with-the-dataset-size)
 - [Exercise 6 : Try the model on different audio](#exercise-6--try-the-model-on-different-audio)
 - [Bonus Exercise : Using real speech for exercises 2-5](#bonus-exercise--using-real-speech-for-exercises-2-5)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

---

Before continuing, make sure that you have cloned the [wasp-2022-summer-school](https://github.com/TeoNikolov/wasp-2022-summer-school) and all child repositories by executing the following in your shell:

- `git clone https://github.com/TeoNikolov/wasp-2022-summer-school.git`
- `git submodule update --init`

Remarks:
- It is possible some commands fail due to lack of privilige. If this happens, please write `sudo` at the beginning of the command.
- All file system paths in this documentation are relative to the directory in which this readme resides.


## Exercise 1 : Setup and get the base model to work

### Setting up the environment
The gesture generation subsystem implements a single gesture model called `Audio2Gestures`. This model is located in `./networks/Audio2Gestures/`, and is maintained in a separate [GitHub repository](https://github.com/teonikolov/Speech_driven_gesture_generation_with_autoencoder/tree/GENEA_2022) (a fork of the [original repository](https://github.com/genea-workshop/Speech_driven_gesture_generation_with_autoencoder/tree/GENEA_2022) by [Taras Kucherenko](https://github.com/Svito-zar)). This model has an integration with Docker to automate the process of setting up a working environment with required dependencies, in which the model can be trained and used to predict gestures from raw audio.

The script `./scripts/deploy.sh` calls the necessary commands to leverage the Docker integration of the gesture model. The script first builds a Docker image by setting up a guest OS and collecting necessary dependencies, followed by deploying a Docker container in which the gesture model is encapsulated. In addition, the folder `./subsystem3_gesture-generation/` is mounted to `/app/wasp/` in the container's filesystem, so that pre-processed dataset files inside `./dataset/`, and pre-trained models inside `./models/`, can be accessed from within the Docker container. The model needs these files to predict gestures.

To setup the environment:

1. Make sure [Docker](https://docs.docker.com/get-docker/) is installed and running on your machine.
1. `cd ./scripts/` and then run the script with `bash ./deploy.sh`
1. Wait for Docker to set up the environment and deploy the container. This could take a while, so why not check this cool [fluid simulator](https://paveldogreat.github.io/WebGL-Fluid-Simulation/) out in the meantime?

If everything went well, you will now have a Docker container with the gesture model running in the background. You can verify that this is the case by running `docker ps` in your shell, and searching for a container whose `IMAGE` says `"wasp-gg"`.  The next step is to open a shell to the container, so that we can interact with the files inside it. To do this, run the following command:

&nbsp;&nbsp;&nbsp;&nbsp;`docker exec -it <container_ID> /bin/bash`

Replace `<container_ID>` with the ID of the container, which is shown using `docker ps`.

### Generating gestures

The next part of the exercise is to familiarize yourself with the generation procedure. For this, we will predict gestures for files inside the `./_input/exercise_1/`. For this purpose, you should use the supplied `./scripts/generate.py` script, located in `/app/wasp/scripts/` inside the Docker container. Navigate to that location using `cd /app/wasp/scripts/` and run the script as such:

&nbsp;&nbsp;&nbsp;&nbsp;`python generate.py -i "../_input/exercise_1/" -o "../_output/exercise_1/" --pipeline_script "../../example_scripts/pipeline.py"`

- `-i` specifies a directory with input `.wav` raw audio files to predict gestures for
- `-o` specifies a directory where generated `.bvh` files will be saved to
- `--pipeline_script` points to the location of the `pipeline.py` script, which is responsible for invoking low-level functions of the Audio2Gestures model

After calling the script, you will see files popping up inside `./_output/exercise_1/3-13-32-128-100/`. These files are the input `.wav` file, output `.bvh` file, as well as intermediate files used by the gesture model. The output directory `3-13-32-128-100/` is created to help you organize generated files. This will come in handy for the next exercises, as you will be modifying various parameters when running `generate.py`. The following naming convention is used:

&nbsp;&nbsp;&nbsp;&nbsp;`{1}_{2}_{3}_{4}_{5}`

1. Savitsky-Golay polynomial order
1. Savitsky-Golay window size
1. Representation dimensionality of the autoencoder
1. Hidden layer size of the encoder
1. Size of data in % on which Audio2Gestures was trained on

*Tip: Open `generate.py` in your favorite text editor, and take a peek at the code inside!*
*Tip 2: The `generate.py` script processes all `.wav` files in the input directory. Make sure your audio files are in the same directory so you can process them in batch with a single command!*
*Tip 3: There are more input and output files in `./_input/demo/` and `./_output/demo/` respectively (3 of synthesized speech, and 2 of real speech from YouTube). Feel free to use these audio files in the next exercises. In fact, we highly encourage you to do this, so you can compare the results of using different input data!*

## Exercise 2 : Explore smoothing parameters

The Audio2Gestures model generates somewhat jerky movements, which are made better by applying a [Savitsky-Golay smoothing filter](https://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter).

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/8/89/Lissage_sg3_anim.gif" alt="savitsky-golay visualization">
  <br>
  <i>Visualization of Savitsky-Golay polynomial fitting</i>
</p>

The Savitsky-Golay smoothing filter uses polynomial fitting for smoothing noisy curves. The fitting procedure requires one to choose an order for the polynomial being fit, as well as the number of data points to consider (a.k.a. window size). Your task is to experiment with these two parameters, and to see which combination yields more visually-pleasing results for your generated gestures.

We will use the same script from exercise 1, but this time you will pass values to the `--smoothing_poly_order` (`-spo`) and `--smoothing_window_size` (`-sws`) arguments. There several constrains when passing values to these arguments:

- `--smoothing_window_size` must be an odd integer between `3` and `127` inclusive (default is `13`)
- `--smoothing_poly_order` must be an integer between `1` and `11` inclusive (default is `3`)
- `--smoothing_poly_order` must be lower than `--smoothing_window_size`

Here is an example command (will output to `./_output/exercise_2/2-5-32-128-100/`):

&nbsp;&nbsp;&nbsp;&nbsp;`python generate.py -spo 2 -sws 5 -i "../_input/exercise_2/" -o "../_output/exercise_2/" --pipeline_script "../../example_scripts/pipeline.py"`

Now modify the parameters, and see how your generated gestures are affected by the smoothing filter!

*Tip: Observe at which point the values start to lead to under-smoothed or over-smoothed motion!*

## Exercise 3 : Explore representation dimensionality of the AE

Next, you should explore how changing the representation dimensionality of the autoencoder in Audio2Gestures affects the gestures. Theoretically, a small dimensionality forces the autoencoder to compress the high-dimensional input data into fewer dimensions. This can improve the data by excluding irrelevant details about the original representation, which are not useful for generalization. On the contrary, over-compression can lead to poor generalization because important information may get lost in the process.

As before, we will use the script from exercise 1, but this time you will pass a value to the `--autoencoder` (`-aedim`) argument. Since we provide pre-trained autoencoder models (doing this yourself can take a *long* time, trust me), you can use only the following values:

-  `8`
-  `32` (default)
-  `128`
-  `512`

Here is an example command (will output to `./_output/exercise_3/3-13-128-128-100/`):

&nbsp;&nbsp;&nbsp;&nbsp;`python generate.py -aedim 128 -i "../_input/exercise_3/" -o "../_output/exercise_3/" --pipeline_script "../../example_scripts/pipeline.py"`

Go ahead, see how your generated gestures are affected by the autoencoder dimensionality!

*Tip: Look at the how expressive the gestures are in terms of speed and location. Are these similar for the whole duration, or do they vary?*


## Exercise 4 : Explore the hidden layer size of the encoder

This exercise is very similar to exercise 3, but instead of varying the dimensionality of the autoencoder, you will vary the dimensionality of the Audio2Gestures encoder. The encoder maps audio features to motion features, and the size of its hidden layers directly affects its capacity to generalize to input data. Theoretically, a small layer size will lack the capacity to learn from input data, leading to underfitting. On the contrary, a high layer size may lead to overfitting as the model is more capable of "memorizing" the input data, including noise.

At this point, you might have guessed: we will use the script from exercise 1 :)
This time you will pass a value to the `--encoder` (`-edim`) argument. Similar to before, we provide pre-trained models of the encoder so that you do not have to train it yourself. Hence, you can use only the following values:

-  `8`
-  `32`
-  `128` (default)

Here is an example command (will output to `./_output/exercise_4/3-13-128-128-100/`):

&nbsp;&nbsp;&nbsp;&nbsp;`python generate.py -edim 32 -i "../_input/exercise_4/" -o "../_output/exercise_4/" --pipeline_script "../../example_scripts/pipeline.py"`

Time for you to see how your generated gestures are affected by the encoder hidden layer size!

*Tip: Look at the how expressive the gestures are in terms of speed and location. Are these similar for the whole duration, or do they vary? What about temporal synchrony with the speech?*

## Exercise 5 : Play with the dataset size

In the previous exercises you used pre-trained models of the autoencoder and encoder components of Audio2Gestures. To train them, we used a [modified version](https://zenodo.org/record/6998231) of Meta's Talking With Hands dataset ([official page](https://research.facebook.com/file/1329572740884228/Talking-With-Hands-16.2M-A-Large-Scale-Dataset-of-Synchronized-Body-Finger-Motion-and-Audio-for-Conversational-Motion-Analysis-and-Synthesis-v2.pdf)) which was developed for the [GENEA Challenge 2022](https://youngwoo-yoon.github.io/GENEAchallenge2022/). It is well known that the generalization ability of deep learning models is affected by the amount of data used for training them. If the data is too little, the model cannot "see the bigger picture", and may overfit to the few data samples it is presented with. In our case, this could lead to repetitive gestures. Using more data will expose the model to a broader range of values to learn from, which should make generated gesture more varyin and fitting to the speech.

Your task is to experiment with the amount of data, and to observe how much the gestures are affected. For this, we once again revisit our beloved script from exercise 1. This time you will pass a value to the `--data_size` (`-data`) argument which relates to the amount of data (in %) which was used when pretraining the Audio2Gestures model. Your options are:

-  `33`
-  `100` (default)

Here is an example command (will output to `./_output/exercise_5/3-13-32-128-33/`):

&nbsp;&nbsp;&nbsp;&nbsp;`python generate.py -data 33 -i "../_input/exercise_5/" -o "../_output/exercise_5/" --pipeline_script "../../example_scripts/pipeline.py"`

Let's see... Does changing the data size affect the generated gestures significantly?

*Tip: Similar to prior exercises, look at gesture expressivity in terms of speed and location, as well as temporal synchrony with the speech.*

## Exercise 6 : Try the model on different audio

Finally, it is important to think about how a model trained on real-world data performs when presented with data that does not fall in the original domain of the data.

Q: Does this matter?
A: Well, I am glad you asked. In our case, the Audio2Gestures model was trained on real speech, but we are using it with synthetic audio when generating gestures. Even if the model performs well on unseen real-world data, it may not perform well on data which is in some ways dissimilar from the one used during training.

Your task is the check if the model differs noticeably in quality when generating gestures for real speech versus synthetic speech. At this point, you might have noticed an interesting pattern: we will use the script from exercise 1 (sorry!).

This time there we do not need to change anything about the script, except the input and output directory. The `exercise_6` directory contains 3 audio files of synthetic speech, and 2 of real speech from YouTube. Generate corresponding gestures with the following command (will output to `./_output/exercise_6/3-13-32-128-100/`):

&nbsp;&nbsp;&nbsp;&nbsp;`python generate.py -i "../_input/exercise_6/" -o "../_output/exercise_6/" --pipeline_script "../../example_scripts/pipeline.py"`

Take a look at the differences in gesture expessivity between real and synthetic speech now.

*Tip: You can also experiment with your own audio files. What happens if you record your own voice? Speak in a different language? What about using audio without speech, but other sounds instead?*

## Bonus Exercise : Using real speech for exercises 2-5

Nice! You completed the exercises above! Now, do you happen to have extra time, and wish to know more about the capabilities of Audio2Gestures? Well, why not repeat exercises 2-5, but this time using real audio as opposed to synthetic? For this, you can use these saples from Exercise 6: `real_Andrew_Ng_Future_Forum_Youtube.wav` and `real_David_Laude_TEDx_Youtube.wav`

Is there a difference in results between real and synthetic speech, when varying the model parameters?

Have a great day :)

[Back to top](#subsystem-3-gesture-generation)

