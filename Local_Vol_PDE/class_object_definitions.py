import numpy as np

def linear_intrp(x, x1, x2, y1, y2):
    return (y2-y1)/(x2-x1)*(x-x1) + y1

class clsRateCurve():
    def __init__(self, curveMat, curveRate):
        self.curveMat = curveMat
        self.curveRate = curveRate
    def interpolate(self, t, method):
        if method == "linear":
            if t <= self.curveMat[0]:
                return self.curveRate[0]
            elif t >= self.curveMat[-1]:
                return self.curveRate[-1]
            else:
                t_idx = np.searchsorted(self.curveMat, t)
                return linear_intrp(t, self.curveMat[t_idx-1], 
                                       self.curveMat[t_idx], 
                                       self.curveRate[t_idx-1], 
                                       self.curveRate[t_idx])


class clsVolSurface():
    def __init__(self, volMat, strikeMtx, impVolMtx):
        self.volMat = volMat
        self.strikeMtx = strikeMtx
        self.impVolMtx = impVolMtx
    def interpolate(self, t, k, tmethod, kmethod):
        if tmethod == "constant":
            t_idx = np.searchsorted(self.volMat, t)
            if t > self.volMat[-1]:
                t_idx = -1
        if kmethod == "linear":
            if k <= self.strikeMtx[t_idx, 0]:
                return self.impVolMtx[t_idx, 0]
            elif k >= self.strikeMtx[t_idx, -1]:
                return self.impVolMtx[t_idx, -1]
            else:
                k_idx = np.searchsorted(self.strikeMtx[t_idx,:], k)
                return linear_intrp(k, self.strikeMtx[t_idx, k_idx-1],
                                       self.strikeMtx[t_idx, k_idx],
                                       self.impVolMtx[t_idx, k_idx-1], 
                                       self.impVolMtx[t_idx, k_idx])
