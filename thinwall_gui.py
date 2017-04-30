from Tkinter import *
import tkFileDialog
import PIL.Image
import PIL.ImageTk
import thinwall
import webbrowser

def makeParameter(frame, label, units, default, row):
    v = StringVar(frame, value=default)
    Label(frame, text=(label + ":"), fg="black", anchor=E).grid(row=row, column=0, padx=(5,0), pady=(5,5), sticky=W+E)
    textBox = Entry(frame, textvariable=v)
    textBox.grid(row=row, column=2, pady=(5,5))
    Label(frame, text=(units), fg="black", anchor=W).grid(row=row, column=3, pady=(5,5), sticky=W+E)
    return v

def makeMultiParameter(frame, label, labels, units, defaults, row):
    assert(len(units) == len(labels))
    assert(len(labels) == len(units))

    entries = dict()

    Label(optionsFrame, text=label + ":", width=15, fg="black", anchor=E).grid(row=row, column=0, padx=(5,0), pady=(5,0), sticky=W+E)

    for (l, u, d) in zip(labels, units, defaults):
        v = StringVar(frame, value=d)
        Label(frame, text=l+ ":", fg="black").grid(row=row, column=1, pady=(5,5))
        textBox1 = Entry(frame, textvariable=v)
        textBox1.grid(row=row, column=2, pady=(5,5))
        textBox1.text = d
        Label(frame, text=u, fg="black", anchor=W).grid(row=row, column=3, pady=(5,5), sticky=W+E)
        entries[l] = v
        row = row + 1

    return entries

def makeButton(frame, label, row, callback):
        btn_generate = Button(frame, text=label, fg="black", command=callback)
        btn_generate.grid(row=3, column=0, columnspan=4, padx=5, pady=(5, 5), sticky=N+S+E+W)

class openFileDialog():
    def __init__(self, frame, label, default, row):
        self.filename = default
        label = Label(frame, text=(label + ":"), anchor=E).grid(row=row, column=0, sticky=E+W)
        self.fileLabel = Label(frame, text=default, bg="white", width=20)
        self.fileLabel.grid(row=row,column=1,columnspan=2, sticky=E+W)
        btn_generate = Button(frame, text="Browse...", fg="black", command=self.browseForFile).grid(row=row, column=3, padx=5, pady=5, sticky=E+W)
    def browseForFile(self):
        self.filename = tkFileDialog.asksaveasfilename()
        self.fileLabel.config(text=self.filename)
    def get(self):
        return self.filename

def mapEntriesToValues(rawEntries):
    values = dict()
    for k in rawEntries:
        if isinstance(rawEntries[k], dict):
            values[k] = mapEntriesToValues(rawEntries[k])
        else:
            values[k] = rawEntries[k].get()
    return values

def generateToolpath(rawEntries):
    parameterValues = mapEntriesToValues(rawEntries)
    thinwall.generate(parameterValues)
    webbrowser.open(parameterValues['outputFile'])
    
entries = dict()

root = Tk()

root.iconbitmap(default='favicon.ico')
root.wm_title("Thinwall Deposit Toolpath Generator")

optionsFrame = Frame(root)
optionsFrame.pack(side=LEFT, fill="both", expand="true", padx=20, pady=20)
imageFrame = Frame(root)
imageFrame.pack(side=LEFT, fill="both", expand="true", padx=20, pady=20)

im = PIL.Image.open("thinwall.png")
photo = PIL.ImageTk.PhotoImage(im)
label = Label(imageFrame, image=photo)
label.image = photo
label.pack(side=TOP, fill="both", expand=1, padx=20, pady=20)
commandFrame = Frame(imageFrame)
commandFrame.pack(side=BOTTOM, fill="x")
for c in range(4):
    Grid.columnconfigure(commandFrame, c, weight=1)

entries["outputFile"] = openFileDialog(commandFrame, "Output File", "output.ngc", 2)
makeButton(commandFrame, "Generate Toolpath", 3, lambda:generateToolpath(entries))

entries["length"] = makeParameter(optionsFrame, "Length", "in", "1.0", 0)
entries["height"] = makeParameter(optionsFrame, "Height", "in", "0.5", 1)
entries["startPosition"] = tb_startPositionY = makeMultiParameter(optionsFrame, "Start Position", ("X", "Y", "Z"), ("in", "in", "in"), ("0.0", "0.0", "0.0"), 2)
entries["scanAngle"] = makeParameter(optionsFrame, "Scan Angle", "degrees", "0.0", 5)
entries["scansPerLayer"] = makeParameter(optionsFrame, "Scans per Layer", "", "3", 6)
entries["firstLayerLaserPower"] = makeParameter(optionsFrame, "First-Layer Laser Power", "Watts", "600", 7)
entries["laserPower"] = makeParameter(optionsFrame, "Laser Power", "Watts", "300", 8)
entries["feedrate"] = makeParameter(optionsFrame, "Feed Rate", "in/min", "10", 9)
entries["layerHeight"] = makeParameter(optionsFrame, "Layer Height", "in", "0.01", 10)
entries["extensionDistance"] = makeParameter(optionsFrame, "Extension Distance", "in", "0.2", 11)

mainloop()

