import math

def atmosphere(altitude):
    # input altitude in meters

    gamma = 1.4
    Ru = 8314.5 # J/kmol/ºC
    Mair = 29 # kg/kmol

    R = Ru / Mair

    # pressure (kPa), temp(ºC), T(K), a(m/s), rho(kg/m^3)    
    if (altitude <= 11000):
        temp = 15.04 - 0.00649 * (altitude)
        pressure = 101.29 * ((temp + 273.1) / 288.08) ** 5.256    
    elif (altitude > 11000) and (altitude <= 25000):
        temp = -56.46
        pressure = 22.65 * (math.e ** (1.73 - 0.000157 * altitude))
    elif(altitude > 25000):
        temp = -131.21 + 0.00299 * altitude
        pressure = 2.488 * ((temp + 273.1) / 216.6) ** (-11.388)

    T = temp + 273.15
    a = (gamma * R * T) ** 0.5
    rho = pressure / (0.2869 * T)

    return [pressure, T, rho, a]