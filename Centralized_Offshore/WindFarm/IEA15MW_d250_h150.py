from py_wake import np
from py_wake.wind_turbines import WindTurbine
from py_wake.wind_turbines.power_ct_functions import PowerCtTabular


power_curve = np.array([[0, 0],
                        [2, 0],
                        [3, 39.46],
                        [3.55, 291.55],
                        [4.07, 609.95],
                        [4.55, 986.48],
                        [5.01, 1410.4],
                        [5.42, 1869.3],
                        [5.81, 2349.3],
                        [6.15, 2835.5],
                        [6.46, 3312.7],
                        [6.73, 3765.7],
                        [6.97, 4180.2],
                        [7.16, 4547.5],
                        [7.31, 4855.7],
                        [7.43, 5091.9],
                        [7.5, 5248.9],
                        [7.53, 5321.2],
                        [7.54, 5335.8],
                        [7.59, 5438.3],
                        [7.68, 5631.7],
                        [7.8, 5921.4],
                        [7.97, 6315.6],
                        [8.18, 6825 ],
                        [8.42, 7463.4],
                        [8.71, 8239 ],
                        [9.03, 9168.7],
                        [9.39, 10286],
                        [9.78, 11618],
                        [10.21, 13195],
                        [10.66, 15000],
                        [10.67, 15000],
                        [11.17, 15000],
                        [11.7, 15000],
                        [12.26, 15000],
                        [12.85, 15000],
                        [13.47, 15000],
                        [14.11, 15000],
                        [14.78, 15000],
                        [15.47, 15000],
                        [16.19, 15000],
                        [16.92, 15000],
                        [17.67, 15000],
                        [18.45, 15000],
                        [19.23, 15000],
                        [20.03, 15000],
                        [20.84, 15000],
                        [21.66, 15000],
                        [22.49, 15000],
                        [23.32, 15000],
                        [24.16, 15000],
                        [25, 15000]])
ct_curve = np.array([[0, 0],
                    [2, 0],
                    [3, 0.817],
                    [3.55, 0.79],
                    [4.07, 0.784],
                    [4.55, 0.786],
                    [5.01, 0.788],
                    [5.42, 0.789],
                    [5.81, 0.789],
                    [6.15, 0.787],
                    [6.46, 0.785],
                    [6.73, 0.782],
                    [6.97, 0.78],
                    [7.16, 0.776],
                    [7.31, 0.776],
                    [7.43, 0.776],
                    [7.5, 0.776],
                    [7.53, 0.776],
                    [7.54, 0.776],
                    [7.59, 0.776],
                    [7.68, 0.776],
                    [7.8, 0.776],
                    [7.97, 0.776],
                    [8.18, 0.776],
                    [8.42, 0.776],
                    [8.71, 0.776],
                    [9.03, 0.776],
                    [9.39, 0.776],
                    [9.78, 0.776],
                    [10.21, 0.776],
                    [10.66, 0.769],
                    [10.67, 0.743],
                    [11.17, 0.56],
                    [11.7, 0.462],
                    [12.26, 0.388],
                    [12.85, 0.329],
                    [13.47, 0.281],
                    [14.11, 0.241],
                    [14.78, 0.208],
                    [15.47, 0.18],
                    [16.19, 0.157],
                    [16.92, 0.137],
                    [17.67, 0.12],
                    [18.45, 0.106],
                    [19.23, 0.093],
                    [20.03, 0.083],
                    [20.84, 0.074],
                    [21.66, 0.066],
                    [22.49, 0.06],
                    [23.32, 0.054],
                    [24.16, 0.049],
                    [25, 0.044]])


class IEA15MW(WindTurbine):
    
    '''
    Data from:
    github.com/IEAWindTask37
    
    '''
    
    def __init__(self, method='linear'):
        """
        Parameters
        ----------
        method : {'linear', 'pchip'}
            linear(fast) or pchip(smooth and gradient friendly) interpolation
        """
        u, p = power_curve.T
        u1, ct = ct_curve.T
        WindTurbine.__init__(self, 
                             name='IEA15MW', 
                             diameter=250, 
                             hub_height=150,
                             powerCtFunction=PowerCtTabular(u, p*1e03, 'w', ct, ws_cutin=3, ws_cutout=25, ct_idle=0.044, method=method))
        

IEA15MW_RWT = IEA15MW

def main():
    wt = IEA15MW()
    print('Diameter', wt.diameter())
    print('Hub height', wt.hub_height())

    import matplotlib.pyplot as plt
    ws = np.linspace(2, 20, 100)
    plt.plot(ws, wt.power(ws) * 1e-3, label='Power')
    c = plt.plot([], [], label='Ct')[0].get_color()
    plt.ylabel('Power [kW]')
    ax = plt.gca().twinx()
    ax.plot(ws, wt.ct(ws), color=c)
    ax.set_ylabel('Ct')
    plt.xlabel('Wind speed [m/s]')
    plt.gcf().axes[0].legend(loc=1)
    plt.show()

if __name__ == '__main__':
    main()