from system_class import EnergySystem
import numpy as np
from EnergyStor import EnergyStorage
from Food_class import Food
from ColdHubs import ColdHubs

## define EnergySystem "system1"
capacity = 15000 # cooling power [W]
efficiency = 2 #cop , 200% efficiency
am_temperature = 30 # ambient temperature [C]
lat =2 # latitude
lon =45 # longitude
start_date = '2019-01-01'
end_date = '2020-01-01'
# initialisation of system1
system1 = EnergySystem(capacity, efficiency, am_temperature, lat, lon, start_date, end_date)



#define EnergyStorage "battery"
batt_capa = 50 *3.6e6 #kWh --> Joule
batt_eff = .98 # efficiency
energy_form = "electricity"
energy_density = 300  #kWh/m3
energy_cost = 150 #$/kWh
storage_name = "battery"

battery = EnergyStorage(batt_capa, batt_eff, energy_form, storage_name, energy_density, energy_cost)


#defien Food "food1"
food_type = "fruit"
weight = 1 #kg
name = "apple"
heat_capacity = 3.7e3 #J/kgK
surface_area = .008/.15 #m2/kg [notes] check this data or find more data
initial_temperature = am_temperature # assum food temperature equals to the ambient temperature
target_temperature = 5 # could be per food
max_tem = 8
min_tem = 3
shelf_life = 30 #days
life_remaining = 30 #days

food1 = Food(food_type, weight, name, heat_capacity, surface_area, initial_temperature, target_temperature,
                 max_tem, min_tem, shelf_life, life_remaining)


## define solar parameters
solar_area=200 # solar panel area [m2]

## define ColdHubs "coldhubs"
volume = 60 #m3
u_value = 0.5 #W/m2K
temperature = 5 # intial T_hub
surface_area = 4*5*6 #m2
coldhubs=ColdHubs(volume, u_value, temperature, surface_area)

# assemble everything into the system1
system1.time_variant_analysis(solar_area, battery, food1, coldhubs)

