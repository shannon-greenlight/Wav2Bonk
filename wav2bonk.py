import sys, os, os.path
from scipy.io import wavfile
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile
from tkinter.ttk import *
root = Tk()
window_height = 600
window_width = 400
root.geometry(f'{window_height}x{window_width}')
root.configure(background='#aaaaaa')
root.title('Greenface Labs Wav2Bonk')

input_filename = 'none'

def fileDialog():
  infile = askopenfile(mode='r', filetypes=[("Wav files", "*.wav")], initialdir='./wavfile')
  input_filename = infile.name
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

  if len(wavData.columns) == 2:
      print('Stereo .wav file not supported!\n')
      sys.exit()

  elif len(wavData.columns) == 1:
      #print('Loaded mono .wav file: '+input_filename)
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
      #print('Save is done to: ' + output_filename + " Length: " + str(i))
      display_text.set('Saved: ' + output_filename + " Length: " + str(i))
      #the_label.cget("text") = 'Save is done to: ' + output_filename + " Length: " + str(i)

  else:
      print('Multi channel .wav file not supported!\n')
      sys.exit()


screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

style = ttk.Style()
style.configure("BW.Frm", foreground="red", background="white")

s = ttk.Style()
s.configure('Danger.TFrame', background='#9999ff', borderwidth=5, anchor="center", relief='sunken')

frm = ttk.Frame(root, padding=10, style='Danger.TFrame')
frm.pack(pady=20)

display_text = tk.StringVar()
display_text.set("Greenface Labs .wav to Bonkulator.")
the_label = ttk.Label(frm, textvariable=display_text, font="verdana 16", background="#444444", foreground="white").pack()

the_button = ttk.Button(frm, text="Select File", command=fileDialog).pack(pady=10)
exit_button = ttk.Button(frm, text="Done", command=root.destroy).pack(pady=10)

#the_button.text = "Done"
#the_button.command = root.destroy

#infile = askopenfile(mode='r', filetypes=[("Wav files", "*.wav")], initialdir='./wavfile')
#input_filename = infile.name
#root.mainloop()


root.mainloop()
