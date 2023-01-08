from system_class import EnergySystem
import numpy as np
from EnergyStor import EnergyStorage
from Food_class import Food
from ColdHubs import ColdHubs


capacity = 50 # cooling power
efficiency = 2
cooling_demand = 5
temperature = 5
am_temperature = 30
storage_capacity =10
lat =2
lon =45
start_date = '2019-01-01'
end_date = '2020-01-01'
system1 = EnergySystem(capacity, efficiency, cooling_demand, temperature, am_temperature, storage_capacity, lat, lon, start_date, end_date)



## get solar data from renewable.ninja
# solar_data = system1.get_solar()
# air_temperature_series = solar_data.t2m
# radiance = solar_data.swgdn

#define energy storage
batt_capa = 5 *3.6e6 #kWh
batt_eff = .98 # efficiency
energy_form = "electricity"
energy_density = 300 #kWh/m3
energy_cost = 150 #$/kWh
storage_name = "battery"

battery = EnergyStorage(batt_capa, batt_eff, energy_form, storage_name, energy_density, energy_cost)


#defien the food type
food_type = "fruit"
weight = 400 #kg
name = "apple"
heat_capacity =  3.7e3 #J/kgK
surface_area = .008/.15 #m2/kg
initial_temperature = am_temperature
target_temperature = 5 #fridge
shelf_life = 30 #days
life_remaining = 30 #days

food1 = Food(food_type, weight, name, heat_capacity, surface_area, initial_temperature, target_temperature,
                 shelf_life, life_remaining)


solar_area=1 #m2
#test energy balance function
# system1.energybalance(solar_area, battery, food1)

volume = 100#m3
u_value = 0.5 #W/m2K
temperature = 5

surface_area = 3*3*6 #m2

coldhubs=ColdHubs(volume, u_value, temperature, surface_area)

system1.time_variant_analysis(solar_area, battery, food1, coldhubs)

