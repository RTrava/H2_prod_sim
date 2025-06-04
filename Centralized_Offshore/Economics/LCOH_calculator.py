# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 16:26:20 2024

@author: travaglini
"""

import pandas as pd


def LCOH_func(sizes, components, EL, energy, r, lifetime, SF, cables, bound, rep):
   
    'lists inizialisation'    
    techs_list = []
    CAPEX_O = []
    price_list = []
    oem_price_list = []
    comp_inst_cap = []
        
    components[EL]['size']                      =   sizes['EL']             # MW
    components['WT']['size']                    =   sizes['WF']             # MWp
    components['Compressor_off']['size']        =   sizes['Compressor_off'] # MWp
    components['RO_unit']['size']               =   sizes['RO_unit']        # m3/d
    components['IA_cables']['size']             =   sizes['IA_Cables']      # km
    components['AC_grid_cables']['size']        =   sizes['H2_pipe_off']    # km
    components['H2_substation']['size']         =   sizes['substation']
    
    # 'repourposed pipelines'
    if rep:
        components['H2_off_repur_pipelines']['size']       =   sizes['H2_pipe_off']     # km 
        components['H2_On_repur_pipelines']['size']        =   sizes['H2_pipe']         # km
        components['H2_off_repur_pipelines']['flag']       =   'ON'
        components['H2_On_repur_pipelines']['flag']        =   'ON'
        components['H2_off_new_pipelines']['flag']         =   'OFF'
        components['H2_On_new_pipelines']['flag']          =   'OFF'

    # 'new pipelines'
    else:
        components['H2_off_new_pipelines']['size']      =   sizes['H2_pipe_off']    # km 
        components['H2_On_new_pipelines']['size']       =   sizes['H2_pipe']        # km
        components['H2_off_new_pipelines']['flag']      =   'ON'
        components['H2_On_new_pipelines']['flag']       =   'ON'
        components['H2_off_repur_pipelines']['flag']       =   'OFF'
        components['H2_On_repur_pipelines']['flag']        =   'OFF'

    # component activation for economic calculations
    components[EL]['flag']                      =   'ON'
    components['WT']['flag']                    =   'ON'
    components['Compressor_off']['flag']        =   'ON'
    components['RO_unit']['flag']               =   'ON'
    components['IA_cables']['flag']             =   'ON'
    components['AC_grid_cables']['flag']        =   'ON'
    components['H2_substation']['flag']         =   'ON'
    
    'hydrogen production'
    H2_y = float(energy['H2']['H2_prod_EL[kg/y]'])                #[kg/y] Annual hydrogen output 

    'electricity request/production'
    E_purchased_y   = float(energy['electricity']['E_purch[MWh/y]']) #[MWh/y]
    
    'brine disposal'
    brine_y = float(energy['H2O']['brines[kg/y]']) #[kg/y]

    N = lifetime + 1        #[y] plant lifetime  
    OeM_y = 0               #[€] OEM initialization
    I0 = 0                  #[€] investment cost initialization
    
    for tech in components:
        if components[tech]['flag'] == 'ON':
            if tech == EL:
                component_cost = components[tech]['specific_CAPEX_'+bound] * components[tech]['ref_size'] *(components[tech]['size']/components[tech]['ref_size'])**SF * (1 + components[tech]['contingency_costs'] + components[tech]['development_costs']) #[€] investment cost initialization
            else: 
                component_cost = float(components[tech]['size'] * components[tech]['specific_CAPEX_'+bound]) * (1 + components[tech]['contingency_costs'] + components[tech]['development_costs']) #[€] component cost estimation 
            
            brine_costs = brine_y * components['RO_unit']['brine_disp_off'] #[€] brine disposal costs
            CAPEX_O.append(component_cost)
            OeM_costs = component_cost * components[tech]['O&M_'+bound]
            
            techs_list.append(tech)

            if tech == EL: price_list.append(component_cost + component_cost * round(lifetime/components[tech]['lifetime']) * components[tech]['replacement_cost_'+bound])
            else: price_list.append(component_cost)

            oem_price_list.append(OeM_costs*25)
            comp_inst_cap.append(float(components[tech]['size']))
            #total investment cost
            I0 = I0 + component_cost
            #total annual cost for Operation and Maintenance
            OeM_y = OeM_y +  OeM_costs
   
    techs_list.append('brine_disp')
    price_list.append(0)
    CAPEX_O.append(0)
    comp_inst_cap.append(0)
    oem_price_list.append(brine_costs*25)
    OeM_y += brine_costs

    techs_list.append('grid_energy')
    price_list.append(0)
    CAPEX_O.append(0)
    comp_inst_cap.append(0)
    oem_price_list.append(E_purchased_y * energy['electricity']['purchase price from grid']*25)

    CAPEX_list   = []
    OeM_list     = []
    H2_list = []
    
    for n in range(N):
        if n == 0:
            CAPEX_list.append(I0)
            OeM_list.append(0)
            H2_list.append(0)
            
        else:
            CAPEX_list.append(0)
            OeM_list.append( (OeM_y + E_purchased_y * energy['electricity']['purchase price from grid']) / ((1+r)**n) )
            H2_list.append( (H2_y) / ((1+r)**n) )
            
            #replacement cost
            for tech in components:
                if n%components[tech]['lifetime'] == 0 and components[tech]['flag'] == 'ON':
                    if tech == EL:
                        component_cost = components[tech]['specific_CAPEX_'+bound] * components[tech]['ref_size'] *(components[tech]['size']/components[tech]['ref_size'])**SF
                    else: 
                        component_cost = float(components[tech]['size'] * components[tech]['specific_CAPEX_'+bound])

                    CAPEX_list[n] += component_cost * components[tech]['replacement_cost_'+bound]
    
    costs = pd.DataFrame()
    dfLCOH = pd.DataFrame()
    
    dfLCOH['CAPEX'] = CAPEX_list
    dfLCOH['OeM']   = OeM_list
    dfLCOH['NUM']   = dfLCOH['CAPEX'] + dfLCOH['OeM']
    dfLCOH['H2']    = H2_list
    LCOH = sum(dfLCOH['NUM']) / sum(dfLCOH['H2'])

    LCOH_BD = [(x+y) / sum(price_list + oem_price_list) * 100 for x,y in zip(price_list, oem_price_list)]
    
    costs['component[-]']   = techs_list
    costs['size']           = comp_inst_cap
    costs['CAPEX [€]']       = CAPEX_O
    costs['price[€]']       = price_list
    costs['LCOH_breakdown [%]'] = LCOH_BD    
    
    return LCOH, dfLCOH, costs













