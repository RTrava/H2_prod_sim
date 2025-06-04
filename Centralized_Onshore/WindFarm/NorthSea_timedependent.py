# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 11:08:28 2024

@author: travaglini
"""

# load a time series of wd, ws and ti
import numpy as np
import pandas as pd
import math
from WindFarm.IEA15MW_d250_h150 import IEA15MW
from py_wake.site._site import UniformWeibullSite
from py_wake import NOJ

###############################################################################################################################################
def rotate_point(X, Y, radians, origin):

    XX=[]
    YY=[]
    
    offset_x, offset_y = origin
    
    for i in range(len(X)):
        x=X[i]
        y=Y[i]
        adjusted_x = (x - offset_x)
        adjusted_y = (y - offset_y)
        cos_rad = math.cos(radians)
        sin_rad = math.sin(radians)
        qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
        qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y
        XX.append(qx)
        YY.append(qy)

    return XX, YY

def WTlayout(D, dx, dy, theta): #D= turbine diameter, dx=distance in cross wind direction, dy=distance along wind direction, theta= rotation angle
    
    #generic rectangular wind farm layout (7.5dx5d) oriented with the larger side horizontally
    x_ref = [-0.1084341763, -0.0956772144, -0.0829202525, -0.0701632905, -0.0574063286, -0.0446493667, -0.0318924048, -0.0191354429, -0.0063784810, 0.0063784810, 0.0191354429, 0.0318924048, 0.0446493667, 0.0574063286, 0.0701632905, 0.0829202525, 0.0956772144, 0.1084341763, -0.1084341763, -0.0956772144, -0.0829202525, -0.0701632905, -0.0574063286, -0.0446493667, -0.0318924048, -0.0191354429, 0.0318924048, 0.0446493667, 0.0574063286, 0.0701632905, 0.0829202525, 0.0956772144, 0.1084341763, -0.1084341763, -0.0956772144, -0.0829202525, -0.0701632905, -0.0574063286, -0.0446493667, -0.0318924048, -0.0191354429, 0.0191354429, 0.0318924048, 0.0446493667, 0.0574063286, 0.0701632905, 0.0829202525, 0.0956772144, 0.1084341763, -0.1084341763, -0.0956772144, -0.0829202525, -0.0701632905, -0.0574063286, -0.0446493667, -0.0318924048, -0.0191354429, -0.0063784810, 0.0063784810, 0.0191354429, 0.0318924048, 0.0446493667, 0.0574063286, 0.0701632905, 0.0829202525, 0.0956772144, 0.1084341763]
    y_ref = [-0.0290644846, -0.0290644846, -0.0290644846, -0.0290644846, -0.0290644846, -0.0290644846, -0.0290644846, -0.0290644846, -0.0290644846, -0.0290644846, -0.0290644846, -0.0290644846, -0.0290644846, -0.0290644846, -0.0290644846, -0.0290644846, -0.0290644846, -0.0290644846, -0.0099290417, -0.0099290417, -0.0099290417, -0.0099290417, -0.0099290417, -0.0099290417, -0.0099290417, -0.0099290417, -0.0099290417, -0.0099290417, -0.0099290417, -0.0099290417, -0.0099290417, -0.0099290417, -0.0099290417, 0.0092064012, 0.0092064012, 0.0092064012, 0.0092064012, 0.0092064012, 0.0092064012, 0.0092064012, 0.0092064012, 0.0092064012, 0.0092064012, 0.0092064012, 0.0092064012, 0.0092064012, 0.0092064012, 0.0092064012, 0.0092064012, 0.0283418440, 0.0283418440, 0.0283418440, 0.0283418440, 0.0283418440, 0.0283418440, 0.0283418440, 0.0283418440, 0.0283418440, 0.0283418440, 0.0283418440, 0.0283418440, 0.0283418440, 0.0283418440, 0.0283418440, 0.0283418440, 0.0283418440, 0.0283418440]
    D_ref = 250     #[m] reference diameter
    dx_ref = 5      #[diameters] crosswind distance
    dy_ref = 7.5    #[diameters] alongwind distance
    
    x_ref_new = np.array(x_ref)*(D/D_ref) # spatial coordinate with corect D
    y_ref_new = np.array(y_ref)*(D/D_ref) # spatial coordinate with corect D

    x_ref_new0 = (x_ref_new - x_ref_new[0])*(dx/dx_ref)
    y_ref_new0 = (y_ref_new - y_ref_new[0])*(dy/dy_ref)


    x_new = x_ref_new0 * (D*dx)/x_ref_new0[1] #[m] distance in m needed 4 PyWake
    y_new = y_ref_new0 * (D*dy)/y_ref_new0[18] #[m] distance in m needed 4 PyWake
    origin = (x_new[17]/2, y_new[49]/2)
    
    x, y = rotate_point(x_new, y_new, theta, origin)

    return x, y

def WF_model(dx, dy, D, theta, df):#[diameters] cross-wind distance , [diameters] along wind distance, [m] WT diameter, [°] revalent wind direction, wind source dataframe

    '_________________________________________Wind farm layout_________________________________________'
    x, y = WTlayout(D, dx, dy, theta)
    
    '_________________________________________Installation site_________________________________________'
    
    
    class NorthSea(UniformWeibullSite):
        def __init__(self, ti=.1, shear=None):
            #weibull initialization needed for the code
            f = [1]
            a = [1]
            k = [1]
            UniformWeibullSite.__init__(self, np.array(f) / np.sum(f), a, k, ti=ti, shear=shear)
            self.initial_position = np.array([x, y]).T
    
    #time dependent wind surce superimposition
    Time=df.index
    wd=df.iloc[:,1]     #[deg]
    ws=df.iloc[:,2]     #[m/s]
    site = NorthSea()
    x = np.array(x)
    y = np.array(y)
    windTurbines = IEA15MW()
    time_stamp = np.arange(len(wd))/6/24 #[days]
    
    '_________________________________________model definition + run_________________________________________'
    
    # Call the wind farm model with the time=time_stamp and the time-dependent operating keyword argument.
    # setup new WindFarmModel with site containing time-dependent TI and run simulation
    wf_model = NOJ(site, windTurbines, k=0.04)  # k=wake espansion factor
    sim_res_time = wf_model(x, y,               #[m] wind turbine positions
                            wd=wd,              #[°] Wind direction time series
                            ws=ws,              #[m/s] Wind speed time series
                            time=time_stamp,     #[day^-1] time_stamp, # time stamps (should be normalized on a dayly basis)
                      )
    
    '_________________________________________save_________________________________________'

    AEP = sim_res_time.aep().data.sum(axis=1)                  #[Wh]This will show an xarray with the characteristics of the site, including the number of turbines and the wind speed and wind direction studied. In addition, it will show the AEP [GWh] of each turbine for each flow case.
    totalAEP = AEP.sum()/1e03                                  #[kWh] Wind Farm AEP        
    
    output = pd.DataFrame()
    #dataframe with global production

    ParkPower=np.zeros(len(wd))
    for i in range(len(x)):
        ParkPower = np.add(ParkPower, sim_res_time.Power.sel(wt=i).data)
    
    output['Time Stamp'] = Time    
    output['Wind Power [kW]'] = ParkPower/1e03                  #[kW] Wind Farm AEP
    
    return output, totalAEP
###############################################################################################################################################



