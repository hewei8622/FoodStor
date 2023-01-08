from system_class import EnergySystem
import numpy as np
from EnergyStor import EnergyStorage
from Food_class import Food


capacity = 5
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

#The number of hours for analysis, which also is the length of variables
# len_analysis = system1.get_analysis_duration()
# print("the hours considered is " + str(len_analysis))

## get solar data from renewable.ninja
# solar_data = system1.get_solar()
# air_temperature_series = solar_data.t2m
# radiance = solar_data.swgdn

# solar_data = system1.get_solar_from_file('solar_data_2019.csv')
# print(solar_data)
# print(solar_data.columns)
# print(solar_data['GHI'])
# print(solar_data['Temperature'])

# #define energy storage 1
# batt_capa = 5*3.6e6 #kWh
# batt_eff = .98 # efficiency
# energy_form = "electricity"
# energy_density = 300 #kWh/m3
# energy_cost = 150 #$/kWh
# storage_name = "battery"
#
# battery = EnergyStorage(batt_capa, batt_eff, energy_form, storage_name, energy_density, energy_cost)
#
#
# #define energy storage 2
# batt_capa = 15*3.6e6 #kWh
# batt_eff = .8 # efficiency
# energy_form = "heat"
# energy_density = 80 #kWh/m3
# energy_cost = 50 #$/kWh
# storage_name = "TES"
#
# TES = EnergyStorage(batt_capa, batt_eff, energy_form, storage_name, energy_density, energy_cost)
#
# energystorage = []
# energystorage.append(battery)
# energystorage.append(TES)
#
# system1.set_energystorage(energystorage)


#defien the food type
food_type = "fruit"
weight = 4 #kg
name = "apple"
heat_capacity =  3.7e3 #J/kgK
surface_area = .008/.15 #m2/kg
initial_temperature = am_temperature
target_temperature = 5 #fridge
shelf_life = 30 #days
life_remaining = 30 #days

food1 = Food(food_type, weight, name, heat_capacity, surface_area, initial_temperature, target_temperature,
                 shelf_life, life_remaining)

# food_type = "fruit"
# weight = 40 #kg
# name = "pear"
# heat_capacity =  2.7e3 #J/kgK
# surface_area = .01/.15 #m2/kg
# initial_temperature = am_temperature
# target_temperature = 5 #fridge
# shelf_life = 10 #days
# life_remaining = 10 #days
#
# food2 = Food(food_type, weight, name, heat_capacity, surface_area, initial_temperature, target_temperature,
#                  shelf_life, life_remaining)
#
# food =[]
# food.append(food1)
# food.append(food2)
#
# system1.set_food(food)

food1.food_temperature_update(5, 1)

