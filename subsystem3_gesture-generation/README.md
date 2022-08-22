# Subsystem 3: Gesture Generation

- [Exercise 1 : Setup and get the base model to work](#exercise-1--setup-and-get-the-base-model-to-work)
  * [Interacting with Audio2Gestures](#interacting-with-audio2gestures)
  * [Generating gestures](#generating-gestures)
  * [Visualizing gestures](#visualizing-gestures)
- [Exercise 2 : Explore smoothing parameters](#exercise-2--explore-smoothing-parameters)
- [Exercise 3 : Explore representation dimensionality of the AE](#exercise-3--explore-representation-dimensionality-of-the-ae)
- [Exercise 4 : Explore the hidden layer size of the encoder](#exercise-4--explore-the-hidden-layer-size-of-the-encoder)
- [Exercise 5 : Play with the dataset size](#exercise-5--play-with-the-dataset-size)
- [Exercise 6 : Try the model on different audio](#exercise-6--try-the-model-on-different-audio)
- [Bonus Exercise : Using synthetic audio for exercises 2-5](#bonus-exercise--using-synthetic-audio-for-exercises-2-5)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

---

Note: Before continuing, make sure that you have followed the [installation instructions](https://github.com/TeoNikolov/wasp-2022-summer-school#Installation) first.

## Exercise 1 : Setup and get the base model to work

### Interacting with Audio2Gestures
The gesture generation subsystem implements a single gesture model called `Audio2Gestures`. This model is located in `./subsystem3_gesture-generation/networks/Audio2Gestures/`, and is maintained in a separate [GitHub repository](https://github.com/teonikolov/Speech_driven_gesture_generation_with_autoencoder/tree/GENEA_2022) (a fork of the [original repository](https://github.com/genea-workshop/Speech_driven_gesture_generation_with_autoencoder/tree/GENEA_2022) by [Taras Kucherenko](https://github.com/Svito-zar)).

This model uses Docker to automate the process of setting up a working environment, which means that we need to open a shell inside the corresponding Docker container to interact with Audio2Gestures. First, get the container ID of the Audio2Gestures Docker container, by writing `docker ps` and copying the container ID of the one for which `IMAGE` is `"wasp-gg"`. Then, execute the following (replacing `<container_ID>` with the ID you found):

&nbsp;&nbsp;&nbsp;&nbsp;`docker exec -it <container_ID> /bin/bash`

Your terminal is now inside the Docker container. There are several local folders that are mounted in the container, so that their files can be accessed. They are:

- `./data/` in `/app/wasp/data/`
	- contains data files such as raw audio
- `./scripts/` in `/app/wasp/scripts/`
	- contains scripts that automate various tasks
- `./subsystem3_gesture-generation/models/` in `/app/wasp/models/`
	- contains pre-trained Audio2Gestures models
- `./subsystem3_gesture-generation/dataset/` in `/app/wasp/dataset/`
	- contains metadata of the dataset used to pre-train Audio2Gestures

### Generating gestures

The next part of the exercise is to familiarize yourself with the generation procedure. For this, we will predict gestures for files inside `./data/subsystem3_exercises/exercise_1/`. For this purpose, you should use the supplied `./scripts/generate_gestures.py` script. Navigate to the location in the Docker container using `cd /app/wasp/scripts/` and then run:

&nbsp;&nbsp;&nbsp;&nbsp;`python "generate_gestures.py" -i "../data/subsystem3_exercises/exercise_1/" --pipeline_script "../../example_scripts/pipeline.py"`

- `-i` is a directory with input `.wav` raw audio files to predict gestures for
- `-o` is a directory where generated `.bvh` files will be saved to (defaults to value of `-i`)
- `--pipeline_script` points to the location of the `pipeline.py` script, which is responsible for invoking low-level functions of the Audio2Gestures model

After calling the script, you will see files popping up inside `./data/subsystem3_exercises/exercise_1/3-13-32-128-100/`. These files are the input `.wav` file, output `.bvh` file, as well as intermediate files used by the gesture model. The output directory `3-13-32-128-100/` is created to help you organize generated files. This will come in handy for the next exercises, as you will be modifying various parameters when running `generate_gestures.py`. The folders use the following naming convention:

&nbsp;&nbsp;&nbsp;&nbsp;`{1}_{2}_{3}_{4}_{5}`

1. Savitsky-Golay polynomial order
1. Savitsky-Golay window size
1. Representation dimensionality of the autoencoder
1. Hidden layer size of the encoder
1. Size of data in % on which Audio2Gestures was trained on

You will learn about the above topics in the exercises below.

*Tip: Open `generate_gestures.py` in your favorite text editor, and take a peek at the code inside!*
*Tip 2: The `generate_gestures.py` script processes all `.wav` files in the input directory. Having your audio files in the same directory allows you to process them in batch with a single command!*

### Visualizing gestures

The above steps lead you to obtaining animation data in the form of `.bvh` files. Next, you will visualize the animation data with a 3D avatar in order to subjectively evaluate the quality of the generated gesture motion. For this, Blender is used to retarget the animation data onto various 3D avatars, which can then be exported in either a `.mp4` video format, or a standard `.fbx` 3D data format (with `.mp4` being better for fast iterations, and `.fbx` being a requirement for use in Unreal Engine). For this, you will use the provided `./scripts/visualize_gestures.py` script which interacts with Blender. *Make sure to note down the location of your Blender executable first, as you will need it.*

To visualize videos, [code for GENEA Challenge 2022](https://github.com/TeoNikolov/genea_visualizer/) is used that includes a prototype avatar. Knowing your `<blender_executable>` path, you can render a video with the following command (in my case, it was `"C:/Program Files (x86)/Steam/steamapps/common/Blender/blender.exe"`):

&nbsp;&nbsp;&nbsp;&nbsp;`python .\visualize_gestures.py --blender_exe "<blender_executable>" -i "../data/subsystem3_exercises/exercise_1/3-13-32-128-100/" --mp4`

The process is very similar for exporting `.fbx` data, which is a matter of changing `--mp4` to `--fbx` as such:

&nbsp;&nbsp;&nbsp;&nbsp;`python .\visualize_gestures.py --blender_exe "<blender_executable>" -i "../data/subsystem3_exercises/exercise_1/3-13-32-128-100/" --fbx`

<p align="center">
  <img src="https://github.com/TeoNikolov/wasp-2022-summer-school/blob/main/subsystem4_visualization/avatars.png" alt="the 4 avatars">
  <br>
  <i>The 4 avatars</i>
</p>

Lastly, you can modify which avatar is used when exporting `.fbx` files. You have four options:

- `Majken`
- `Leffe`
- `Lea`
- `Harold`

To specify the avatar, pass the `--avatar` argument, and set its value to one of the above. For example with `Leffe`:

&nbsp;&nbsp;&nbsp;&nbsp;`python .\visualize_gestures.py --blender_exe "<blender_executable>" -i "../data/subsystem3_exercises/exercise_1/3-13-32-128-100/" --fbx --avatar "Leffe"`

*Tip: For quick visualizations, it is better to use `.mp4` over `.fbx` as it is faster to export.*
*Note: You can specify both `--mp4` and `--fbx` flags to export both file formats.*

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

Here is an example command (outputs to `./data/subsystem3_exercises/exercise_2/2-5-32-128-100`):

&nbsp;&nbsp;&nbsp;&nbsp;`python "generate_gestures.py" -i "../data/subsystem3_exercises/exercise_2/" --pipeline_script "../../example_scripts/pipeline.py" -spo 2 -sws 5`

Now modify the parameters, and see how your generated gestures are affected by the smoothing filter!

**Reminder: Remember to visualize the data as you did for Exercise 1!**

*Tip: Observe at which point the values start to lead to under-smoothed or over-smoothed motion!*

## Exercise 3 : Explore representation dimensionality of the AE

Next, you should explore how changing the representation dimensionality of the autoencoder in Audio2Gestures affects the gestures. Theoretically, a small dimensionality forces the autoencoder to compress the high-dimensional input data into fewer dimensions. This can improve the data by excluding irrelevant details about the original representation, which are not useful for generalization. On the contrary, over-compression can lead to poor generalization because important information may get lost in the process.

As before, we will use the script from exercise 1, but this time you will pass a value to the `--autoencoder` (`-aedim`) argument. Since we provide pre-trained autoencoder models (doing this yourself can take a *long* time, trust me), you can use only the following values:

-  `8`
-  `32` (default)
-  `128`
-  `512`

Here is an example command (outputs to `./data/subsystem3_exercises/exercise_3/3-13-128-128-100/`):

&nbsp;&nbsp;&nbsp;&nbsp;`python "generate_gestures.py" -i "../data/subsystem3_exercises/exercise_3/" --pipeline_script "../../example_scripts/pipeline.py" -aedim 128`

Go ahead, see how your generated gestures are affected by the autoencoder dimensionality!

**Reminder: Remember to visualize the data as you did for Exercise 1!**

*Tip: Look at the how expressive the gestures are in terms of speed and location. Are these similar for the whole duration, or do they vary?*

## Exercise 4 : Explore the hidden layer size of the encoder

This exercise is very similar to exercise 3, but instead of varying the dimensionality of the autoencoder, you will vary the dimensionality of the Audio2Gestures encoder. The encoder maps audio features to motion features, and the size of its hidden layers directly affects its capacity to generalize to input data. Theoretically, a small layer size will lack the capacity to learn from input data, leading to underfitting. On the contrary, a high layer size may lead to overfitting as the model is more capable of "memorizing" the input data, including noise.

At this point, you might have guessed: we will use the script from exercise 1 :)
This time you will pass a value to the `--encoder` (`-edim`) argument. Similar to before, we provide pre-trained models of the encoder so that you do not have to train it yourself. Hence, you can use only the following values:

-  `8`
-  `32`
-  `128` (default)

Here is an example command (outputs to `./data/subsystem3_exercises/exercise_4/3-13-32-32-100/`):

&nbsp;&nbsp;&nbsp;&nbsp;`python "generate_gestures.py" -i "../data/subsystem3_exercises/exercise_4/" --pipeline_script "../../example_scripts/pipeline.py" -edim 32`

Time for you to see how your generated gestures are affected by the encoder hidden layer size!

**Reminder: Remember to visualize the data as you did for Exercise 1!**

*Tip: Look at the how expressive the gestures are in terms of speed and location. Are these similar for the whole duration, or do they vary? What about temporal synchrony with the speech?*

## Exercise 5 : Play with the dataset size

In the previous exercises you used pre-trained models of the autoencoder and encoder components of Audio2Gestures. To train them, we used a [modified version](https://zenodo.org/record/6998231) of Meta's Talking With Hands dataset ([official page](https://research.facebook.com/file/1329572740884228/Talking-With-Hands-16.2M-A-Large-Scale-Dataset-of-Synchronized-Body-Finger-Motion-and-Audio-for-Conversational-Motion-Analysis-and-Synthesis-v2.pdf)) which was developed for the [GENEA Challenge 2022](https://youngwoo-yoon.github.io/GENEAchallenge2022/). It is well known that the generalization ability of deep learning models is affected by the amount of data used for training them. If the data is too little, the model cannot "see the bigger picture", and may overfit to the few data samples it is presented with. In our case, this could lead to repetitive gestures. Using more data will expose the model to a broader range of values to learn from, which should make generated gesture more varyin and fitting to the speech.

Your task is to experiment with the amount of data, and to observe how much the gestures are affected. For this, we once again revisit our beloved script from exercise 1. This time you will pass a value to the `--data_size` (`-data`) argument which relates to the amount of data (in %) which was used when pretraining the Audio2Gestures model. Your options are:

-  `33`
-  `100` (default)

Here is an example command (outputs to `./data/subsystem3_exercises/exercise_5/3-13-32-128-33/`):

&nbsp;&nbsp;&nbsp;&nbsp;`python "generate_gestures.py" -i "../data/subsystem3_exercises/exercise_5/" --pipeline_script "../../example_scripts/pipeline.py" -data 33`

Let's see... Do you think changing the data size affects the generated gestures?

**Reminder: Remember to visualize the data as you did for Exercise 1!**

*Tip: Similar to prior exercises, look at gesture expressiveness in terms of speed and location, as well as temporal synchrony with the speech.*

## Exercise 6 : Try the model on different audio

Finally, it is important to think about how a model trained on real-world data performs when presented with synthetic data.

Q: Does this matter?
A: Well, I am glad you asked. In our case, the Audio2Gestures model was trained on real speech, but we are using it with synthetic audio when generating gestures. Even if the model performs well on unseen real-world data, it may not perform well on data which is in some ways dissimilar from the one used during training.

Your task is the check if the model differs noticeably in quality when generating gestures for real speech versus synthetic speech. At this point, you might have noticed an interesting pattern: we will use the script from exercise 1 (sorry!).

This time, we do not need to change anything about the script, except the input directory. The `./data/subsystem3_exercises/exercise_6/` contains 3 audio files of synthetic speech, and 2 of real speech from YouTube. You should generate the corresponding gestures via the following command (outputs to `./data/subsystem3_exercises/exercise_6/3-13-32-128-100/`):

&nbsp;&nbsp;&nbsp;&nbsp;`python "generate_gestures.py" -i "../data/subsystem3_exercises/exercise_6/" --pipeline_script "../../example_scripts/pipeline.py"`

Take a look at the differences in gesture expressiveness between real and synthetic speech now.

**Reminder: Remember to visualize the data as you did for Exercise 1!**

*Tip: You can also experiment with your own audio files. What happens if you record your own voice? Speak in a different language? What about using audio without speech, but other sounds instead? What if you play dubstep?*

## Bonus Exercise : Using synthetic audio for exercises 2-5

Awesome! You completed all exercises!

Do you happen to have extra time, and wish to learn more about what Audio2Gestures is capable of? Well, why not repeat exercises 2-5, but this time instead of using real audio, you use synthetic one? For this, you can use samples from Exercise 6 (just copy-paste them in the Exercise # folders) and run the corresponding scripts:
- `synthetic_Quentin_Tarantino.wav` 
- `synthetic_Scottish.wav`
- `synthetic_Welcome.wav`

What is interesting to see here is if changing the various generation parameters will yield similar differences in results when using synthetic audio versus real audio. Maybe the model performs well on real data when the encoder hidden layer size is high, but not so much when using synthetic data?

Go ahead, and see for yourself!

**Reminder: Remember to visualize the data as you did for Exercise 1!**

---

[Back to top](#subsystem-3-gesture-generation)

