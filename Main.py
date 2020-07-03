import tkinter as tk
from tkinter import ttk
from LazyTree import LazyTree
from FileViewList import FileViewList as FL
from PIL import ImageTk, Image
import pymsgbox
import shutil
import os

### Global vars ###
currentDir = ''
selectedDir = ''
copyDir = ''
cut = False


### Global funcs ###
def doNothing():
    pass


def newFile():
    name = pymsgbox.prompt('Enter new file name')
    if name != '' and name != None:
        with open(os.path.join(currentDir, name), 'w') as new:
            pass
        explorer.insert_nodes(currentDir)


def newDir():
    name = pymsgbox.prompt('Enter new folder name')
    if name != '' and name != None:
        os.mkdir(os.path.join(currentDir, name))
        explorer.insert_nodes(currentDir)


def delObject(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)
    explorer.insert_nodes(currentDir)


def copyObject(isCut = False):
    global copyDir
    global cut
    cut = False
    copyDir = selectedDir
    cut = isCut


def navBack():
    explorer.back()


def navUp():
    if len(currentDir) > 3:
        path = currentDir.replace(currentDir.rsplit('\\')[-1], '')[0:-1]
        if len(path) < 3:
            path += '\\'
        explorer.insert_nodes(path)


def pasteObject():
    shutil.copy(copyDir, currentDir)
    global cut
    if cut:
        delObject(copyDir)
        cut = False;
    explorer.insert_nodes(currentDir)


def setCurrent(path):
    global currentDir
    # if len(path) == 2:
    #     path += '\\'
    currentDir = path
    entPath.delete(0,tk.END)
    entPath.insert(0, currentDir)


def setSelected(path):
    global selectedDir
    selectedDir = path


def printPath(path):
    print(path)


### Setup ###
root = tk.Tk()
root.title('File Explorer')
style = ttk.Style(root)
style.configure('Treeview', indent=10)


### Menu bar ###
menu = tk.Menu(root)

## File Menu
menuFile = tk.Menu(menu, tearoff = 0)
menuFile.add_command(label='New File', command=newFile)
menuFile.add_command(label='New Folder', accelerator="Ctrl+N", command=newDir)
menuFile.add_separator
menuFile.add_command(label='Close', accelerator="Ctrl+Q", command=root.quit)
menu.add_cascade(label='File', underline=0, menu=menuFile)

## Edit Menu
menuEdit = tk.Menu(menu, tearoff = 0)
#menuEdit.add_command(label='Select All', command=doNothing)
menuEdit.add_command(label='Cut', accelerator="Ctrl+X", command=lambda: copyObject(True))
menuEdit.add_command(label='Copy', accelerator="Ctrl+C", command=copyObject)
menuEdit.add_command(label='Paste', accelerator="Ctrl+V", command=pasteObject)
menuEdit.add_command(label='Delete', accelerator="Delete", command=lambda: delObject(selectedDir))
menu.add_cascade(label='Edit', underline=0, menu=menuEdit)

## Help Menu
menuHelp = tk.Menu(menu, tearoff = 0)
menuHelp.add_command(label='About', command=doNothing)
menu.add_cascade(label='Help', underline=0, menu=menuHelp)

## Bindings
root.bind_all("<Control-n>", lambda self: newDir())
root.bind_all("<Control-X>", lambda self: copyObject(True))
root.bind_all("<Control-C>", lambda self: copyObject())
root.bind_all("<Control-V>", lambda self: pasteObject())
root.bind_all("<Delete>", lambda self: delObject(selectedDir))
root.bind_all("<Control-Q>", root.quit)
root.config(menu=menu)


### Main Window ###
main = tk.Frame(root, width=100, height=100)
main.pack(fill=tk.BOTH, expand=1)

## Tool Bar
toolBar = tk.Frame(main)
toolBar.pack(side=tk.TOP, fill=tk.X)
# Back
image = Image.open(r'img\back.png')
image = image.resize((30,30), Image.ANTIALIAS)
imgBack = ImageTk.PhotoImage(image=image)
btnBack = ttk.Button(toolBar, text='Back', image=imgBack, command=navBack)
btnBack.pack(side=tk.LEFT)
# Up
image = Image.open(r'img\up.png')
image = image.resize((30,30), Image.ANTIALIAS)
imgUp = ImageTk.PhotoImage(image=image)
btnUp = ttk.Button(toolBar, text='Up', image=imgUp, command=navUp)
btnUp.pack(side=tk.LEFT)
# Address bar
lblPath = tk.Label(toolBar, text='Path:', width=10, anchor=tk.E)
lblPath.pack(side=tk.LEFT)
entPath = ttk.Entry(toolBar)
entPath.pack(side=tk.LEFT, fill=tk.X, expand=1)

## View
pane = tk.PanedWindow(main, orient='horizontal', height=500)
pane.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
pane.configure(sashrelief=tk.RAISED)

## File Tree
frmTree = tk.Frame(
    master=pane,
    relief=tk.SUNKEN,
    borderwidth=2,
    background='white',
    width=150
)
tree = LazyTree(frmTree)
drives = [ chr(x) + ":\\" for x in range(65,90) if os.path.exists(chr(x)+":\\") ]
for drive in drives:
     tree.insert_node('', drive, drive)
pane.add(frmTree)

## Explorer
frmExp = tk.Frame(
    master=pane,
    relief=tk.SUNKEN,
    borderwidth=2,
    bg='white',
    width=300
)
pane.add(frmExp)
explorer = FL(frmExp);


### Events ###
tree.Subscribe(explorer.insert_nodes)
tree.Subscribe(setCurrent)
explorer.SubscribeSelect(setSelected)
explorer.SubscribeOpen(setCurrent)

root.mainloop()






