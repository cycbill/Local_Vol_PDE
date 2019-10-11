
import numpy as np
import pandas as pd
import xlwings as xw
import os
import matplotlib.pyplot as plt

from read_data import read_data
from calibrate_local_vol_surface import calibrate_local_vol_surface

## Read market data
wb = xw.Book('Local Vol Data.xlsx')
sht = wb.sheets['Calibration Dupire PDE']
curveMat_rd, curveRate_rd, curveMat_rf, curveRate_rf, \
    volMat, strikeMtx, impVolMtx, locVolGuessMtx = read_data(sht)

## Global parameters
NX = 300
NT = 100
spot = 1.3597



local_vol_surface = calibrate_local_vol_surface(spot, NX, NT, curveMat_rd, curveRate_rd, curveMat_rf, curveRate_rf, \
                                                volMat, strikeMtx, impVolMtx, locVolGuessMtx)

