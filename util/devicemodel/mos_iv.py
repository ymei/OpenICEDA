#!/usr/bin/env python
# -*- coding: utf-8 -*-

## @package mos_iv
# process MOS I/V simulation data
#
from __future__ import print_function
from __future__ import division
import math,sys,time,os,shutil
import sqlite3 as db

import numpy as np
import pandas as pd

if sys.version_info[0] < 3:
    # import Tkinter as tk
    pass
else:
    # import tkinter as tk
    pass

## NMOS nfet 01v8
#Ws = [0.36, 0.39, 0.42, 0.52, 0.54, 0.55, 0.58, 0.6, 0.61, 0.64, 0.65, 0.74, 0.84, 1, 1.26, 1.68, 2, 3, 5, 7, 100]
#Ls = [0.15, 0.18, 0.25, 0.5, 1, 2, 4, 8, 20, 100]
## NMOS nfet 01v8_lvt
Ws = [0.42, 0.55, 0.64, 0.84, 1, 1.65, 3, 5, 7, 100]
Ls = [0.15, 0.18, 0.25, 0.5, 1, 2, 4, 8, 100]
Vgs = np.linspace(0, 1.8, 361)
Vds = np.linspace(0, 1.8, 361)
## PMOS pfet 01v8
#Ws = [0.42, 0.55, 0.64, 0.84, 1, 1.26, 1.65, 1.68, 2, 3, 5, 7, 100]
#Ls = [0.15, 0.18, 0.25, 0.5, 1, 2, 4, 8, 20, 100]
## PMOS pfet 01v8_lvt
#Ws = [0.42, 0.55, 1, 3, 5, 7, 100]
#Ls = [0.35, 0.5, 1, 1.5, 2, 4, 8, 20, 100]
#Vgs = np.linspace(0.0, -1.8, 361)
#Vds = np.linspace(0.0, -1.8, 361)

## Number of lines in data block header
dbHeaderNLines = 12

if __name__ == "__main__":
    fname = sys.argv[1]
    ofname = sys.argv[2]
    ofname1 = ofname.split(".sqlite")[0]+".pkl"

    ofp = db.connect(ofname)
    dbcur = ofp.cursor()
    sql_create_table = """CREATE TABLE IF NOT EXISTS mos_iv (
    W real NOT NULL,
    L real NOT NULL,
    Vg real,
    Vd real,
    Id real
    );"""
    dbcur.execute(sql_create_table)

    midx = pd.MultiIndex.from_product([Ws, Ls, Vgs, Vds], names=["W", "L", "Vg", "Vd"])
    pda = np.zeros(len(midx))
    ie = 0

    iw = 0
    il = -1
    with open(fname, 'r') as fp:
        while True:
            line = fp.readline()
            if not line: # EOF
                break
            if line[0:5] == 'Title':
                il += 1
                if il >= len(Ls):
                    il = 0
                    iw += 1
                [fp.readline() for i in range(dbHeaderNLines-1)]
                if iw>=len(Ws) or il>=len(Ls):
                    print("Extra data found! iw={:d}, il={:d}".format(iw, il))
                    break
                W = Ws[iw]
                L = Ls[il]
                print("W/L = {:g}/{:g}".format(W, L))
                if iw>0 or il>0:
                    ofp.commit()
                continue
            ls = line.split()
            if len(ls) == 2:
                Vd = float(ls[1])
                Vg = float(fp.readline())
                fp.readline()
                Id = float(fp.readline())
                pda[ie] = Id
                ie += 1
                sql = "INSERT INTO mos_iv VALUES ({:g}, {:g}, {:g}, {:g}, {:g})".format(
                    W, L, Vg, Vd, Id)
                dbcur.execute(sql)

    print("Total number of data points: {:d}".format(ie))
    ofp.commit()
    ofp.close()

    pdf = pd.Series(pda, index=midx, name="Id").to_frame()
    pdf.to_pickle(ofname1)
