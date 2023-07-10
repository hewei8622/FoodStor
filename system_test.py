from system_class import EnergySystem
import numpy as np
from EnergyStor import EnergyStorage
from Food_class import Food
from ColdHubs import ColdHubs

import matplotlib.pyplot as plt

## define EnergySystem "system1"
capacity = 1000 # cooling power [W]
efficiency = 2 #cop , 200% efficiency
am_temperature = 30 # ambient temperature [C]
lat =2 # latitude
lon =45 # longitude
start_date = '2019-01-01'
end_date = '2019-01-31'
# initialisation of system1
system1 = EnergySystem(capacity, efficiency, am_temperature, lat, lon, start_date, end_date)



#define EnergyStorage "battery"
batt_capa = 10 *3.6e6 #kWh --> Joule
batt_eff = .98 # efficiency
energy_form = "electricity"
energy_density = 300  #kWh/m3
energy_cost = 150 #$/kWh
storage_name = "battery"

battery = EnergyStorage(batt_capa, batt_eff, energy_form, storage_name, energy_density, energy_cost)


#defien Food "food1"
food_type = "fruit"
weight = 5 #kg
name = "apple"
heat_capacity = 3.7e3 #J/kgK
surface_area = .01/.15 #m2/kg [notes] check this data or find more data
initial_temperature = am_temperature # assum food temperature equals to the ambient temperature
target_temperature = 5 # could be per food
max_tem = 8
min_tem = 3
shelf_life = 30 #days
life_remaining = 30 #days

food1 = Food(food_type, weight, name, heat_capacity, surface_area, initial_temperature, target_temperature,
                 max_tem, min_tem, shelf_life, life_remaining)


## define solar parameters
solar_area=20 # solar panel area [m2]

## define ColdHubs "coldhubs"
volume = 60 #m3
u_value = 0.1 #W/m2K
temperature = am_temperature # intial T_hub
surface_area = 4*5*1.5 #m2
coldhubs=ColdHubs(volume, u_value, temperature, surface_area)

# assemble everything into the system1
# system1.time_variant_analysis(solar_area, battery, food1, coldhubs)
battery_soc, T_hub, T_food, solar_generation, cold_in, cold_out, day = system1.time_variant_analysis(solar_area, battery, food1, coldhubs)

# plot results
fig, (ax1, ax2, ax3) = plt.subplots(3,1)
# make a little extra space between the subplots
fig.subplots_adjust(hspace=0.5)

idx1 = 0
idx2 = -1

ax1.plot(day[idx1:idx2], battery_soc[idx1+1:idx2]/battery.capacity)
ax1.set_ylabel('Battery_SOC')
ax2.plot(day[idx1:idx2], T_hub[idx1:idx2], day[idx1:idx2], system1.coldhubs.T_hub_max*np.ones(len(day[idx1:idx2])),'--', day[idx1:idx2], system1.coldhubs.T_hub_min*np.ones(len(day[idx1:idx2])),'--')
ax2.set_ylabel('T_hub')
ax2.plot(day[idx1:idx2], T_food[idx1:idx2],day[idx1:idx2], system1.coldhubs.T_hub_max*np.ones(len(day[idx1:idx2])),'--', day[idx1:idx2], system1.coldhubs.T_hub_min*np.ones(len(day[idx1:idx2])),'--')
# ax3.set_ylabel('T_food')
ax3.plot(day[idx1:idx2], solar_generation[idx1:idx2], day[idx1:idx2], cold_in[idx1:idx2], day[idx1:idx2], cold_out[idx1:idx2])
ax3.set_ylabel('Power')
ax3.set_xlabel('hours in a year')

plt.show()

