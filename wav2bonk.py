import sys, os, os.path
from scipy.io import wavfile
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile
from tkinter.ttk import *
root = Tk()
window_height = 800
window_width = 250
root.geometry(f'{window_height}x{window_width}')
root.configure(background='#555566')
root.title('Greenface Labs Wav2Bonk')
root.clipboard_clear()

out_clip = ''
input_filename = 'none'

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

def print_info():
  print("Path at terminal when executing this file")
  print(os.getcwd() + "\n")

  print("This file path, relative to os.getcwd()")
  print(__file__ + "\n")

  print("This file full path (following symlinks)")
  full_path = os.path.realpath(__file__)
  print(full_path + "\n")

  print("This file directory and name")
  path, filename = os.path.split(full_path)
  print(path + ' --> ' + filename + "\n")

  print("This file directory only")
  print(os.path.dirname(full_path))

def write_data(data, outfile):
  global out_clip
  outfile.write(data)
  out_clip += data

def process_wav_data(input_filename,wavData):
    global out_clip
    parts = input_filename.split(".")
    dirs = parts[0].split("/")
    output_filename = "output/" + dirs[-1] + ".txt"

    output_dir = "output"
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)

    with open(output_filename, "w") as f:
        out_clip = ""
        write_data("w0,", f)

        input_len = len(wavData.W)
        index = pd.date_range('1/1/2000', periods=input_len, freq='T')
        wavData.index = index
        sf = input_len // 128
        wavData = wavData.resample(f'{sf}T').mean()

        for i, x in enumerate(wavData.W):
            if i > 0:
                write_data(",", f)
            out_val = (wavData.iloc[i].W + 32768) // 16
            write_data(str(int(out_val)), f)

    display_text2.set(f'Data copied to clipboard.\nSaved to: {output_filename}')
    root.clipboard_clear()
    root.clipboard_append(out_clip)
    
def fileDialog():
  infile = askopenfile(mode='r', filetypes=[("Wav files", "*.wav")], initialdir='./wavfile')
  if infile is not None:
    input_filename = infile.name
    print(input_filename)
    _, data = wavfile.read(str(input_filename))
    # print(data)

    wavData = pd.DataFrame(data)
    wavData.columns = ['W']
    input_len = len(wavData.W)

    if input_len <= 2048:
      if len(wavData.columns) == 2:
          display_text2.set('Stereo .wav file not supported!')
      elif len(wavData.columns) == 1:
          process_wav_data(input_filename,wavData)
      else:
          display_text2.set('Multi channel .wav file not supported!')
    else:
          display_text2.set('Wav file > 2048 in length!')

print_info()
s = ttk.Style()
s.configure('Danger.TFrame', background='#99aaff', borderwidth=5, anchor="center")

root.minsize(400, 400)  # Set a minimum size for the window
frm = ttk.Frame(root, padding=10, style='Danger.TFrame', height=600, width=500)
frm.pack(pady=30)

display_text1 = tk.StringVar()
display_text1.set("Greenface Labs")
the_label1 = ttk.Label(frm, textvariable=display_text1, font="verdana 14", background="#99aaff", foreground="green", anchor="center")
the_label1.pack()

display_text2 = tk.StringVar()
display_text2.set("Wav to Bonkulator")
the_label2 = ttk.Label(frm, textvariable=display_text2, font="verdana 18", background="#99aaff", foreground="#330044", anchor="center")
the_label2.pack(pady=(5,10))

# Define a style for the buttons
btn_style = ttk.Style()
btn_style.configure('TButton',
          font=('verdana', 12),
          foreground='black',
          background='#99aaff',
          borderwidth=1)

# Apply the style when creating the buttons
the_button = ttk.Button(frm, text="Select File", command=fileDialog, style='TButton').pack(pady=10)
from tkinter import messagebox

# Define the function that will be called when the button is pressed
def show_help():
  messagebox.showinfo("Help", """Wav2Bonk v2.0.0

Select a .wav file to convert to Bonkulator format.
The .wav file must be 16 bit, mono, and less than 2049 values.
Example .wav files are found in the 'wavfile' folder.

The converted data will be copied to the clipboard.
The converted data will also be saved to a text file in the output folder.
The text file will have the same name as the .wav file.

The text file can also be opened in a spreadsheet program.

The data can then be imported into the Bonkulator using either the desktop app or the web app.

The Bonkulator can be found at https://greenfacelabs.com/bonkulator
""")

help_button = ttk.Button(frm, text="Help", command=show_help, style='TButton')
help_button.pack(pady=10)
exit_button = ttk.Button(frm, text="Done", command=root.destroy, style='TButton').pack(pady=10)
root.mainloop()
