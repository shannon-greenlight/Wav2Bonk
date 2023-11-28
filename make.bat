pyinstaller --onefile --hidden-import=pandas --hidden-import=scipy --add-data "wavfile;wavfile" --add-data "output;output" wav2bonk.py
