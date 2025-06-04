import pandas as pd

#%%
###########################################################################################################################################

'MAIN'

def simplified_sim(df_NorthSea, EL_P_nom, components, energy, EL, kWh_factor, L_pipe, EX_length, IA_length, eta_rect, cables, bound_tech):
    
    T_EXT = 20 #[15°C]
    'power fluxes'
    #available power form RES     
    P_RES = df_NorthSea['Wind Power [kW]'] #[kW] wind power source
   

    'ALK ELECTROLYZER'
    if EL == 'ALK' : 
        from Electrolyzer.MODEL_ALK import alk_EL_model as EL_model
        from Electrolyzer.MODEL_ALK import alk_EL_transit as EL_transit
    'PEM ELECTROLYZER'
    if EL == 'PEM' : 
        from Electrolyzer.MODEL_PEM import pem_EL_model as EL_model
        from Electrolyzer.MODEL_PEM import pem_EL_transit as EL_transit

    #power required by the alkaline electrolyzer to start the hydrogen production [kW]
    EL_P_min = components[EL]['cell_min_power'] * EL_P_nom 
    #new electrolyzer condition
    EL_h_work = 0 #[h]
    # intial electrolyzer temperature
    EL_T_0 = components[EL]['T_op']               #[°C]
    # electrolyzer nominal mass flow
    nom_mass_flow = components[EL]['nom_mass_flow_' + bound_tech] #[kWh/kg]
    # electrolyzer time degradation factor
    degr = components[EL]['degr_time_' + bound_tech] #[V/h]
    
    EL_T_list = [EL_T_0]
    CS_factor = int(max(1,components[EL]['CS']/(60/kWh_factor))) #[min] cold startup time 
    switch = 1
        
    'lists initialization'
    P_compr             = []             
    P_RO                = []
    EL_H2_prod          = []
    EL_q_prod           = []
    EL_cooling_w        = []
    EL_CF_list          = []
    EL_P_recieved_list  = []
    H2O_feed_list       = []
    H2O_brine_list      = []
    O2_prod_list        = []
    EL_subst            = []
    P_aux               = []
    P_grid              = []
    P_used              = []
    
    'electricity transmission losses'
    EL_tr_losses = (EX_length * components[cables]['losses'] + IA_length * components['IA_cables']['losses']) #[kW]
    
    'for loop for each timestep of the timeframe'
    for i in range(len(P_RES)):
        
        #########################################################
        'load estimation'
        P_requested = EL_P_nom #[kW]
        #########################################################
        'conversion step AC-DC for wind farm power'
        
        P_avail = min(P_requested, (P_RES.iloc[i] * (1 - EL_tr_losses) * eta_rect)) #[kW]
        
        #power to the electrolyzer
        EL_P_given = P_avail    #[kW]
                         
        'electrolyzer operation' #EL
        EL_P_recieved_list.append(EL_P_given) #[kW]
 
        #conversion factor update
        EL_CF, EL_f_i_V, EL_f_H2_i, V_array, W_compr, Replacement = EL_model(EL_T_list[i], EL_h_work, kWh_factor, nom_mass_flow, degr)
        
        #trend of the conversion factor
        EL_CF_list.append(EL_CF) # [kg/kWh]    
        
        H2_producible = EL_P_recieved_list[i] * EL_CF / kWh_factor #[kg] h2 prod
        H2O_producible = (H2_producible * EL_CF / kWh_factor) * energy['H2']['H2O_cons'] / components['RO_unit']['Rec_f'] # [kg] water    
        
        'Thermal management'
        EL_T, q = EL_transit(H2_producible/(EL_P_nom/1e03), EL_f_i_V, EL_f_H2_i, EL_T_list[i], T_EXT, kWh_factor) 
        EL_T_list.append(EL_T)    #[°C] electrolyzer temperature evolution in time
        
        W_cool = q / components[EL]['COP'] #[kW] cooling power required
        W_RO = H2O_producible * components['RO_unit']['Conv_f'] #[kW] power of the RO system
        P_expl = EL_P_given - (W_cool +W_RO) #[kW] exploited RES power
        
        #if minimum electrolyzer power is not met                  
        if P_expl< EL_P_min:
            W_cool = 0
            W_RO = 0
            P_expl = 0
            
        EL_H2_prod.append(switch * P_expl * EL_CF / kWh_factor) #[kg]
        P_RO.append(W_RO)     #[kW]
        EL_cooling_w.append(W_cool)  #[kW] electrolyzer cooling power from an electric chiller
        P_aux.append((W_RO + W_cool) / kWh_factor) #[kW] auxiliary power 
        P_compr.append(W_compr* P_expl)          #[kW]
        P_grid.append(W_compr* P_expl)          #[kW] grid power
        P_used.append(P_expl)                   #[kW] exploited power
        H2O_feed_list.append((P_expl * EL_CF / kWh_factor) * energy['H2']['H2O_cons'] / components['RO_unit']['Rec_f']) #[kg]
        H2O_brine_list.append((P_expl * EL_CF / kWh_factor) * energy['H2']['H2O_cons'] * ( 1/ components['RO_unit']['Rec_f'] -1 )) #[kg]
        O2_prod_list.append((P_expl * EL_CF / kWh_factor) * energy['H2']['O2_prod'])   #[kg]
        print('sim adv:',i/len(P_RES)*100, '%')
        
        if sum(EL_T_list[i+1-CS_factor:i+1]) >= CS_factor * components[EL]['T_op']: switch = 1
        EL_q_prod.append(q*(EL_P_nom/1e03)/1000) #electrolyzer cooling heat evolution in time
        # #working hours counting only if activated
        if EL_H2_prod[i] > 0:
            EL_h_work = EL_h_work + 1/kWh_factor
        
        'electolyzer replacement'
        if Replacement == True:
            EL_subst.append(1)
            EL_h_work = 0
        else:
            EL_subst.append(0)

        
    'Data saving after the for loop'
    annuality_factor = len(P_RES)/kWh_factor/8760                              #[-] coefficient used to obtain the annual value of the magnitudes above
    E_aux_y = (sum(P_aux) / kWh_factor / annuality_factor) / 1000              #[MWh/y]  yearly wind farm contribution to cooling and desalination production
    E_grid_y = (sum(P_grid) / kWh_factor / annuality_factor) / 1000            #[MWh/y]  yearly grid contribution to compression 
    E_res_y = (sum(EL_H2_prod) / EL_CF / annuality_factor) / 1000              #[MWh/y]  yearly RES contribution to H2 production
    H2_prod_y = (sum(EL_H2_prod) / annuality_factor)                           #[kg/y] yearly H2 production  
    H2O_feed_y = (sum(H2O_feed_list) / annuality_factor)                       #[kg/y] yearly H2O consumption  
    H2O_brine_y = (sum(H2O_brine_list) / annuality_factor)                     #[kg/y] yearly H2 production  
    O2_prod_y = (sum(O2_prod_list) / annuality_factor)                         #[kg/y] yearly H2 production  
    E_used_y = (sum(P_used) / kWh_factor / annuality_factor)/ 1000

    'output'
    output = pd.DataFrame()
    output['EL_Power [MW]'] =       [EL_P_nom / 1e03]
    output['E_expl [MWh/y]'] =      [E_used_y]    
    output['E_aux[MWh/y]'] =        [E_aux_y]
    output['E_grid[MWh/y]'] =       [E_grid_y]
    output['E_res[MWh/y]'] =        [E_res_y] 
    output['H2_prod_EL[kg/y]'] =    [H2_prod_y]
    output['H2O_feed[kg]']=         [H2O_feed_y]
    output['O2_prod[kg]']=          [O2_prod_y]
    output['H2O_brine[kg]']=        [H2O_brine_y]
    
    'output time dependent'
    output_td = pd.DataFrame()
    output_td['time stamp'] =           df_NorthSea['Time Stamp']
    output_td['P_res[MW]'] =            [x / 1000 for x in P_RES]     
    output_td['P_EL[MW]'] =             [x / 1000 for x in EL_P_recieved_list]     
    output_td['P_Effective_EL[MW]'] =   [x / 1000 for x in P_used]     
    output_td['P_aux[MW]'] =            [x / 1000 for x in P_aux]  
    output_td['P_grid[MW]'] =           [x / 1000 for x in P_grid]  
    output_td['Cooling_power_EL[MW]'] = [x / 1000 for x in EL_cooling_w] 
    output_td['Compr_power[MW]'] =      [x / 1000 for x in P_compr]   
    output_td['RO_power[MW]'] =         [x / 1000 for x in P_RO]      
    output_td['T_EL[°C]'] =             EL_T_list[1:len(EL_T_list)]  
    output_td['H2_prod_EL[kg]'] =       EL_H2_prod
    output_td['H2O_feed[kg]']=          H2O_feed_list
    output_td['O2_prod[kg]']=           O2_prod_list
    output_td['H2O_brine[kg]']=         H2O_brine_list
    output_td['el_replacements [-]']=   EL_subst

    return output, output_td

