import pandas as pd
import numpy as np
from SystemOperation.H2simulation_nogrid import simplified_sim
from Components import components, energy
from Economics.LCOH_calculator import LCOH_func
import time
import os

time_start = time.perf_counter()

tech = 'ALK'                        #[-] electrolyzer technology, options: 'ALK', 'PEM'
ex_dist = 100                       #[km] export distance, options:50, 100, 200              
bound_t = ['opt', 'pes', 'avg']     #[-] techncal boundaries for the simulations, options: 'opt', 'pes', 'avg'

#%%
for bound_tech in bound_t:

    kWh_factor = 6   #[-] factor for resolution definition -> kWh_factor = 60/resolotion in minutes 
    lifetime = 25    #[y] plant lifetime 
    r = 0.07         #[-] interest rate
    
    'wind farm data'
    D = 250                         #[m] IEA15MW_RWT
    l = 7.5                         #[diameters] cross-wind distance
    L = 14                          #[diameters] along-wind  distance

    'wind power dataset'
    df_WP = pd.read_csv(os.path.dirname(os.getcwd()) + '\\WindFarm\\WindPower_res\\' + str(ex_dist) + 'km\\time_dep_pp_' + str(ex_dist) + '_25y.csv')
    df_WP = df_WP.rename(columns={"WF Power [kW]": "Wind Power [kW]", "Unnamed: 0": 'Time Stamp'})
    df_WP.iloc[0:6*24*365, :]
    
    'EL performance '
    N_EL = 67 #[-] electrolyzer number
    EL_P_nom = 1000 * 1e03 / N_EL#[kW]  electrolyzer nominal power
    EL_cell_power = components[tech]['cell_power']          #[kW] cell nominal power
    N_cell = EL_P_nom  / EL_cell_power #[-] cell number
    SF = 0.69 #[-] scale factor for electrolyzer cost calclations 
    CF_nom = components[tech]['CF_nom'] #[kg/MWh]
    
    eta_rect = 1 #[-] rectifier AC-DC efficiency to allow power usage from wind farm power to BESS/EL 
    
    'cables lenght calculator' 
    depth = 50                     #[m] sea depth
    li = l * D + 2 * depth * 2.6
    L = L * D 
    IA_length = li * 51 + 4 * ((np.sqrt((3*l)**2+L**2) + 2 * depth * 2.6) + (1.6*L*4 + 2 * depth * 2.6) + (np.sqrt((4.5*l)**2+(0.5*L)**2) + 2 * depth * 2.6) + (np.sqrt((1.5*l)**2+(0.5*L)**2) + 2 * depth * 2.6))
    IA_length /= 1e03                           #[km]
    n_IA_cables = 12                            #[-] number of intra array cables
    EX_length = 2.84*(depth-20)/1000 + ex_dist  #[km]
    BB_lenght = 10                              #[km] lenght of the pipelines between hot tap and POD
    
    L_pipe_off = EX_length                      #[km] export pipeline length
    L_pipe = BB_lenght                          #[km] onshore pipeline length
    
    simp_output, time_series = simplified_sim(df_WP, EL_P_nom, components, energy, tech, kWh_factor, L_pipe_off, EX_length, IA_length/n_IA_cables, eta_rect, bound_tech) #
    
    #%%
    'LCOH' 
    
    economic_sim = False # set true to run only economic analysis
    path=os.getcwd()+'\\Results\\' + str(ex_dist) + '\\' + tech
    
    bounds = ['HB', 'LB', 'ref', 'avg'] #[-] economic boundaries for the simulations, options: 'HB', 'LB', 'ref', 'avg'
    reps = [True, False] #repurposed (true) or new (false) pipelines

    if not os.path.exists(path):
        os.makedirs(path)
    for bound_tech in bound_t:
        for bound in bounds:
            for rep in reps:
                if rep: pipe_tipe = 'rep_pipe'
                else: pipe_tipe = 'new_pipe'
        
                if economic_sim: simp_output=pd.read_csv(path+'\\simp_output_results_'+tech+'_'+str(ex_dist)+'_'+bound+'_'+bound_tech+'_'+pipe_tipe+'.csv')
                
                EX_length = 2.84*(depth-20)/1000 + ex_dist #[km]
                L_pipe_off = EX_length
                
                'sizes dic'
                sizes = {}
                sizes['EL']                 =   EL_P_nom / 1e03                             # [MW]
                sizes['WF']                 =   1005                                        # [MW] 
                sizes['IA_pipe']            =   IA_length                                   # [km]
                sizes['EX_pipe']            =   EX_length                                   # [km]
                sizes['Backbone_pipe']      =   L_pipe                             # [km]     
                if not economic_sim: sizes['Compressor_off'] =   max(time_series['Compr_power[MW]'])         #[MW]
                if  economic_sim: sizes['Compressor_off'] =  components['Compressor_on'][tech + '_ref']         #[MW]
                sizes['RO_unit']            =   CF_nom * sizes['EL']*N_EL * 24 * energy['H2']['H2O_cons'] / 1e03 #[m^3/d] dayly permeate production 
                sizes['substation']         =   EL_P_nom / 1e03 * N_EL 
                
                energy['H2']['H2_prod_EL[kg/y]'] = simp_output['H2_prod_EL[kg/y]']
                energy['electricity']['E_res[MWh/y]'] = simp_output['E_res[MWh/y]']
                energy['electricity']['E_purch[MWh/y]'] = simp_output['E_grid[MWh/y]']
                energy['H2O']['brines[kg/y]'] = simp_output['H2O_brine[MWh]']
                if not economic_sim: components[tech]['lifetime'] = round(time_series[time_series['el_replacements [-]'] == 1].index[0]/(8760*kWh_factor))
                if economic_sim: components[tech]['lifetime'] = components[tech]['lifetime_' + bound_tech]         #[MW]
                
                LCOH, df_cost_ts, df_comp_cost = LCOH_func(sizes, N_EL, components, tech, energy, r, lifetime, SF, bound, rep)
                print('el:'+str(tech), '\ndistance from shores:'+str(L_pipe_off), '\ndistance from substation:'+str(L_pipe), '\nLCOH:'+str(LCOH))
                simp_output['LCOH [€/kg]'] = LCOH
                
                'Output'
                df_cost_ts.to_csv(path +'\\time_dep_costs_'+tech+'_'+str(ex_dist)+'_'+bound+'_'+bound_tech+'_'+pipe_tipe+'.csv')
                df_comp_cost.to_csv(path +'\\sistem costs_'+tech+'_'+str(ex_dist)+'_'+bound+'_'+bound_tech+'_'+pipe_tipe+'.csv')
                simp_output.to_csv(path +'\\simp_output_results_'+tech+'_'+str(ex_dist)+'_'+bound+'_'+bound_tech+'_'+pipe_tipe+'.csv')
        time_series.to_csv(path +'\\phys_flows_D-OFF.csv')
    
