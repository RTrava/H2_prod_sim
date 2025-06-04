# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 13:48:22 2024

@author: Riccardo
"""

import pandas as pd
import os
from PEM_Tvar import PEM_EL, EL_transit

# path = os.getcwd()
# directory = 'wind famr case'
# file_r ='power from wind farm.csv'

# df = pd.read_csv(path + directory + file_r, index_col=0)
# Power = df.iloc[:, 1]
# Power = Power.to_list()

Power=[1e03]*8760*6

EL_cell_power = 2.775         #[kW]
# #number of availabe cells 500000 cells = 1MW
# EL_cell_number = 361
#electrolyzer stack nominal pwoer [kW]
EL_P_nom = 1e03 
EL_cell_number = round(EL_P_nom / EL_cell_power)
#power required by the alkaline electrolyzer to start the hydrogen production
EL_P_min = 0.5 * EL_P_nom
#new electrolyzer condition
EL_h_work = 0
# intial electrolyzer temperature
EL_T_0 = 80               #[°C]
EL_T_list = [EL_T_0]
T_EXT = 25              #[°C] ext temperature
#ramp rate limit
RR = 500 * 60 #[kW/min]
#conversion factor list
EL_CF_list = []

kWh_factor = 6

EL_P_recieved_list = []
EL_H2_prod_list = []
EL_H2_prod_list_y = []
EL_H2_prod_y = []
Q_cooling = []

for i in range(len(Power)):

    'eletrolyzer activation'
    #conversion factor update
    EL_CF, EL_f_i_V, EL_f_H2_i, V_array = PEM_EL(EL_T_list[i], EL_h_work, EL_cell_number, kWh_factor)
    #trend of the conversion factor
    EL_CF_list.append(EL_CF)
    
    #H2 production calculation in the given minute
    if i == 0: P=Power[i]
    else:
        if Power[i] - Power[i-1] <= RR * (60/kWh_factor): P=Power[i]
        if Power[i] - Power[i-1] > RR * (60/kWh_factor): P= RR * (60/kWh_factor)

    if P > EL_P_min:
        if P < EL_P_nom:
            EL_P_given = P
        else:
            EL_P_given = EL_P_nom
        
        EL_H2_prod = EL_P_given * EL_CF / kWh_factor
        
        
    else:
        EL_H2_prod = 0
        EL_P_given = 0
        
        
    #trend of the power fed to the electrolyzer
    EL_P_recieved_list.append(EL_P_given)
    #H2 produced at each timestep
    EL_H2_prod_list.append(EL_H2_prod)

    'Thermal management'
    EL_T, q_cooling = EL_transit(EL_H2_prod, EL_f_i_V, EL_f_H2_i, EL_T_list[i], EL_cell_number, T_EXT, kWh_factor) 
    EL_T_list.append(EL_T)    #electrolyzer temperature evolution in time
    Q_cooling.append(q_cooling)
    #working hours counting only if activated
    if EL_H2_prod > 0:
        EL_h_work = EL_h_work + 1/kWh_factor