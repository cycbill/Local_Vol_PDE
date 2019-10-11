import numpy as np
import xlwings as xw
import os

def read_data(sht):
    curveMat_rf = sht.range('C21:C33').options(np.array).value
    curveRate_rf = sht.range('D21:D33').options(np.array).value
    curveMat_rd = sht.range('G21:G40').options(np.array).value
    curveRate_rd = sht.range('H21:H40').options(np.array).value

    volMat = sht.range('K22:K32').options(np.array).value
    strikeMtx = sht.range('L22:R32').options(np.array).value
    impVolMtx = sht.range('S22:Y32').options(np.array).value
    locVolGuessMtx = sht.range('Z22:AF32').options(np.array).value

    return curveMat_rd, curveRate_rd, curveMat_rf, curveRate_rf, volMat, strikeMtx, impVolMtx, locVolGuessMtx