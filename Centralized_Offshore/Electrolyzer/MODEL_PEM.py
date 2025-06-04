# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 10:30:52 2024

@author: Riccardo

"""

import numpy as np
from scipy import interpolate
import math

V_array_ideal = np.array([1.2,1.823187069])   #[V] linear region voltage
i_array_linear = np.array([0,1.5])  #[A/cm^2] linear region current density ->>[0,2.4] to use a range from 0 to 160% of the nominal cell power
i_array_ideal = np.array([0.000001, 0.004350739, 0.008825151, 0.021180363, 0.035741866, 0.06177606, 0.09266409, 0.19944842, 0.40242693, 1.5]) #[A/cm^2] actual current density

def pem_EL_model(T_el, h_work_tot, kWh_factor, H2_tot_des, V_degr, i_array_ideal = i_array_ideal, i_array_linear = i_array_linear): #Power input to the electrolyzer [], number of cells [-], Temperature []
    
    '''
    conv_factor : conversion efficiency Power to H2.
    f_i_V : current to voltage function.
    f_H2_i : H2 production to current function .
    V_array : Min e max voltaggio.
    '''
    
    Replacement = False
    W_cell = 2.735                      #[kW] nominal cell power
    n_cells_design = 100                # number of cells in the 273 kW stack
    W_EL_ref = 1e03                     #[kW] stack reference size
    SF = W_EL_ref/(W_cell * n_cells_design)        # scale factor della configurazione, lo applico al volume
    
    'aux Power'
    W_compr = 0.013292425   #[-] power consumption compressor 
    
    T_operation = 80                    #[°C] design operation temperature
    V_T = 4e-3                          #[mV/°C] cool down voltage increase
    S_cell = 1e03                       #[cm^2] surface of cells
    
    I_array     = i_array_ideal * S_cell /1e03   #[kA] current
    I_array_lin = i_array_linear * S_cell /1e03   #[kA] current
    
    V_array     = np.array([2656.5676410365854 *np.exp(- 1.6837330206777318e-05 *T_el)*np.log( 4.831579563780809e-05 *j+ 1.000431570616741 )+ 1363.9113612443105 *np.exp(- 0.0552003111609333 *T_el)*np.log( 7.411258168728302e-05 *j+ 0.9999440017340709 )+ 0.10523067647514033 *np.exp(- 0.00790107077361709 *T_el)*np.log( 5715.45376014452 *j+ 2.1862298129926083 ) + V_degr * h_work_tot for j in I_array])#[V] actual voltage array
    V_repl      = (V_array_ideal + V_T*(T_operation - T_el)) * 1.2 #[V] replacement voltage array
    
    if max(V_array) >= max(V_repl): 
        Replacement = True
        print('High voltage, new electrolyzer  needed')

    'nominal volume flow rates'       
    H2_tot_des = (W_cell*n_cells_design)/H2_tot_des                     #[kg/h] mass flow rate of H2 per stack 62.1*0.08988
    
    'el operation'
    #H2 production array of the stack = n_cells * H2 production of a cell
    H2_array    = np.array([0, H2_tot_des * SF])
    
    #link between cell current (= stack current) and cell voltage: polarization curve
    f_i_V = interpolate.interp1d(I_array,V_array)

    #link between stack H2 production and stack current (= cell current)                 
    f_H2_i = interpolate.interp1d(H2_array/kWh_factor,I_array_lin) 
    
    #conversion factor calculation: H2 stack production / P stack consumption
    conv_factor = max(H2_array)/ (max(I_array) * max(V_array) * (n_cells_design*SF))      # [kg/kWh]    
    
    return conv_factor, f_i_V, f_H2_i, V_array, W_compr, Replacement


def pem_EL_transit(H2_prod,f_i_V, f_H2_i, T_el, T_ext, kWh_factor):# Temperatures in K, H2_prod in kg/h
    
    '''
    Themal model: exothermic reaction (heat production from thermal lossess DeltaV = V-Vtn)  
    T_el : electrolyzer temperature
    '''
    
    n_cells_design = 100               # number of cells in the 273.5kW module
    W_cell = 2.735                      #[kW] nominal cell power
    W_EL_ref = 1e03                     #1MW stack
    SF = W_EL_ref/(W_cell * n_cells_design)        # scale factor della configurazione, lo applico al volume
    
    A_ext = 0.7546                       #[m^2] stack outside surface area
    op_time = (60*60)/(kWh_factor)       # [s]  simulation time in seconds
    T_op = 80                            # [°C] operating temperature
    V_tn = 1.48                        # [V]  thermoneutral voltage
      
    'heat coefficeints'
    hc = 14.55                          #[W/m^2K] convective heat transfer coefficient
    eps= 0.6                            #[-]  emittance of unpolished stainless steel 
    sigma = 5.67e-8                     #[W/m^2K^4] stefan Boltzman constant
    T_m = ((T_el + T_ext) / 2) + 273.15 #[K] mean temperature of the stack surface and the enclosing container
    hr = 4 * eps * sigma * T_m**3       #[W/m^2K] radiative heat transfer coefficient
    c_stack = 135100 * SF**(1/3)        # [J/K]   stack thermal capacity

    'instulated container'
    k_ins = 0.045                       #[W/mK] thermal conductivity of the insulaton layer --> rock wool
    t_ins = 0.02                        #[m] insulation layer thickness
      
    q_lost = 1/(1/(hc + hr) + t_ins/k_ins) * A_ext * (T_el - T_ext) # [W] thermal power lost to the environment
    
    if H2_prod > 0:  
        #stack current from H2 production
        I_op = f_H2_i(H2_prod)
        #cell voltage from cell current (= stack current)
        V_op = f_i_V(I_op)
        
        #thermal power generated form the stack
        q_gain = (n_cells_design * SF) * (V_op-V_tn)*I_op*1000     # [V]*[kA]*1000 = [V]*[A] = [W] produce thermal power
                
        Tx = T_el + (op_time / c_stack) * (q_gain - q_lost)
    
        if Tx > T_op:
            Tx = T_op
        
        q_cool = q_gain - q_lost #[W] cooling power needed

    else:
        Tx = T_el - (op_time / c_stack) * q_lost
        q_cool = 0
    
    return Tx, q_cool
