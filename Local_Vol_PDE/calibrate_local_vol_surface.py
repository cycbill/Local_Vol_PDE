import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from class_object_definitions import clsRateCurve, clsVolSurface
from utilities import calc_forward, black_scholes_vanilla

#def initial_cond(iPillar, spot, lnK):
#    if iPillar == 0:
#        premium = np.maximum(spot - np.exp(lnK), np.zeros_like(lnK))
#    else:
#        premium = black_scholes(spot, np.exp(lnK), )

def local_vol_solver(iPillar, spot, NX, NT, Tstart, Tend, strikes, lnStrikes, impVols, 
                     locVolGuessMtx, clsDomCurve, clsForCurve, callputs):

    ## Get target price
    rd = clsDomCurve.interpolate(Tend, 'linear')
    rf = clsForCurve.interpolate(Tend, 'linear')
    target_prices = black_scholes_vanilla(spot, strikes, Tend, rd, rf, impVols)

    ## Get PDE price
    dx = (lnStrikes[-1] - lnStrikes[0]) / (NX+1)
    dt = (Tend - Tstart) / (NT+1)
    x_grids = np.linspace(lnStrikes[0], lnStrikes[1], NX+1, True)
    t_grids = np.linspace(Tstart, Tend, NT+1, True)
    #u = initial_cond(iPillar, spot, x_grids)
    return target_prices


def calibrate_local_vol_surface(spot, NX, NT, curveMat_rd, curveRate_rd, curveMat_rf, 
                                curveRate_rf, volMat, strikeMtx, impVolMtx, locVolGuessMtx):
	
    nbMat = len(volMat)
    nbStrike = strikeMtx.shape[1]
    
    #print('maturity:')
    #print(volMat)
    #print('strike:')
    #print(strikeMtx)
    #print('vol:')
    #print(impVolMtx)

    local_vol_surface = np.zeros_like(locVolGuessMtx)
    clsDomCurve = clsRateCurve(curveMat_rd, curveRate_rd)
    clsForCurve = clsRateCurve(curveMat_rf, curveRate_rf)
    clsImpVol = clsVolSurface(volMat, strikeMtx, impVolMtx)
    
    forwards = calc_forward(spot, volMat, clsDomCurve, clsForCurve)

    callputs = np.array([0,0,0,0,1,1,1])

    
    ## Plot implied vol surface
    #t_list = np.linspace(0,0.02,100,True)
    #k_list = np.linspace(0.5,2.0, 300, True)
    #kgrids, tgrids = np.meshgrid(k_list, t_list)
    #surface = np.zeros((100,300))
    #for i,t in enumerate(t_list):
    #    for j,k in enumerate(k_list):
    #        #print(i,j,t,k)
    #        surface[i,j] = clsImpVol.interpolate(t, k, "constant", "linear")
    #print(tgrids.shape, kgrids.shape, surface.shape)
    #fig = plt.figure()
    #ax = plt.axes(projection='3d')
    #ax.plot_surface(tgrids, kgrids, surface, cmap='viridis', edgecolor='none')
    #plt.show()

    
    for i in range(nbMat):
        if i == 0:
            Tstart = 0
            Tend = volMat[i]
        else:
            Tstart = volMat[i-1]
            Tend = volMat[i]
        local_vol_surface[i,:] = local_vol_solver(i, spot, NX, NT, Tstart, Tend, strikeMtx[i,:], np.log(strikeMtx[i,:]), impVolMtx[i,:], 
                                                    locVolGuessMtx, clsDomCurve, clsForCurve, callputs)
    print(local_vol_surface)
    return local_vol_surface