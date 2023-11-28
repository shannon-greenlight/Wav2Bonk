# Wav2Bonk
GUI wav to Bonkulator waveform converter.
This program converts mono .wav files into a csv format text file that is compatible with the Greenface Labs Bonkulator.
The length of the input .wav file is limited to 2048.
Wav2bonk.py can be invoked from the command line by typing: python wav2bonk.py

Wav2bonk.py requires pandas and scipy. Install these using your preferred method.

In Windows, you can use:

python -m pip install scipy

python -m pip install pandas

python must be in the computer's PATH for this to work. wav2bonk.bat is provided as a convenience to Windows users. This also requires that python be in the user's PATH.

Wav2bonk.py has a file browser that lets you select the input .wav file. Once selected, wav2bonk.py converts the contents to a text file with the same basename as the .wav file and saves that to the "out" folder as well as copying the data to the clipboard.
Once the data is in the clipboard (either directly as described, or by copying the contents of the text file) you can paste it into the text area in the bonkulator control app while the Bonkulator is in the User Waverform function.

The folder "wavfile" is the default path for the file browser. It contains a few example .wav files. You can put your favorite .wave files here if desired.

