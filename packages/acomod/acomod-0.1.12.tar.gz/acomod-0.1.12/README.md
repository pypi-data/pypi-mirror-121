# Acoustic Modes Viewer

This program is a simple viewer of power spectral density of sounds recorded either from 
microphone or played from .wav files. 
The package provides a module and a program to trace Fourier acoustic modes 
and resonance frequencies of excited bodies.

## Use cases
* estimate length of an excited metal bar, or 
* measure frequency of flute tones, 
* identify resonance frequencies and through provided sound speed the corresponding length scales of mechanical components that generate unwanted resonances (e.g. in a car as a function of speed cs)
* test 1/f noise and microphonic effects in electrical devices the program runs on.


## Features
* Analysis of sound from microphone or from a file (WAV format)
* In order to analyze transient signals, the program keeps track of peaks detected in the instantaneous power spectra 
* Saves recorded and processed data to files for further analysis
* Outputs list of peak frequencies (f) and associated wavelengths (l=cs/f)

## Installation

### Virtualenv installation with pip

```sh
python3 -m venv venv
source venv/bin/activate
pip install acomod
```

### From sources (Ubuntu 20.04 LTS)

```sh
sudo apt install libportaudio2/focal
python3 -m venv venv
source venv/bin/activate
git clone https://github.com/bslew/acomod.git
cd acomod
pip install -r requirements.txt
python setup.py build
python setup.py install
```

### Run
```sh
acoustic_mode_viewer
```


#### Note
You may need to specify the LD_LIBRARY_PATH environment variable to point to the location where appropriate Qt libraries can be found. Let's store these settings in your virtual environment activaton script.

```sh
$ echo 'LD_LIBRARY_PATH='`find "$VIRTUAL_ENV" -name "*libQt5Core.so.5*" -exec dirname "{}" \;`:$LD_LIBRARY_PATH >> venv/bin/activate
```



## Screenshots

![Screenshot](screenshot.png)

![Screenshot](https://github.com/bslew/acomod/blob/master/screenshot.png)

## Examples

### Loading and playing wav files
The program comes with a set of examples stored in "data" folder.
After starting the program just go to: File>Open File... (or Ctrl-o), 
go to src/acomod/data/ and select
a wav file. Press play (or Ctrl-p) to start calculating and plotting power spectra on 
sections of the wav file of length specified in the "Record Length" box. 
(The sound is not played). Peaks 
for each partial spectra can also be shown as specified by 
Npeaks window. The maximal values in each mode can also be over-plotted in red
(View>Plot Maximal Values, or Ctrl-m). If the wav file length fits within the recording
length the two plots are be identical. Similarly, the average spectrum can be toggled 
by pressing Ctrl-a.

Press "Play" again (ctrl-p) to stop/start calculating power spectrum in the background.

### Browsing the modes
Use left or right arrows to loop over Npeaks modes in the power spectra and check their
respective frequencies (and corresponding wavelengths). You may need to focus on the plot
window first (Ctrl-g). 

### Toggling axes

Use Ctrl-l and Ctrl-k to toggle between logarithmic and linear axes.

### Recording new data

New sounds can be recorded by pressing Crtl-r. The recording can be latter saved as wav file.
As in case of "playing" mode, the spectra are calculated using recording lengths as specified
in the "Record Length" box and the plots are updated on every newly calculated spectra.


## Troubleshooting
##### 	**acoustic_mode_viewer gives core dump on start**

When you pip3 install acomod in virtual environment or locally via --user option Qt platform plugin may fail to be properly initialized due to incorrect configuration of LD_LIBRARY_PATH environment variable (under Linux) and pointing locations of Qt libraries installed most likely somewhere in the system directories. If the version of those is not the one required by the PyQt5 the program will fail with

	"This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.",
	
a message that typically is not even printed out to the terminal.

**Solution**:
		Provide the correct path to the Qt shared libraries: e.g.
				
```sh
$ export LD_LIBRARY_PATH=`find ./venv -name "*libQt5Core.so.5*" -exec dirname '{}' \;`:$LD_LIBRARY_PATH
```

or in case of `pip install acomod --user`
				
```sh
$ export LD_LIBRARY_PATH=`find $HOME/.local -name "*libQt5Core.so.5*" -exec dirname '{}' \;`:$LD_LIBRARY_PATH
```


## Authors
Bartosz Lew (bartosz.lew@protonmail.com)
