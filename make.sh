#!/bin/sh
pyinstaller --onedir --hidden-import=pandas --hidden-import=scipy --add-data "wavfile:wavfile"  wav2bonk.py
zip -r wav2bonk.zip dist/wav2bonk