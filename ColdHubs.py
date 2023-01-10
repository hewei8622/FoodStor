
import numpy as np


class ColdHubs:
    def __init__(self, volume, u_value, temperature, surface_area):
        self.volume = volume # physical volume [m3]
        self.u_value = u_value # overall heat transfer coeff [W/m2K]
        ## air's properties are assumed to be constant, not depending on the temperature
        ## [notes] this could be revised using coolprop but may not be necessary
        self.air_heat_capacity = 700 #J/kg K heat capacity
        self.temperature = temperature # coldhub's air temperature [C]
        self.air_density = 1.293 #kg m−3 air density
        self.area = surface_area # the coldhub's surface area
        self.h_conv = 1 #W/m2K convective heat transfer coeff
        ## bounds for T_hub should be determined by the Food's requirement
        self.T_hub_max = 8 # upper bound for T_hub
        self.T_hub_min = 3 # lowwer bound for T_hub

    def get_air_temperature(self, cold_in, cold_out, am_tempearture, res):
        # cold_out -- cold energy absorbed by food stored in teh hub [J]
        # cold_in -- cold energy input to the hub [J]
        # am_temperature -- ambient temperature of the env where the coldhub is placed [C]
        heat_loss = self.u_value * self.area * (am_tempearture - self.temperature) * 3600 * res
        dT = (cold_in - cold_out - heat_loss)/(self.air_density * self.volume * self.air_heat_capacity)


        self.temperature = self.temperature - dT





