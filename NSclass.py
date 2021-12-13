# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 19:02:16 2021

@author: cosmo
"""

import numpy as np
import scipy as sp
from scipy import integrate
from project.utils import ODEsolver, cgs_geom_dictionary


class NeutronStar:
    
    def __init__(self, NS_type, eq_state):
        
        self.kind = NS_type
        self.eos = eq_state
        
    
    def TOV_eqs(self, r, y, index="False"):

        m,p=y
        if p<0:
            return [0,0]
        eden = self.eos.EdenFromPressure(p, index)
#        print(eden)
        dm = 4*np.pi*eden*r**2
        dp = - (eden+p)*(m + 4*np.pi*r**3*p)/(r*(r-2*m))
        dy = [dm, dp]
        
        return dy

    def Newton_eqs(self, r, y):

        m,p=y
        
        eden = self.eos.DensityFromPressure(p)
        dm = 4*np.pi*eden*r**2
        dp = - (eden*m)/(r**2)
        dy = [dm, dp]

        return dy
    
    def star_solver(self, eq_type, central_value, value_type="pressure", unit_type="geom"):

        
        
        #if unit_type == "cgs":
        central_value = central_value*cgs_geom_dictionary[unit_type][value_type]["geom"]
        #elif unit_type == "si":
            #central_value = central_value*cgs_geom_dictionary["si"][value_type]["geom"]    


        if value_type == "density":
            central_value = self.eos.PressureFromDensity(central_value)

        solutions = ODEsolver(eq_type, central_value)
        r_out = np.array([])
        m_out = np.array([])
        p_out = np.array([])

        for i in range(solutions[0].size):
            r_out = np.append(r_out, solutions[0][i]*cgs_geom_dictionary["geom"]["lenght"]["km"])
            m_out = np.append(m_out, solutions[1][i]*cgs_geom_dictionary["geom"]["mass"]["m_sol"])
            p_out = np.append(p_out, solutions[2][i]*cgs_geom_dictionary["geom"]["pressure"]["cgs"])

        return r_out, m_out, p_out
        
    
    def mass_vs_radius(self, centrals, eq_type, value_type, unit_type):
        
        radii = np.array([])
        masses = np.array([])
        
        import tqdm               
        for i in tqdm.tqdm(range(centrals.size)):
            solutions = self.star_solver(eq_type, centrals[i], value_type, unit_type)
            radii = np.append(radii, solutions[0][-1])
            masses = np.append(masses, solutions[1][-1])

        
        return radii, masses
        
            
            