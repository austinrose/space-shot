import math
import numpy as np
from scipy import linalg


# convert IJK vectors to orbital elements (r and v in km and km/s)
def ijk2oe(r_IJK, v_IJK):
    mu = 3.986 * 10**5
    r_mag = linalg.norm(r_IJK)
    v_mag = linalg.norm(v_IJK)
    h = np.cross(r_IJK.T, v_IJK.T)
    h_mag = linalg.norm(h)
    n = np.cross(np.mat([0,0,1]), h).T
    n_mag = linalg.norm(n)
    e = (1 / mu) * (((v_mag)**2 - mu/r_mag)*r_IJK - (np.inner(r_IJK.T,v_IJK.T).item(0) * v_IJK))
    e_mag = linalg.norm(e)
    p = h_mag**2 / mu
    a = p / (1 - e_mag**2)
    little_omega = math.acos(np.inner(n.T,e.T).item(0)/(n_mag * e_mag)) * 180 / math.pi
    big_omega = math.acos(n[0,0]/n_mag) * 180 / math.pi
    i = math.acos(h[0,2]/h_mag) * 180 / math.pi   
    nu = math.acos(np.inner(e.T, r_IJK.T).item(0)/(r_mag * e_mag)) * 180 / math.pi

    return [e_mag, p, a, little_omega, big_omega, i, nu]

# convert orbital elements to IJK earth centric coordinates
def oe2ijk(p, e_mag, i, o, w, nu):

    #convert i,o,w into radians
    i = i * math.pi / 180
    w = w * math.pi / 180
    o = o * math.pi / 180
    nu = nu * math.pi / 180

    # convert orbital elements into perifoal eccentricity coordinate system
    r_scalar = p / (1 + e_mag * math.cos(nu))
    rw_vec = np.mat([r_scalar * math.cos(nu), r_scalar * math.sin(nu), 0])
    vw_vec = ((1/p)**0.5) * np.mat([-math.sin(nu), (e_mag + math.cos(nu)), 0])

    # define transformation matrix
    r11 = (math.cos(o) * math.cos(w)) - (math.sin(o) * math.sin(w) *math.cos(i))
    r12 = (-math.cos(o) * math.sin(w)) - (math.sin(o) * math.cos(w) *math.cos(i))
    r13 = math.sin(o) * math.sin(i)

    r21 = (math.sin(o) * math.cos(w)) + (math.cos(o) * math.sin(w) * math.cos(i))
    r22 = (-math.sin(o) * math.sin(w)) + (math.cos(o) * math.cos(w) * math.cos(i))
    r23 = -math.cos(o) * math.sin(i)

    r31 = math.sin(w) * math.sin(i)
    r32 = math.cos(w) * math.sin(i)
    r33 = math.cos(i)

    R = np.mat([[r11, r12, r13], [r21, r22, r23], [r31, r32, r33]])

    # compute transformed radius and velocity
    r_out = R * rw_vec.T
    v_out = R * vw_vec.T    

    return [r_out, v_out]

# convert topocentric coordinates to IJK 
# inputs:  rho: np matrix 1x3, theta: float (deg), l: float (deg)
def sez2ijk(rho, theta, l):
    # convert rho and theta to radians
    rho = rho * math.pi / 180
    l = l * math.pi / 180

    # define transformation matrix
    r11 = math.sin(l) * math.cos(theta)
    r12 = -math.sin(theta)
    r13 =  math.cos(l) * math.cos(theta)

    r21 = math.sin(l) * math.sin(theta)
    r22 = math.cos(theta)
    r23 = math.cos(l) * math.sin(theta)

    r31 = - math.cos(l)
    r32 = 0
    r33 = math.sin(l)

    D = np.mat([[r11, r12, r13], [r21, r22, r23], [r31, r32, r33]])

    r = D * rho.T

    return r

def v_sez2v_ijk(r_IJK, v_SEZ):
    omega_earth = np.mat([0, 0, 0.05883])
    v_IJK = v_SEZ + np.cross(omega_earth, r_IJK.T).T
    return v_IJK.T
