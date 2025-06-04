import numpy as np
import math
from scipy import interpolate

V_array_ideal = np.array([1.642,1.89])
i_array_ideal = np.array([2,10.02])              #current density [kA/m2]

def alk_EL_model(T_el, h_work_tot, kWh_factor, H2_design, V_degr, i_array_ideal = i_array_ideal, V_array_ideal = V_array_ideal):
    '''
    conv_factor : Efficienza di conversione Power to H2.
    f_i_V : Funzione per passare da corrente a voltaggio.
    f_H2_i : Funzione per passare da H2 production a corrente .
    V_array : Array contenente il Min e max voltaggio.
    '''
    Replacement = False
    W_cell = 9.45                      #[kW] nominal cell power
    n_cells_design = 106               # number of cells in the 1MW stack
    SF = 1        # scale factor of the configuration
    
    H2_design = (W_cell*n_cells_design)/H2_design         # [kg/h] nominal produced hydrogen flow from the 1MW module 17.98
    
    'aux Power'
    W_RO = 0.115352292      #[kW] power consumption osmosis unit
    W_compr = 0.037494891   #[kW] power consumption compressor 
    W_cool = 0.055233978    #[kW] power comsumption cooling system
    W_aux = W_RO + W_cool                     #[kW] total power consumption auxiliaries
    
    T_operation = 71
    # V_degr = 3 * 10 ** -6     # uV/h time voltage increase
    V_T = 5 * 10 ** -3        # 5mV/°C cool down voltage increase
    S_cell = 0.5              # m^2 surface of cells


    #cell voltage = stack voltage / n_cells
    V_array     = V_array_ideal + V_degr * h_work_tot + V_T*(T_operation - T_el)
    V_repl      = (V_array_ideal) * 1.2
    if max(V_array_ideal + V_degr * h_work_tot) >= max(V_repl): 
        Replacement = True
        print('High voltage, new electrolyzer  needed')
                
    #cell current = stack current 
    I_array     = i_array_ideal*S_cell     
    
    #H2 production array of the stack = n_cells * H2 production of a cell
    H2_array    = np.array([0, H2_design * SF])
    
    #link between cell current (= stack current) and cell voltage: polarization curve
    f_i_V = interpolate.interp1d(I_array,V_array)

    #link between stack H2 production and stack current (= cell current)                 
    f_H2_i = interpolate.interp1d(H2_array/kWh_factor,I_array)   
    
    #conversion factor calculation: H2 stack production / P stack consumption
    conv_factor = max(H2_array)/ (max(I_array) * max(V_array) * n_cells_design + (W_cell * n_cells_design) * W_aux)      # [kg/kWh]    
    
    return conv_factor, f_i_V, f_H2_i, V_array, W_RO, W_compr, W_cool, W_aux, Replacement



def alk_EL_transit(H2_prod,f_i_V, f_H2_i, T_el, T_ext, kWh_factor):
    
    '''
    Themal model: exothermic reaction (heat production from thermal lossess DeltaV = V-Vtn)  
    T_el : electrolyzer temperature
    '''
    
    n_cells_design = 106               # number of cells in the 1MW module
    L_design = 3                       # [m] design length of the gas-liquid separator
    r1_design = 0.3                    # [m] internal radius
    
    SF = 1        # scale factor della configurazione, lo applico al volume
    
    L = L_design * SF**(1/3)           # scale of the geometry accoring to the SF
    
    pi = math.pi
    op_time = (60*60)/(kWh_factor)       # [s]  simulation time in seconds
    T_op = 71                            # [°C] operating temperature
    # T_ext = 25                         # [°C] external temperature, activate in case 
        
    V_tn = 1.48                        # [V]  thermoneutral voltage
    
    'geometry'
    r1 = r1_design * SF**(1/3)          
    s1 = 0.004                          # [m] thickness of the electrolyzer container
    
    r3 = 1             # [m]  container internal radius
    s2 = 0.005         # [m] container thickness
    
    'heat coefficeints'
    h1 = 100          # [W/ m^2K]   internal convection between water (H2O + 30% KOH) - tank
    h2 = 10           # [W/ m^2K]   convection tank-container
    h3 = 20           # [W/ m^2K]   external convection container-air
    
    k1 = 52           # [W/ mK] steel tank conduction 
    k2 = 52           # [W/ mK] steel container conduction     
    
    'instulated container'
    insulation = True
    if insulation == True:
        s2 = 0.1     # [m]     insulation layer thickness (0.2 m design value)

        k2 = 0.05    # [W/ mK] insulation layer conduction
        
    
    'electrolyte'
    m_elect = L * r1 * r1 * pi * 1000 / 2 # [kg] of H2O in gas-liquid separator (half water, half gas)
    c_elect = 4190                        # [J/kg*K]   water specific heat

    a = h1*2*pi*r1*L
    b = k1*2*pi*L/np.log((r1 + s1)/r1)   
    c = h2*2*pi*(r1 + s1)*L
    d = h2*2*pi*r3*L
    e = k2*2*pi*L/np.log((r3 + s2)/r3)
    f = h3*2*pi*(r3 + s2)*L
    
    q_lost = (T_el - T_ext) / (1/a + 1/b + 1/c + 1/d + 1/e + 1/f) # [W] thermal power lost to the environment

    if H2_prod > 0:  
        #stack current from H2 production
        I_op = f_H2_i(H2_prod)
        #cell voltage from cell current (= stack current)
        V_op = f_i_V(I_op)
        
        #thermal power generated form the stack
        q_gain = n_cells_design * (V_op-V_tn)*I_op*1000     # [V]*[kA]*1000 = [V]*[A] = [W] produce thermal power
                
        Tx = T_el + (op_time / (m_elect * c_elect)) * (q_gain - q_lost)
    
        if Tx > T_op:
            Tx = T_op
        
        q_cool = q_gain - q_lost #[W] cooling power needed

    else:
        Tx = T_el - (op_time / (m_elect * c_elect)) * q_lost
        q_cool = 0
        
    return Tx, q_cool
    

#%%

'PLOTS'

electrolyzer_plots = False

if electrolyzer_plots == True:
    import matplotlib.pyplot as plt
    
    
    'funzioni ideali'
    V_array_ideal = np.array([1.642,1.89])
    i_array_ideal = np.array([2,10])
    H2_array_ideal = np.array([0,18])
    
    f_i_V_id = interpolate.interp1d(i_array_ideal,V_array_ideal) 
    f_H2_i_id = interpolate.interp1d(H2_array_ideal,i_array_ideal)
    x_i_id = np.arange(i_array_ideal[0],i_array_ideal[1]+0.01, 0.01)
    x_H2_id = np.arange(H2_array_ideal[0],(H2_array_ideal[1]), 0.01)
    y_i_id = f_H2_i_id(x_H2_id)
    y_v_id = f_i_V_id(x_i_id)
    
    #%%
    
    'ideal voltage curve'
    plt.figure(figsize = (6,4))
    plt.plot(x_i_id,y_v_id)
    plt.grid(alpha = 0.3)
    plt.ylim(1.4,2)
    plt.ylabel('Voltage [V]') #,fontsize=15, labelpad=15,fontweight="bold")
    plt.xlabel('Current denisty [kA/$\mathregular{m^2}$]') #,fontsize=15, labelpad=15,fontweight="bold")
    plt.title('Voltage vs Current density - ideal curve') #,fontsize=15,fontweight="bold")
    
    plt.xlim(2,10)
    
        
    #%%
    
    'ideal h2 production curve'
    plt.figure(figsize = (6,4))
    plt.plot(x_H2_id,y_i_id)
    plt.grid(alpha = 0.3)
    plt.ylabel('Current density [kA/$\mathregular{m^2}$]') #,fontsize=15, labelpad=15,fontweight="bold")
    plt.xlabel('H2 production per module [kg/h]') #,fontsize=15, labelpad=15,fontweight="bold")
    plt.title('Current density vs $\mathregular{H_2}$ production - ideal curve') #,fontsize=15,fontweight="bold")
    plt.ylim(0,11)
    plt.xlim(0,18)
    
            
    #%%
    
    ''' curve di degradazione '''
    'temperature degradation'
    from colour import Color

    T_operation = 71
    V_T = 5 * 10 ** -3        # 5mV/°C degradazione per raffreddamento
    
    color1 = Color("#05a3f7")

    colori = (list(color1.range_to("#f70521",7)))

    hex_list = list()
    
    for i in range(len(colori)):
        hex_list.append(str(colori[i]))   

    j=0
    
    plt.figure(figsize = (6,6))
    T_el = np.arange(10,80,10)
    for i in range(len(T_el)):
        V_degr_T = V_array_ideal + V_T*(T_operation - T_el[i])
        f_i_V = interpolate.interp1d(i_array_ideal,V_degr_T) 
        x_i = np.arange(i_array_ideal[0],i_array_ideal[1]+1, 1)
        y_v = f_i_V(x_i)
        plt.plot(x_i,y_v, label= '%d °C' %(T_el[i]), color = hex_list[j])
        j = j + 1
    
    plt.grid(alpha = 0.3)
    legend_properties = {'size':8}
    plt.legend(prop=legend_properties,edgecolor='black',framealpha=0.5, loc='lower right', ncol = 2) 
    plt.ylabel('Voltage [V]') #,fontsize=15, labelpad=15,fontweight="bold")
    plt.xlabel('Current density [kA/$\mathregular{m^2}$]') #,fontsize=15, labelpad=15,fontweight="bold")
    
    plt.xlim(2,10)
    
    #plt.title('Operating Temperature influence on Polarization curve') #,fontsize=15,fontweight="bold")
    
    #%%
    
    'time degradation' 
    V_degr = 3 * 10 ** -6     # uV/h degradazione nel tempo
    
    color1 = Color("blue")

    colori = (list(color1.range_to("brown",7)))

    hex_list = list()
    
    for i in range(len(colori)):
        hex_list.append(str(colori[i]))   

    j=0
    
    plt.figure(figsize = (6,6))
    h_work_tot = np.arange(0,12*24*365,2*24*365)
    for i in range(len(h_work_tot)):
        V_degr_time = V_array_ideal + V_degr * h_work_tot[i]
        f_i_V = interpolate.interp1d(i_array_ideal,V_degr_time) 
        x_i = np.arange(i_array_ideal[0],i_array_ideal[1]+1, 1)
        y_v = f_i_V(x_i)
        plt.plot(x_i,y_v, label= '%d years' %(h_work_tot[i]/365/24),  color = hex_list[j])
        j = j + 1
    
    plt.grid(alpha = 0.3)
    legend_properties = {'size':8} #,'weight':'bold'.
    plt.legend(prop=legend_properties,edgecolor='black',framealpha=0.5, loc='lower right', ncol = 2) 
    plt.ylabel('Voltage [V]') #,fontsize=15, labelpad=15,fontweight="bold")
    plt.xlabel('Current density [kA/$\mathregular{m^2}$]') #,fontsize=15, labelpad=15,fontweight="bold")
    plt.xlim(2,10)

    
    #plt.title('Working time influence on Polarization curve') #,fontsize=15,fontweight="bold")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
