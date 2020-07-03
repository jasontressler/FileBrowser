import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Event import Event
import os


class LazyTree(object):
    def __init__(self, master):
        self.OnSelectionChanged = Event()
        self.nodes = dict()
        self.tree = ttk.Treeview(master, show='tree')
        ysb = ttk.Scrollbar(master, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)
        ysb.pack(fill=tk.BOTH, side=tk.RIGHT, expand=0)
        self.tree.pack(fill=tk.BOTH, side=tk.TOP, expand=1)

        abspath = ''
        self.tree.bind('<<TreeviewOpen>>', self.open_node)
        self.tree.bind('<<TreeviewSelect>>', self.get_node)

    def Subscribe(self, method):
        self.OnSelectionChanged += method

    def Unsubscribe(self, method):
        self.OnSelectionChanged -= method

    def get_node(self, event):
        node = self.tree.focus()
        abspath = self.nodes[node]
        self.OnSelectionChanged(abspath)

    def insert_node(self, parent, text, abspath):
        node = self.tree.insert(parent, 'end', text=text, open=False)
        if os.path.isdir(abspath):
            self.nodes[node] = abspath
            self.tree.insert(node, 'end')

    def open_node(self, event):
        node = self.tree.focus()
        abspath = self.nodes[node]
        #abspath = self.nodes.pop(node, None)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            try:
                for p in os.listdir(abspath):
                    self.insert_node(node, p, os.path.join(abspath, p))
            except PermissionError:
                messagebox.showerror(title='Access denied', message='Permission denied: could not open')

