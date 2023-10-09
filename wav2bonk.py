import sys, os, os.path
from scipy.io import wavfile
import pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile
root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
infile = askopenfile(mode='r', filetypes=[("Wav files", "*.wav")], initialdir='./wavfile')
input_filename = infile.name
root.mainloop()
print(input_filename)
parts = input_filename.split(".")
dirs = parts[0].split("/")
output_filename = "output/" + dirs[len(dirs)-1]+".txt"
print(output_filename)

samrate, data = wavfile.read(str(input_filename))
print(data)

wavData = pd.DataFrame(data)

wavData.columns = ['W']
input_len = len(wavData.W)
index = pd.date_range('1/1/2000', periods=input_len, freq='T')
#if input_len != 256:
    #print('WARNING!! Input File not 256 in length! Length: '+str(input__len))
    #sys.exit()

if len(wavData.columns) == 2:
    print('Stereo .wav file not supported!\n')
    sys.exit()

elif len(wavData.columns) == 1:
    print('Loaded mono .wav file: '+input_filename)
    #print('\n')
    f = open(output_filename, "w")
    f.write("w0,")
    
    wavData.index = index
    sf = input_len / 128
    # print(sf)
    wavData = (wavData.resample(str(sf)+'T').mean())
    # print(index)
    # print(wavData)
    
    i = 0
    for x in wavData.W:
      if i > 0:
        f.write(",")
      avg = (wavData.iloc[i].W)
      avg = avg + 32768
      avg = avg / 16
      avg = int(avg)
      f.write(str(avg))
      i = i + 1

    f.close()
    print('Save is done to: ' + output_filename + " Length: " + str(i))

else:
    print('Multi channel .wav file not supported!\n')
    sys.exit()

