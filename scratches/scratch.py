import numpy as np
from scipy.integrate import solve_ivp
from density import density_exp_model
import matplotlib.pyplot as plt


# %matplotlib inline

def hit_apogee(t, y):
    return y[0]


hit_apogee.terminal = True
hit_apogee.direction = -1


class RocketSim1D(object):

    def __init__(self, Cd, D, M_s, specific_impulse, burn_time, total_impulse):
        self.Cd = Cd
        self.D = D
        self.specific_impulse = specific_impulse
        self.burn_time = burn_time
        self.total_impulse = total_impulse
        self.g = 9.81  # Gravity (m/s^2)
        self.M_s = M_s
        self.M_p = total_impulse / (specific_impulse * self.g)
        self.M_tot = M_s + self.M_p
        self.thrust = total_impulse / burn_time
        self.A = np.pi * D ** 2 / 4  # Area (m^2)
        self.Re = 6378 * 10 ** 3  # Radius of earth (m)
        self.mdot = self.thrust / (specific_impulse * self.g)
        print('The mass of the propellant: ' + str(np.round(self.M_p, 1)) + ' kg')

    def System(self, t, y):
        # y is the state vector [velocity, altitude]
        # t is time
        rho = density_exp_model(y[1], self.Re)

        if t <= self.burn_time:
            # print(t)
            self.M_cur = self.M_tot - self.mdot * t
            dVdt = self.thrust / self.M_cur - 0.5 * rho * y[0] ** 2 * self.A * self.Cd / self.M_cur - self.g
        elif y[0] > 0:
            dVdt = -0.5 * rho * y[0] ** 2 * self.A * self.Cd / self.M_cur - self.g
        elif y[0] < 0:  # Reach apogee
            dVdt = 0.5 * rho * y[0] ** 2 * self.A * self.Cd / self.M_cur - self.g

        dhdt = y[0]
        dydt = [dVdt, dhdt]
        return dydt

    def solve(self):
        t_span = [0, 600]
        times = np.linspace(0, 600, 6000)
        yo = [0.0, 0.0]
        sol = solve_ivp(self.System, t_span, yo, t_eval=times, method='LSODA', max_step=1, events=hit_apogee)

        plt.figure(figsize=(16, 4), dpi=80)
        plt.subplot(1, 3, 1)
        plt.plot(sol.t, sol.y[1])
        plt.xlabel('Time (s)')
        plt.ylabel('Altitude (m)')

        plt.subplot(1, 3, 2)
        plt.plot(sol.t, sol.y[0])
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity (m/s)')

        accel = (sol.y[0, 1:] - sol.y[0, :-1]) / (sol.t[1:] - sol.t[:-1])
        plt.subplot(1, 3, 3)
        plt.plot(sol.t[:-1], accel)
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration (m/s^2)')
        plt.savefig('Results' + '.pdf', format='pdf', dpi=1200, bbox_inches='tight')
        print('Apogee: ' + str(np.round(np.max(sol.y[1]), -3)) + ' km')
        print('Max Velocity: ' + str(np.round(np.max(sol.y[0]), -2)) + ' m/s')
        print('Max Acceleration: ' + str(np.round(np.max(accel), 0)) + ' m/s^2')
