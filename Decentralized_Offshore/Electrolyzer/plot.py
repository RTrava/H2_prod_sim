# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 13:44:26 2024

@author: travaglini
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from matplotlib.lines import Line2D

'PEM'
i_p =[0.000001, 0.004350739, 0.008825151, 0.021180363, 0.035741866, 0.06177606, 0.09266409, 0.19944842, 0.40242693, 2.4]#[A/cm^2]
I_p =[0.00001, 0.04350739, 0.08825151, 0.21180363, 0.35741866, 0.6177606, 0.9266409, 1.9944842, 4.0242693, 24]          #[kA/m^2]
v8_p =[1.2, 1.361619, 1.4071537, 1.4423953, 1.4717538, 1.4952273, 1.5186986, 1.5636317, 1.6005498, 1.9983677]

D = 4e-3
v8_p =np.array([1.2, 1.361619, 1.4071537, 1.4423953, 1.4717538, 1.4952273, 1.5186986, 1.5636317, 1.6025498, 1.9983677])
v7_p = v8_p + D * 10
v6_p = v8_p + D * 20
v5_p = v8_p + D * 30
v4_p = v8_p + D * 40
v3_p = v8_p + D * 50
v2_p = v8_p + D * 60
v1_p = v8_p + D * 70

I_a = [2,10] #current density [kA/m2]

'ALK'
D = 5e-3
v7 = np.array([1.642,1.89])
v6 = v7 + D * 10
v5 = v7 + D * 20
v4 = v7 + D * 30
v3 = v7 + D * 40
v2 = v7 + D * 50
v1 = v7 + D * 60
I_a = [2,10] #current density [kA/m2]


fig, (ax0, ax1) = plt.subplots(1, 2, dpi=300, sharey=True, figsize=(9, 3))
# plot input data
ax0.plot(I_a, v1, c='darkblue')
ax0.plot(I_a, v2, c='blue')
ax0.plot(I_a, v3, c='purple')
ax0.plot(I_a, v4, c='royalblue')
ax0.plot(I_a, v5, c='deepskyblue')
ax0.plot(I_a, v6, c='lightblue')
ax0.plot(I_a, v7, c='gold')
ax0.set_xlim(2, 10)
ax0.set_ylim(1.5, 2.2)
ax0.grid(alpha=0.3)
ax0.set_xlabel('I [kA/m^2]')
ax0.set_ylabel('V [V]')
ax0.set_title('ALK')

ax1.plot(I_p, v1_p, c='darkblue')
ax1.plot(I_p, v2_p, c='blue')
ax1.plot(I_p, v3_p, c='purple')
ax1.plot(I_p, v4_p, c='royalblue')
ax1.plot(I_p, v5_p, c='deepskyblue')
ax1.plot(I_p, v6_p, c='lightblue')
ax1.plot(I_p, v7_p, c='gold')
ax1.plot(I_p, v8_p, c='orange')
ax1.set_xlim(2, 10)
ax1.set_ylim(1.5, 2.2)
ax1.grid(alpha=0.3)
ax1.set_xlabel('I [kA/m^2]')
ax1.set_title('PEM')

legend_elements1 = [Line2D([0], [0], label='10°C', color='darkblue', linewidth=4),
					Line2D([0], [0], label='20°C', color='blue', linewidth=4),
					Line2D([0], [0], label='30°C', color='purple', linewidth=4),
					Line2D([0], [0], label='40°C', color='royalblue', linewidth=4),
					Line2D([0], [0], label='50°C', color='deepskyblue', linewidth=4),
					Line2D([0], [0], label='60°C', color='lightblue', linewidth=4),
					Line2D([0], [0], label='70°C', color='gold', linewidth=4),
					Line2D([0], [0], label='80°C', color='orange', linewidth=4),                   
                    # Line2D([0], [0], marker = 'o', color='w', label='Measured', markerfacecolor='k', markersize=8),
                    ]


leg1=ax0.legend(handles=legend_elements1, loc='upper center', bbox_to_anchor=(1, -0.2), ncol=10, fontsize=8, title='Temperature: [°C]', title_fontsize=10)

plt.subplots_adjust(wspace=0.08)