#!/usr/bin/env python
# -*- coding: utf-8 -*-

## @package mos_iv_plot
# Plot I/V curves of MOS transistors
#

from __future__ import print_function
from __future__ import division
import math,sys,time,os,shutil
from datetime import datetime
import array,copy
import ctypes
import socket
import argparse
import json
import numpy as np
import pandas as pd

if sys.version_info[0] < 3:
    import Tkinter as tk
    ttk = tk
else:
    import tkinter as tk
    from tkinter import ttk
import threading

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
try:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
except ImportError:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler # for the default matplotlib key bindings
from matplotlib.figure import Figure
from matplotlib.ticker import FormatStrFormatter
from matplotlib import artist

class CommonData:
    def __init__(self, pklFiles=[]):
        self.pklFiles = pklFiles
        self.datasetsParams = {}
        for f in self.pklFiles:
            self.datasetsParams[f] = self.get_dataset_parameters(f)
        self.dfm = None

    def get_dataset_parameters(self, fname):
        self.dfm = pd.read_pickle(fname)
        Ws = self.dfm.index.levels[0].tolist()
        Ls = self.dfm.index.levels[1].tolist()
        return {"Ws" : Ws, "Ls" : Ls}

    def load_dataset(self, name):
        self.dfm = pd.read_pickle(name)
        self.vgDelta = self.dfm.index.levels[2][1]
        self.vdDelta = self.dfm.index.levels[3][1]

class DataPanelGUI:

    ##
    # @param [in] dataFigSize (w, h) in inches for the data plots figure assuming dpi=72
    def __init__(self, master, cD, dataFigSize=(22, 12.5)):
        self.master = master
        self.cD = cD
        self.master.wm_title("MOS I/V curves")
        # appropriate quitting
        self.master.wm_protocol("WM_DELETE_WINDOW", self.quit)
        # File selection
        self.selectionFrame = ttk.Frame(self.master)
        self.selectionFrame.pack(side=tk.TOP, fill=tk.X)
        self.datasetNameVar = tk.StringVar()
        self.datasetNameVar.set(self.cD.pklFiles[0])
        self.cD.load_dataset(self.cD.pklFiles[0])
        self.datasetSel = ttk.OptionMenu(self.selectionFrame, self.datasetNameVar,
                                         self.cD.pklFiles[0], *self.cD.pklFiles,
                                         command=self.on_dataset_selection)
        self.datasetSel.grid(row=0, rowspan=2, column=0, sticky="sw")
        # W, L, Vstep slidebar
        self.W = self.cD.datasetsParams[self.datasetNameVar.get()]["Ws"][0]
        self.wVar = tk.IntVar()
        self.wVar.set(0)
        self.wLabelVar = tk.StringVar()
        self.wLabelVar.set(f"W = {self.W}")
        self.wLabel = ttk.Label(self.selectionFrame, textvariable=self.wLabelVar)
        self.wLabel.grid(row=0, column=1)
        self.wSlide = ttk.Scale(self.selectionFrame, orient=tk.HORIZONTAL, length=300,
                                from_ = 0,
                            to = len(self.cD.datasetsParams[self.datasetNameVar.get()]["Ws"]) - 1,
                                variable=self.wVar, command=self.on_wSlide)
        self.wSlide.grid(row=1, column=1, padx=10)
        #
        self.L = self.cD.datasetsParams[self.datasetNameVar.get()]["Ls"][0]
        self.lVar = tk.IntVar()
        self.lVar.set(0)
        self.lLabelVar = tk.StringVar()
        self.lLabelVar.set(f"L = {self.L}")
        self.lLabel = ttk.Label(self.selectionFrame, textvariable=self.lLabelVar)
        self.lLabel.grid(row=0, column=2)
        self.lSlide = ttk.Scale(self.selectionFrame, orient=tk.HORIZONTAL, length=300,
                                from_ = 0,
                            to = len(self.cD.datasetsParams[self.datasetNameVar.get()]["Ls"]) - 1,
                                variable=self.lVar, command=self.on_lSlide)
        self.lSlide.grid(row=1, column=2, padx=5)
        #
        self.Vstep = 10
        self.vstepVar = tk.IntVar()
        self.vstepVar.set(10)
        self.vstepLabelVar = tk.StringVar()
        self.vstepLabelVar.set(f"Vstep = {self.Vstep}")
        self.vstepLabel = ttk.Label(self.selectionFrame, textvariable=self.vstepLabelVar)
        self.vstepLabel.grid(row=0, column=3)
        self.vstepSlide = ttk.Scale(self.selectionFrame, orient=tk.HORIZONTAL, length=200,
                                    from_ = 1, to = 20,
                                    variable=self.vstepVar, command=self.on_vstepSlide)
        self.vstepSlide.grid(row=1, column=3, padx=5)
        #
        self.infoLabel = ttk.Label(self.selectionFrame,
                                   text = f"ΔVg = {self.cD.vgDelta}, ΔVd = {self.cD.vdDelta}")
        self.infoLabel.grid(row=0, column=4, padx=10, sticky="n")

        # frame for plotting
        self.dataPlotsFrame = ttk.Frame(self.master)
        self.dataPlotsFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.dataPlotsFrame.bind("<Configure>", self.on_resize)
        matplotlib.rcParams.update({'font.size' : 14})
        self.dataPlotsFigure = Figure(figsize=dataFigSize, dpi=72)
#        colormap = self.dataPlotsFigure.cm.gist_ncar
#plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.jet(np.linspace(0, 1, num_plots))))
        self.dataPlotsFigure.subplots_adjust(left=0.06, right=0.98, top=0.98, bottom=0.05, wspace=0.12, hspace=0.05)
        self.dataPlotsSubplots = []
        self.dataPlotsSubplots.append(self.dataPlotsFigure.add_subplot(2, 2, 1))
        self.dataPlotsSubplots.append(self.dataPlotsFigure.add_subplot(2, 2, 2))
        self.dataPlotsSubplots.append(self.dataPlotsFigure.add_subplot(2, 2, 3))
        self.dataPlotsSubplots.append(self.dataPlotsFigure.add_subplot(2, 2, 4))
        self.dataPlotsCanvas = FigureCanvasTkAgg(self.dataPlotsFigure, master=self.dataPlotsFrame)
        self.dataPlotsCanvas.draw()
        self.dataPlotsCanvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.dataPlotsToolbar = NavigationToolbar2TkAgg(self.dataPlotsCanvas, self.dataPlotsFrame)
        self.dataPlotsToolbar.update()
        self.dataPlotsCanvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.dataPlotsCanvas.mpl_connect('key_press_event', self.on_key_event)

    def on_dataset_selection(self, choice):
        print(f"Current dataset changed to {self.datasetNameVar.get()}")
        self.cD.load_dataset(self.datasetNameVar.get())
        self.infoLabel.configure(text = f"ΔVg = {self.cD.vgDelta}, ΔVd = {self.cD.vdDelta}")
        self.W = self.cD.datasetsParams[self.datasetNameVar.get()]["Ws"][0]
        self.L = self.cD.datasetsParams[self.datasetNameVar.get()]["Ls"][0]
        self.wSlide.config(from_ = 0,
                           to = len(self.cD.datasetsParams[self.datasetNameVar.get()]["Ws"]) - 1)
        self.lSlide.config(from_ = 0,
                           to = len(self.cD.datasetsParams[self.datasetNameVar.get()]["Ls"]) - 1)
        print(f"{self.cD.datasetsParams[self.datasetNameVar.get()]}")
        self.on_wSlide(0)
        self.on_lSlide(0)

    def on_wSlide(self, val):
        Ws = self.cD.datasetsParams[self.datasetNameVar.get()]["Ws"]
        self.wVar.set(round(float(val)))
        self.W = Ws[self.wVar.get()]
        self.wLabelVar.set(f"W = {self.W}")
        self.plot()

    def on_lSlide(self, val):
        Ls = self.cD.datasetsParams[self.datasetNameVar.get()]["Ls"]
        self.lVar.set(round(float(val)))
        self.L = Ls[self.lVar.get()]
        self.lLabelVar.set(f"L = {self.L}")
        self.plot()

    def on_vstepSlide(self, val):
        self.vstepVar.set(round(float(val)))
        self.Vstep = self.vstepVar.get()
        self.vstepLabelVar.set(f"Vstep = {self.Vstep}")
        self.plot()

    def plot(self):
        colorCycle = ['red', 'black', 'black', 'black', 'black',
                      'black', 'black', 'black', 'black', 'black']
        # Id vs Vd
        self.dataPlotsSubplots[0].cla()
        self.dataPlotsSubplots[0].set_prop_cycle(color=colorCycle)
        self.dataPlotsSubplots[0].set_xlabel('Vds [V]')
        self.dataPlotsSubplots[0].set_ylabel('Id [A]')
        dfm1 = cD.dfm.loc[self.W, self.L].unstack(0) # row index is Vd.
        dfm2 = dfm1.loc[:, ::self.Vstep]
        self.dataPlotsSubplots[0].plot(dfm2)
        self.dataPlotsSubplots[0].grid()
        # Id vs Vg
        self.dataPlotsSubplots[1].cla()
        self.dataPlotsSubplots[1].set_prop_cycle(color=colorCycle)
        self.dataPlotsSubplots[1].set_xlabel('Vg [V]')
        self.dataPlotsSubplots[1].set_ylabel('Id [A]')
        self.dataPlotsSubplots[1].set_yscale('log')
        self.dataPlotsSubplots[1].set_ylim(bottom=1e-15)
        dfm3 = cD.dfm.loc[self.W, self.L].unstack(1).loc[:, ::self.Vstep] # row index is Vg.
        x = cD.dfm.index.levels[2].to_numpy() # Vg
        self.dataPlotsSubplots[1].plot(np.abs(dfm3))
        self.dataPlotsSubplots[1].grid()
        # ro
        x = cD.dfm.index.levels[3].to_numpy() # Vd
        ro = np.reciprocal(np.gradient(dfm2, x, axis=0))
        self.dataPlotsSubplots[2].cla()
        self.dataPlotsSubplots[2].set_prop_cycle(color=colorCycle)
        self.dataPlotsSubplots[2].set_xlabel('Vds [V]')
        self.dataPlotsSubplots[2].sharex(self.dataPlotsSubplots[0])
        self.dataPlotsSubplots[2].set_ylabel('ro = ∂Vd/∂Id [Ohm]')
        self.dataPlotsSubplots[2].set_yscale("log")
        self.dataPlotsSubplots[2].plot(x, ro)
        self.dataPlotsSubplots[2].grid()
        # gm
        x = cD.dfm.index.levels[2].to_numpy() # Vg
        gm = np.gradient(dfm3, x, axis=0)
        self.dataPlotsSubplots[3].cla()
        self.dataPlotsSubplots[3].set_prop_cycle(color=colorCycle)
        self.dataPlotsSubplots[3].set_xlabel('Vg [V]')
        self.dataPlotsSubplots[3].sharex(self.dataPlotsSubplots[1])
        self.dataPlotsSubplots[3].set_ylabel('gm = ∂Id/∂Vg [1/Ohm]')
        self.dataPlotsSubplots[3].set_yscale("log")
        self.dataPlotsSubplots[3].set_ylim(1e-15)
        x = cD.dfm.index.levels[2].to_numpy() # Vg
        self.dataPlotsSubplots[3].plot(x, gm)
        self.dataPlotsSubplots[3].grid()
        #
        self.dataPlotsCanvas.draw()
        self.dataPlotsToolbar.update()


    def on_key_event(self, event):
        print('You pressed {:s}'.format(event.key))
        key_press_handler(event, self.dataPlotsCanvas, self.dataPlotsToolbar)

    def on_resize(self, event):
        # print(event.width, event.height)
        return

    def quit(self):
        self.master.quit()     # stops mainloop
        self.master.destroy()  # this is necessary on Windows to prevent
                               # Fatal Python Error: PyEval_RestoreThread: NULL tstate

if __name__ == "__main__":

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--config-file", type=str, default="config.json", help="configuration file")
    parser.add_argument("pkl_files", nargs='+', default=[])

    args = parser.parse_args()
    print(f"Files to consider: {args.pkl_files}")
    cD = CommonData(args.pkl_files)
    print(cD.datasetsParams)

    #
    root = tk.Tk()
    dataPanel = DataPanelGUI(root, cD)
    dataPanel.plot()
    root.mainloop()
    # If root.destroy() is placed here, an error will occur if the window is
    # closed by the window manager.
