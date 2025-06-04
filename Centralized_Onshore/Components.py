# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 13:11:36 2023

@author: travaglini
"""

#this scripr contains the technologies we want to use for the model
#each coponent is defined as a dictionary where the specific features are specified
import numpy as np

'_______________________________________components_______________________________________'
components = {}

components['WT'] =                  {#technical
                                     'flag':                    'OFF',             #boolean to actiate components in LCOH calculation
                                     'capacity':                15,                # [MW] per wind turbine
                                     #economic     
                                     'lifetime':                30,                 #[y]
                                     'specific_CAPEX_ref':      2400e03,            #[€/MW] (expert validated) per wind turbine capacity  
                                     'specific_CAPEX_avg':      2305.7e03,          #[€/MW] (average) per wind turbine capacity  
                                     'specific_CAPEX_HB':       2839400,            #[€/MW] (higher bound) per wind turbine capacity  
                                     'specific_CAPEX_LB':       2007300,            #[€/MW] (lower bound) per wind turbine capacity  
                                     'O&M_ref' :                0.026,              #[-] fraction of the CAPEX
                                     'O&M_avg' :                0.026,              #[-] fraction of the CAPEX
                                     'O&M_HB' :                 0.06,               #[-] fraction of the CAPEX
                                     'O&M_LB' :                 0.029,              #[-] fraction of the CAPEX
                                     'replacement_cost_ref':    0.7,                #[-] fraction of the CAPEX
                                     'replacement_cost_avg':    0.7,                #[-] fraction of the CAPEX
                                     'replacement_cost_HB':     0.7,                #[-] fraction of the CAPEX
                                     'replacement_cost_LB':     0.7,                #[-] fraction of the CAPEX
                                     #economic parameters
                                     'contingency_costs':       0.0,                #[%] of the capex
                                     'development_costs':       0.0,                #[%] of the capex
                                    }
                                   
components['RO_unit'] =        {
                                     'flag':                    'OFF',              #boolean to actiate components in LCOH calculation
                                     'Conv_f':                  4.5,                #[kWh/kg] 
                                     'Rec_f':                   0.45,               #[-] Recovery factor =(permeate/feed)
                                     #economic     
                                     'lifetime':                30,                 #[y]
                                     'specific_CAPEX_ref':      1212.3,             #[€/m3/d] per RO capacity  ->> define the capacity as m3/d 
                                     'specific_CAPEX_avg':      1212.3,             #[€/m3/d] per RO capacity  ->> define the capacity as m3/d 
                                     'specific_CAPEX_HB':       1212.3,             #[€/m3/d] per RO capacity  ->> define the capacity as m3/d 
                                     'specific_CAPEX_LB':       1212.3,             #[€/m3/d] per RO capacity  ->> define the capacity as m3/d 
                                     'O&M_ref':                 0.0217,             #[-] fraction of the CAPEX
                                     'O&M_avg':                 0.0217,             #[-] fraction of the CAPEX
                                     'O&M_HB':                  0.025,              #[-] fraction of the CAPEX
                                     'O&M_LB':                  0.02,               #[-] fraction of the CAPEX
                                     'replacement_cost_ref':    0.7,                #[-] fraction of the CAPEX
                                     'replacement_cost_avg':    0.7,                #[-] fraction of the CAPEX
                                     'replacement_cost_HB':     0.7,                #[-] fraction of the CAPEX
                                     'replacement_cost_LB':     0.7,                #[-] fraction of the CAPEX
                                     'brine_disp_on':           7.3e-3/445,         #[€/m3] brine cost 
                                     'brine_disp_off':          7.3*3e-3/445,       #[€/m3] brine cost accounting for ships  
                                     'brine_disp_dec':          0,                  #[€/m3] directly immited into water  
                                     #economic parameters
                                     'contingency_costs':       0.3,                #[%] of the capex
                                     'development_costs':       0.05,               #[%] of the capex
                                     }
    
#electrolyzers
components['ALK'] =                 {
                                     'flag':                'OFF',             #boolean to actiate components in LCOH calculation
                                     'cell_power':           9.45,             #[kW] nominal power
                                     'cell_min_power':       0.2,              #[kW] minimum power
                                     'stack_power':          1e03,             #[kW]
                                     'CF_nom':               17.98,            #[kg/MWh]
                                     'nom_mass_flow_opt':    47.1,             #[kWh/kg]
                                     'nom_mass_flow_pes':    55.6,             #[kWh/kg]
                                     'nom_mass_flow_avg':    51.8,             #[kWh/kg]
                                     'degr_time_opt':        4.00e-6,          #[V/h]
                                     'degr_time_pes':        6.85e-6,          #[V/h]
                                     'degr_time_avg':        5.04e-6,          #[V/h]
                                     'T_op':                 70,               #[°C] operative temperature
                                     'T_min':                35,               #[°C] electrolyzer minimum working temperature
                                     'CS':                   20,               #[min] cold startup time 
                                     'ref_size':             10,               #[MW] reference size for cost calculations
                                     'output_H2_pressure':   5,                #[bar] 
                                     'lifetime':             10,               #[y] first try
                                     'lifetime_opt':         11,               #[y]
                                     'lifetime_pes':         7,                #[y]
                                     'lifetime_avg':         9,                #[y]
                                     #economics
                                     'specific_CAPEX_ref':   727.8e03,         #[€/MW] 
                                     'specific_CAPEX_avg':   663.9e03,         #[€/MW] 
                                     'specific_CAPEX_HB':    1000e03,          #[€/MW] 
                                     'specific_CAPEX_LB':    350e03,           #[€/MW] 
                                     'O&M_ref' :             0.03,             #[-] fraction of the CAPEX
                                     'O&M_avg' :             0.03,             #[-] fraction of the CAPEX
                                     'O&M_HB' :              0.04,             #[-] fraction of the CAPEX
                                     'O&M_LB' :              0.02,             #[-] fraction of the CAPEX
                                     'replacement_cost_HB':  0.55,             #[-] fraction of the CAPEX
                                     'replacement_cost_LB':  0.4,              #[-] fraction of the CAPEX
                                     'replacement_cost_ref': 0.475,            #[-] fraction of the CAPEX
                                     'replacement_cost_avg': 0.475,            #[-] fraction of the CAPEX
                                     'COP'    :              4.5,              #[MWh_th/MWh_el]
                                     #economic parameters
                                     'contingency_costs':    0.0,              #[%] of the capex
                                     'development_costs':    0.0,              #[%] of the capex
                                    }


components['PEM'] =                 {
                                     'flag':                'OFF',              #boolean to actiate components in LCOH calculation
                                     'cell_power':          2.735,              #[kW]
                                     'stack_power':         273.5,              #[kW]
                                     'cell_min_power':      0.05,               #[kW] minimum power
                                     'CF_nom':              20.113,             #[kg/MWh]
                                     'nom_mass_flow_opt':   49.2,               #[kWh/kg]
                                     'nom_mass_flow_pes':   58.1,               #[kWh/kg]
                                     'nom_mass_flow_avg':   52.6,               #[kWh/kg]
                                     'degr_time_opt':       4.29e-6,            #[V/h]
                                     'degr_time_pes':       6.60e-6,            #[V/h]
                                     'degr_time_avg':       4.85e-6,            #[V/h]
                                     'T_op':                80,                 #[°C] operative temperature
                                     'T_min':               35,                 #[°C] electrolyzer minimum working temperature
                                     'CS':                  10,                 #[min] cold startup time 
                                     'ref_size':            10,                 #[MW] reference size for cost calculations
                                     'output_H2_pressure' : 30,                 #[bar] 
                                     'lifetime':            10,                 #[y]
                                     'lifetime_opt':            10,             #[y]
                                     'lifetime_pes':            6,              #[y]
                                     'lifetime_avg':            9,              #[y]
                                     #economics
                                     'specific_CAPEX_ref':   872.3e03,          #[€/MW] 
                                     'specific_CAPEX_avg':   824.5e03,          #[€/MW] 
                                     'specific_CAPEX_HB':    1400e03,           #[€/MW] 
                                     'specific_CAPEX_LB':    500e03,            #[€/MW] 
                                     'O&M_ref' :             0.026,             #[-] fraction of the CAPEX
                                     'O&M_avg' :             0.026,             #[-] fraction of the CAPEX
                                     'O&M_HB' :              0.04,              #[-] fraction of the CAPEX
                                     'O&M_LB' :              0.015,             #[-] fraction of the CAPEX
                                     'replacement_cost_HB':  0.55,              #[-] fraction of the CAPEX
                                     'replacement_cost_LB':  0.4,               #[-] fraction of the CAPEX
                                     'replacement_cost_ref': 0.475,             #[-] fraction of the CAPEX
                                     'replacement_cost_avg': 0.475,             #[-] fraction of the CAPEX
                                     'COP'    :              4.5,               #[MWh_th/MWh_el]  coefficient of performance for the cooling system of the electrolyzer
                                     #economic parameters
                                     'contingency_costs':    0.0,               #[%] of the capex
                                     'development_costs':    0.0,               #[%] of the capex
                                    }
                                             
'________________H2 transmission infrastructure________________'
components['H2_off_new_pipelines'] =     {#technical
                                     'flag':                'OFF',              #boolean to actiate components in LCOH calculation
                                     'd1' :                     91.44,          #[cm] based on 36 inch, common pipeline diameter 
                                     'lifetime' :               50,             # [year]    
                                     #economic     
                                     'specific_CAPEX_ref':      3.6e05,         #[€/km] 
                                     'specific_CAPEX_avg':      4.3e05,         #[€/km] 
                                     'specific_CAPEX_HB':       5.8e05,         #[€/km] 
                                     'specific_CAPEX_LB':       3.6e05,         #[€/km] 
                                     'O&M_ref' :                0.027,          #[-] annual fraction of capex 
                                     'O&M_avg' :                0.027,          #[-] annual fraction of capex 
                                     'O&M_HB' :                 0.07,           #[-] annual fraction of capex 
                                     'O&M_LB' :                 0.008,          #[-] annual fraction of capex 
                                     'replacement_cost_ref':    0,              #[-] fraction of the CAPEX
                                     'replacement_cost_avg':    0,              #[-] fraction of the CAPEX
                                     'replacement_cost_HB':     0,              #[-] fraction of the CAPEX
                                     'replacement_cost_LB':     0,              #[-] fraction of the CAPEX
                                     #economic parameters
                                     'contingency_costs':       0.3,            #[%] of the capex
                                     'development_costs':       0.05,           #[%] of the capex
                                     }   

components['H2_On_new_pipelines'] =     {#technical
                                     'flag':                    'OFF',          #boolean to actiate components in LCOH calculation
                                     'd1' :                     91.44,          #[cm] based on 36 inch, common pipeline diameter 
                                     'lifetime' :               50,             # [year]    
                                     #economic     
                                     'specific_CAPEX_ref':      3.2e05,         #[€/km] 
                                     'specific_CAPEX_avg':      3.2e05,         #[€/km] 
                                       'specific_CAPEX_HB':     8.4e05,         #[€/km] 
                                     'specific_CAPEX_LB':       3.2e05,         #[€/km] 
                                     'O&M_ref' :                0.027,          #[-] annual fraction of capex 
                                     'O&M_avg' :                0.027,          #[-] annual fraction of capex 
                                     'O&M_HB' :                 0.07,           #[-] annual fraction of capex 
                                     'O&M_LB' :                 0.008,          #[-] annual fraction of capex 
                                     'replacement_cost_ref':    0,              #[-] fraction of the CAPEX
                                     'replacement_cost_avg':    0,              #[-] fraction of the CAPEX
                                     'replacement_cost_HB':     0,              #[-] fraction of the CAPEX
                                     'replacement_cost_LB':     0,              #[-] fraction of the CAPEX
                                     'contingency_costs':       0.3,            #[%] of the capex
                                     'development_costs':       0.05,           #[%] of the capex
                                     }   
                                          
components['H2_off_repur_pipelines'] =    {#technical
                                       'flag':                    'OFF',        #boolean to actiate components in LCOH calculation
                                       'd1' :                     91.44,        #[cm] based on 36 inch, common pipeline diameter 
                                       'lifetime' :               50,           # [year] 
                                       #economic     
                                       'specific_CAPEX_ref':      3.6e04,       #[€/km] 
                                       'specific_CAPEX_avg':      5.9e04,       #[€/km] 
                                       'specific_CAPEX_HB':       6.4e04,       #[€/km] 
                                       'specific_CAPEX_LB':       4.0e04,       #[€/km] 
                                       'O&M_ref' :                0.027,        #annual fraction of capex 
                                       'O&M_avg' :                0.027,        #annual fraction of capex 
                                       'O&M_HB' :                 0.07,         #annual fraction of capex 
                                       'O&M_LB' :                 0.008,        #annual fraction of capex 
                                       'replacement_cost_ref':    0,            #[-] fraction of the CAPEX
                                       'replacement_cost_avg':    0,            #[-] fraction of the CAPEX
                                       'replacement_cost_HB':     0,            #[-] fraction of the CAPEX
                                       'replacement_cost_LB':     0,            #[-] fraction of the CAPEX
                                       'contingency_costs':       0.3,          #[%] of the capex
                                       'development_costs':       0.05,         #[%] of the capex
                                       }

components['H2_On_repur_pipelines'] =    {#technical
                                       'flag':                'OFF',                #boolean to actiate components in LCOH calculation
                                       'd1' :                     91.44,            #[cm] based on 36 inch, common pipeline diameter 
                                       'lifetime' :               50,               # [year] 
                                       #economic     
                                       'specific_CAPEX_ref':      3.6e04,           #[€/km] 
                                       'specific_CAPEX_avg':      5.9e04,           #[€/km] 
                                       'specific_CAPEX_HB':       6.4e04,           #[€/km] 
                                       'specific_CAPEX_LB':              4.0e04,    #[€/km] 
                                       'O&M_ref' :                0.027,            #annual fraction of capex 
                                       'O&M_avg' :                0.027,            #annual fraction of capex 
                                       'O&M_HB' :                 0.07,             #annual fraction of capex 
                                       'O&M_LB' :                 0.008,            #annual fraction of capex 
                                       'replacement_cost_ref':    0,                #[-] fraction of the CAPEX
                                       'replacement_cost_avg':    0,                #[-] fraction of the CAPEX
                                       'replacement_cost_HB':     0,                #[-] fraction of the CAPEX
                                       'replacement_cost_LB':     0,                #[-] fraction of the CAPEX
                                       'contingency_costs':       0.3,              #[%] of the capex
                                      'development_costs':       0.05,              #[%] of the capex
                                       }


components['H2_local_pipelines'] =     {#technical
                                        'flag':                'OFF',               #boolean to actiate components in LCOH calculation
                                        'd1' :                  30.48,              #[cm] based on 12 inch, common pipeline diameter 
                                        'lifetime' :            30,                 #[year]  #source
                                        #economic     
                                        'specific_CAPEX_ref':   550e03 ,            #[€/km] --> depends on the size of the pipeline
                                        'specific_CAPEX_avg':   550e03  ,           #[€/km] --> depends on the size of the pipeline
                                        'specific_CAPEX_HB':    900e03 ,            #[€/km] --> depends on the size of the pipeline
                                        'specific_CAPEX_LB':    200e03 ,            #[€/km] --> depends on the size of the pipeline
                                        'O&M_ref':              0.005,              #[-] fraction of the CAPEX
                                        'O&M_avg':              0.005,              #[-] fraction of the CAPEX
                                        'O&M_HB':               0.005,              #[-] fraction of the CAPEX
                                        'O&M_LB':               0.005,              #[-] fraction of the CAPEX
                                        'replacement_cost_ref': 0,                  #[-] fraction of the CAPEX
                                        'replacement_cost_avg': 0,                  #[-] fraction of the CAPEX
                                        'replacement_cost_HB':  0,                  #[-] fraction of the CAPEX
                                        'replacement_cost_LB':  0,                  #[-] fraction of the CAPEX
                                        'contingency_costs':    0.3,                #[%] of the capex
                                        'development_costs':    0.05,               #[%] of the capex
                                        }
                                          
'________________compressors________________'
components['Compressor_on'] =           {
                                        'flag':                'OFF',               #boolean to actiate components in LCOH calculation
                                        'specific_CAPEX_ref':       2.85e06,        #[€/MW] 
                                        'specific_CAPEX_avg':       2.85e06,        #[€/MW] 
                                        'specific_CAPEX_HB':        4.0e6,          #[€/MW] 
                                        'specific_CAPEX_LB':        8.0e5,          #[€/MW] 
                                        'O&M_ref' :                 0.0228,         #[%]
                                        'O&M_avg' :                 0.0228,         #[%]
                                        'O&M_HB' :                  0.04,           #[%]
                                        'O&M_LB' :                  0.017,          #[%]
                                        'lifetime' :                30,             # [year]    Source:    
                                        'replacement_cost_ref':     0,              #[-] fraction of the CAPEX
                                        'replacement_cost_avg':     0,              #[-] fraction of the CAPEX
                                        'replacement_cost_HB':      0,              #[-] fraction of the CAPEX
                                        'replacement_cost_LB':      0,              #[-] fraction of the CAPEX
                                        'contingency_costs':        0.3,            #[%] of the capex
                                        'development_costs':        0.05,           #[%] of the capex
                                        'PEM_ref':                  13.292425,      #[MW] reference compressor size with PEM
                                        'ALK_ref':                  37.494891,      #[MW] reference compressor size with ALK
                                        }

components['Compressor_off'] =           {
                                        'flag':                     'OFF',          #boolean to actiate components in LCOH calculation
                                        'specific_CAPEX_ref':       4.45e06,        #[€/MW] 
                                        'specific_CAPEX_avg':       4.45e06,        #[€/MW] 
                                        'specific_CAPEX_HB':        6.7e6,          #[€/MW] 
                                        'specific_CAPEX_LB':        2.2e6,          #[€/MW] 
                                        'O&M_ref' :                 0.0228,         #[%]
                                        'O&M_avg' :                 0.0228,         #[%]
                                        'O&M_HB' :                  0.04,           #[%]
                                        'O&M_LB' :                  0.017,          #[%]
                                        'lifetime' :                30,             # [year]    Source:    
                                        'replacement_cost_ref':     0,              #[-] fraction of the CAPEX
                                        'replacement_cost_avg':     0,              #[-] fraction of the CAPEX
                                        'replacement_cost_HB':      0,              #[-] fraction of the CAPEX
                                        'replacement_cost_LB':      0,              #[-] fraction of the CAPEX
                                        'contingency_costs':        0.3,            #[%] of the capex
                                        'development_costs':        0.05,           #[%] of the capex
                                        'PEM_ref':                  13.292425,      #[MW] reference compressor size with PEM
                                        'ALK_ref':                  37.494891,      #[MW] reference compressor size with ALK
                                        }
    

'________________electricity_transmission________________'
components['IA_cables'] =               {#technical
                                         'flag':                    'OFF',          #boolean to actiate components in LCOH calculation
                                         'capacity' :               90,             #[MWh] 
                                         'losses':                  0,              #[kWh/km]
                                         'lifetime':                30,             #[y]
                                         #economic     
                                         'specific_CAPEX_ref':      290.5e03,       #[€/km] 
                                         'specific_CAPEX_avg':      290.5e03,       #[€/km] 
                                         'specific_CAPEX_HB':       500e03,         #[€/km] 
                                         'specific_CAPEX_LB':       194e03,         #[€/km] 
                                          'O&M_ref':                0.012,          #[-] fraction of the CAPEX
                                          'O&M_avg':                0.012,          #[-] fraction of the CAPEX
                                         'O&M_HB':                  0.022,          #[-] fraction of the CAPEX
                                         'O&M_LB':                  0.002,          #[-] fraction of the CAPEX
                                         'replacement_cost_ref':    0,              #[-] fraction of the CAPEX
                                         'replacement_cost_avg':    0,              #[-] fraction of the CAPEX
                                         'replacement_cost_HB':     0,              #[-] fraction of the CAPEX
                                         'replacement_cost_LB':     0,              #[-] fraction of the CAPEX
                                         'contingency_costs':       0.05,            #[%] of the capex
                                         'development_costs':       0.05,           #[%] of the capex
                                         }                                                    
                                                                       
components['AC_cables'] =               {#technical
                                         'flag':                    'OFF',          #boolean to actiate components in LCOH calculation
                                         'capacity' :               750,            #[MW]   TenneT
                                         'losses':                  6.7e-05,        #[%/km]
                                         'lifetime':                30,             #[y]
                                         #economic     
                                         'specific_CAPEX_ref':      5.33e06,        #[€/km] related to 180km
                                         'specific_CAPEX_avg':      5.06e06,        #[€/km] related to 180km
                                         'specific_CAPEX_HB':       6.84e06,        #[€/km] related to 180km
                                         'specific_CAPEX_LB':       3e06,           #[€/km] related to 180km
                                          'O&M_ref':                0.015,          #[-] fraction of the CAPEX
                                          'O&M_avg':                0.015,          #[-] fraction of the CAPEX
                                         'O&M_HB':                  0.025,          #[-] fraction of the CAPEX
                                         'O&M_LB':                  0.005,          #[-] fraction of the CAPEX
                                         'replacement_cost_ref':    0,              #[-] fraction of the CAPEX
                                         'replacement_cost_avg':    0,              #[-] fraction of the CAPEX
                                         'replacement_cost_HB':     0,              #[-] fraction of the CAPEX
                                         'replacement_cost_LB':     0,              #[-] fraction of the CAPEX
                                     'contingency_costs':           0.05,            #[%] of the capex
                                     'development_costs':           0.05,           #[%] of the capex
                                         }

components['AC_grid_cables'] =          {#technical
                                         'flag':                    'OFF',              #boolean to actiate components in LCOH calculation
                                         'lifetime':                30,                 #[y]
                                         #economic     
                                         'specific_CAPEX_ref':      5.33e06/1005*37,    #[€/km] related to 180km
                                         'specific_CAPEX_avg':      5.06e06/1005*37,    #[€/km] related to 180km
                                         'specific_CAPEX_HB':       6.84e06/1005*37,    #[€/km] related to 180km
                                         'specific_CAPEX_LB':       3e06/1005*37,       #[€/km] related to 180km
                                         'O&M_ref':                0.015,               #[-] fraction of the CAPEX
                                         'O&M_avg':                0.015,               #[-] fraction of the CAPEX
                                         'O&M_HB':                  0.025,              #[-] fraction of the CAPEX
                                         'O&M_LB':                  0.005,              #[-] fraction of the CAPEX
                                         'replacement_cost_ref':    0,                  #[-] fraction of the CAPEX
                                         'replacement_cost_avg':    0,                  #[-] fraction of the CAPEX
                                         'replacement_cost_HB':     0,                  #[-] fraction of the CAPEX
                                         'replacement_cost_LB':     0,                  #[-] fraction of the CAPEX
                                         'contingency_costs':           0.05,           #[%] of the capex
                                         'development_costs':           0.05,           #[%] of the capex
                                         }

components['AC_electric_substructure'] =    {#economic     
                                          'flag':                   'OFF',          #boolean to actiate components in LCOH calculation
                                          'specific_CAPEX_ref':     345.74e03,      #[€/MW]
                                          'specific_CAPEX_avg':     236.95e03,      #[€/MW]
                                          'specific_CAPEX_HB':      345.74e03,      #[€/MW]
                                          'specific_CAPEX_LB':      186.6e03,       #[€/MW]
                                          'lifetime':               30,             #[y]
                                          'O&M_ref':                0.02,           #[-] fraction of the CAPEX
                                          'O&M_avg':                0.02,           #[-] fraction of the CAPEX
                                          'O&M_HB':                 0.025,          #[-] fraction of the CAPEX
                                          'O&M_LB':                 0.015,          #[-] fraction of the CAPEX
                                     'replacement_cost_ref':        0,              #[-] fraction of the CAPEX
                                     'replacement_cost_avg':        0,              #[-] fraction of the CAPEX
                                          'replacement_cost_HB':    0,              #[-] fraction of the CAPEX
                                          'replacement_cost_LB':    0,              #[-] fraction of the CAPEX
                                     'contingency_costs':           0.05,           #[%] of the capex
                                     'development_costs':           0.05,           #[%] of the capex
                                         }

components['DC_cables'] =               {#technical
                                         'flag':                'OFF',              #boolean to actiate components in LCOH calculation
                                         'capacity' :           2000,               #[MW]   
                                         'losses':              3.5e-05,            #[%/km]
                                         'lifetime':            30,                 #[y]
                                         #economic     
                                         'specific_CAPEX_ref':  1.54e06,            #[€/km]
                                         'specific_CAPEX_avg':  2.8e06,             #[€/km]
                                         'specific_CAPEX_HB':   6.8e06,             #[€/km]
                                         'specific_CAPEX_LB':   8.0e05,             #[€/km]
                                          'O&M_ref':            0.016,              #[-] fraction of the CAPEX
                                          'O&M_avg':            0.016,              #[-] fraction of the CAPEX
                                         'O&M_HB':              0.03,               #[-] fraction of the CAPEX
                                         'O&M_LB':              0.002,              #[-] fraction of the CAPEX
                                         'replacement_cost_HB': 0,                  #[-] fraction of the CAPEX
                                         'replacement_cost_LB': 0,                  #[-] fraction of the CAPEX
                                     'replacement_cost_ref':    0,                  #[-] fraction of the CAPEX
                                     'replacement_cost_avg':    0,                  #[-] fraction of the CAPEX
                                     'contingency_costs':       0.05,               #[%] of the capex
                                     'development_costs':       0.05,               #[%] of the capex
                                         }
    
components['DC_electric_substructure'] =    {#economic     
                                          'flag':                   'OFF',          #boolean to actiate components in LCOH calculation
                                          'specific_CAPEX_ref':     807.75e03,      #[€/MW]
                                          'specific_CAPEX_avg':     685.9e03,       #[€/MW]
                                          'specific_CAPEX_HB':      807.75e03,      #[€/MW]
                                          'specific_CAPEX_LB':      565e03,         #[€/MW]
                                          'lifetime':               30,             #[y]
                                          'O&M_ref':                0.019,          #[-] fraction of the CAPEX
                                          'O&M_avg':                0.019,          #[-] fraction of the CAPEX
                                          'O&M_HB':                 0.023,          #[-] fraction of the CAPEX
                                          'O&M_LB':                 0.015,          #[-] fraction of the CAPEX
                                     'replacement_cost_ref':        0,              #[-] fraction of the CAPEX
                                     'replacement_cost_avg':        0,              #[-] fraction of the CAPEX
                                          'replacement_cost_HB':    0,              #[-] fraction of the CAPEX
                                          'replacement_cost_LB':    0,              #[-] fraction of the CAPEX
                                     'contingency_costs':           0.05,           #[%] of the capex
                                     'development_costs':           0.05,           #[%] of the capex
                                         }

components['H2_substation'] =    {#economic     
                                          'flag':                   'OFF',          #boolean to actiate components in LCOH calculation
                                          'lifetime':               30,             #[y]
                                          'specific_CAPEX_ref':     194.33e03,      #[€/MW] energy platform 
                                          'specific_CAPEX_avg':     194.33e03,      #[€/MW] energy platform 
                                          'specific_CAPEX_HB':      318e03,         #[€/MW] energy platform 
                                          'specific_CAPEX_LB':      141e03,         #[€/MW] energy island 
                                          'O&M_ref':                0.006,          #[-] fraction of the CAPEX
                                          'O&M_avg':                0.006,          #[-] fraction of the CAPEX
                                          'O&M_HB':                 0.01,           #[-] fraction of the CAPEX
                                          'O&M_LB':                 0.002,          #[-] fraction of the CAPEX
                                     'replacement_cost_ref':        0,              #[-] fraction of the CAPEX
                                     'replacement_cost_avg':        0,              #[-] fraction of the CAPEX
                                          'replacement_cost_HB':    0,              #[-] fraction of the CAPEX
                                          'replacement_cost_LB':    0,              #[-] fraction of the CAPEX
                                     'contingency_costs':           0.3,            #[%] of the capex
                                     'development_costs':           0.05,           #[%] of the capex
                                         }

components['H2_onshore'] =    {#economic     
                                          'flag':                   'OFF',          #boolean to actiate components in LCOH calculation
                                          'lifetime':               30,             #[y]
                                          'specific_CAPEX_ref':     0,              #[€/MW] energy platform 
                                          'specific_CAPEX_avg':     0,              #[€/MW] energy platform 
                                          'specific_CAPEX_HB':      0,              #[€/MW] energy platform 
                                          'specific_CAPEX_LB':      0,              #[€/MW] energy island 
                                          'O&M_ref':                0,              #[-] fraction of the CAPEX
                                          'O&M_avg':                0,              #[-] fraction of the CAPEX
                                          'O&M_HB':                 0,              #[-] fraction of the CAPEX
                                          'O&M_LB':                 0,              #[-] fraction of the CAPEX
                                          'replacement_cost_ref':   0,              #[-] fraction of the CAPEX
                                          'replacement_cost_avg':   0,              #[-] fraction of the CAPEX
                                          'replacement_cost_HB':    0,              #[-] fraction of the CAPEX
                                          'replacement_cost_LB':    0,              #[-] fraction of the CAPEX
                                          'contingency_costs':      0,              #[%] of the capex
                                          'development_costs':      0,              #[%] of the capex
                                         }

'________________BESS________________'
components['BESS'] =                    {#technical
                                         'flag':                    'OFF',          #boolean to actiate components in LCOH calculation
                                         'lifetime':                30,             #[y]
                                         #economic     
                                         'specific_CAPEX_':         190,            #[€/kWh]
                                         'O&M_':                    0.01,           #[-] fraction of the CAPEX
                                         'O&M_HB':                  0.01,           #[-] fraction of the CAPEX
                                         'O&M_LB':                  0.01,           #[-] fraction of the CAPEX
                                          'replacement_cost_':      0.7,            #[-] fraction of the CAPEX
                                          'replacement_cost_HB':    0.7,            #[-] fraction of the CAPEX
                                          'replacement_cost_LB':    0.7,            #[-] fraction of the CAPEX
                                         }

#################################################################################################################################à
'_______________________________________energy_______________________________________'
energy= {}

energy['H2']=           {'LHV' : 0.0333, #[MWh/kg]
                         'O2_prod':             8,                 #[kg_O2/kg_H2] Oxigen produztion
                         'H2O_cons':            9,                 #[kg_H2O/kg_H2] Water consumption
                         
                        }

energy['H2O'] =         {'cost':0.95/1e03,           #[€/kg] cooling and processing on water
                        }

energy['electricity']=  {'purchase price from grid':   100,                #[€/MWh] (TBD)
                        }

