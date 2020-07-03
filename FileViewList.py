import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Event import Event
from pathlib import Path
from datetime import datetime, timezone
import os
import shutil

def convertSize(num):
    units = {
        0: 'bytes',
        1: 'KB',
        2: 'MB',
        3: 'GB',
        4: 'TB'
    }
    x = float(num)
    u = 0
    while (x > 1024):
        x /= 1024
        u += 1
    return (str(round(x,1))+'\ '+units[u])

def parseEntry(entry):
    info = entry.stat()
    if os.path.isdir(entry):
        value = 'dir '
    else:
        value = 'f '
    value += entry.name.replace(' ', '\ ') + ' '
    value += convertSize(info.st_size) + ' '
    value += datetime.fromtimestamp(info.st_mtime, timezone.utc).strftime('%Y/%m/%d\ %H:%M') + ' '
    value += entry.path.replace(' ', '\ ')
    return value

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, text=col, command=lambda _col=col: \
                 treeview_sort_column(tv, _col, not reverse))

class FileViewList(object):
    curPath = ''
    prevPath = ['']
    def __init__(self, master):
        self.OnSelectionChanged = Event()
        self.OnSelectionOpened = Event()
        self.nodes = dict()
        self.columns = ['#0', 'Name', 'Size', 'Modified', 'Path']
        self.tree = ttk.Treeview(master, columns=self.columns, show='headings')
        ysb = ttk.Scrollbar(master, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)
        ysb.pack(fill=tk.BOTH, side=tk.RIGHT, expand=0)
        xsb = ttk.Scrollbar(master, orient='horizontal', command=self.tree.xview)
        self.tree.configure(xscroll=xsb.set)
        xsb.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=0)
        self.tree.pack(fill=tk.BOTH, side=tk.TOP, expand=1)

        for col in self.columns:
            self.tree.heading(col, text=col, command=lambda _col=col: \
                              treeview_sort_column(self.tree, _col, False))
        self.tree.column('#0', width=5)
        abspath = 'C:/'

        self.tree.bind('<<TreeviewSelect>>', self.get_node)
        self.tree.bind('<Double-1>', self.open_node)

    def SubscribeSelect(self, method):
        self.OnSelectionChanged += method

    def UnsubscribeSelect(self, method):
        self.OnSelectionChanged -= method

    def SubscribeOpen(self, method):
        self.OnSelectionOpened += method

    def UnsubscribeOpen(self, method):
        self.OnSelectionOpened -= method

    def get_node(self, event):
        node = self.tree.focus()
        abspath = self.nodes[node]
        self.OnSelectionChanged(os.path.join(abspath,self.tree.item(node)['values'][1]))

    def open_node(self, event):
        node = self.tree.focus()
        path = self.nodes[node]
        abspath = os.path.join(path,self.tree.item(node)['values'][1])
        if os.path.isdir(abspath):
            self.insert_nodes(abspath)
            self.OnSelectionOpened(abspath)
        else:
            os.startfile(abspath)
            #subprocess.run(['open', abspath], check=True)

    def insert_nodes(self, path):
        node = self.tree.insert('', 'end', text='')
        if self.nodes != None:
            self.tree.delete(*self.tree.get_children())
        try:
            with os.scandir(path) as entries:
                if self.prevPath[-1] != self.curPath:
                    self.prevPath.append(self.curPath)
                for entry in entries:
                    node = self.tree.insert('', 'end', open=False, values=(parseEntry(entry)))
                    self.nodes[node] = path
            self.curPath = path
            self.OnSelectionOpened(path)
        # for x in self.prevPath:
        #     print(x)
        except PermissionError:
            messagebox.showerror(title='Access denied', message='Permission denied: could not open')

    def back(self):
        if len(self.prevPath) > 1:
            self.insert_nodes(self.prevPath[-1])
            del self.prevPath[-1]
            del self.prevPath[-1]
            self.OnSelectionOpened(self.curPath)