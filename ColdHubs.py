
import numpy as np


class ColdHubs:
    def __init__(self, volume, u_value, temperature, surface_area, cost):
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
        self.unit_cost = cost
        print("A ColdHub is initiated")

    def get_cost(self):

        return self.unit_cost * self.volume

    def get_air_temperature(self, cold_in, cold_out, am_tempearture, res):
        # cold_out -- cold energy absorbed by food stored in teh hub [J]
        # cold_in -- cold energy input to the hub [J]
        # am_temperature -- ambient temperature of the env where the coldhub is placed [C]
        heat_loss = self.u_value * self.area * (am_tempearture - self.temperature) * 3600 * res
        dT = (cold_in - cold_out - heat_loss)/(self.air_density * self.volume * self.air_heat_capacity)

        print('at this time step')
        print(['the input cold power is '+str(cold_in)+' W'])
        print('the energy loss to the ambient is' + str(heat_loss) +' W')
        print('the cold abosired by the food is' +str(cold_out) + 'W')

        self.temperature = self.temperature - dT


    def get_air_temperature_ces(self, cold_in, cold_out, cold_store, am_tempearture, res, food):
        # cold_out -- cold energy absorbed by food stored in teh hub [J]
        # cold_in -- cold energy input to the hub [J]
        # cold_store -- cold energy storage -- need to add
        # am_temperature -- ambient temperature of the env where the coldhub is placed [C]
        heat_loss = self.u_value * self.area * (am_tempearture - self.temperature) * 3600 * res

        h_fg = cold_store.latent_heat

        delta_T_pcm = 0.5
        # for simplicity, assuming T_pcm is the same to the T_air for now
        if self.temperature < cold_store.melting_temperature - delta_T_pcm:
            artificial_initial_cold = cold_store.heat_capacity * cold_store.mass

        else:
            if self.temperature < cold_store.melting_temperature + delta_T_pcm:
                artificial_initial_cold = cold_store.heat_capacity * (1 + cold_store.latent_heat) * cold_store.mass
            else:
                artificial_initial_cold = cold_store.heat_capacity * cold_store.mass

        brick_density  = 2000 # kg/m3
        brick_heat_capacity = 1000 #J/kgK
        wall_thickness = 0.1 # m


        coldhub_initial = brick_density * brick_heat_capacity * wall_thickness * self.area
        dT = (cold_in - cold_out - heat_loss) / (self.air_density * self.volume * self.air_heat_capacity + artificial_initial_cold + coldhub_initial + food.weight*food.heat_capacity)

        print('at this time step')
        print(['the input cold power is ' + str(cold_in) + ' W'])
        print('the energy loss to the ambient is' + str(heat_loss) + ' W')
        print('the cold abosired by the food is' + str(cold_out) + 'W')

        self.temperature = self.temperature - dT





