from Simulator1D import RocketSim1D

Cd = 0.75 #Ceofficient of drag
D = 0.3048 # Diameter (m)
M_s = 274 #Dry mass (kg)
specific_impulse = 250 #seconds
total_impulse = 889600 #Newton-seconds
RocketSim1D(Cd, D, M_s, specific_impulse, burn_time, total_impulse).solve()
burn_time = 50 # seconds



