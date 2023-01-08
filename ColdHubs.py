
import numpy as np


class ColdHubs:
    def __init__(self, volume, u_value, temperature, surface_area):
        self.volume = volume
        self.u_value = u_value
        self.air_heat_capacity = 700 #J/kg K
        self.temperature = temperature
        self.air_density = 1.293 #kg m−3
        self.area = surface_area
        self.h_conv = 1 #W/m2K
        self.T_hub_max = 8
        self.T_hub_min = 3


    def get_air_temperature(self, cold_in, cold_out, am_tempearture):
        #heat loss to env
        heat_loss = self.h_conv * self.area * (am_tempearture - self.temperature)
        dT = (cold_in - cold_out - heat_loss)/(self.air_density * self.volume * self.air_heat_capacity)
        #cold_in is cooling from freezer or cold energy storage
        #cold_out is the cooling to food

        self.temperature = self.temperature - dT



