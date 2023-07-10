from system_class import EnergySystem
import numpy as np
from EnergyStor import EnergyStorage
from Food_class import Food
from ColdHubs import ColdHubs
from ColdStor import ColdStorage
import matplotlib as mpl
import matplotlib.pyplot as plt
# mpl.use('macosx')

np.random.rand(1)


#this is the main function to run the system. Below are key parameters setting


# the period in wihch the system in simulated from "start date" to "end date"
start_date = '2019-01-01'
end_date = '2019-12-31'

# cooling power capacity in W
cooling_power = 800 # W
#battery capacity in kWh
batt_kwh = 2
# cold energy storage mass in kg; if ces_mass = 0, there is no cold energy storage
ces_mass = 0
# food mass in kg, currently we only consider one type of food
food_mass = 50
#solar PV panel area in m2
PV_area = 6
# coldhub space in m3
coldhub_volume = 2

# plot index
idx1 = int(np.random.rand(1)*8670*60*.5)
idx1 =1
idx2 = idx1 + 8670*59


## define EnergySystem "system1"
capacity = cooling_power # cooling power [W]
efficiency = 2 #cop , 200% efficiency
am_temperature = 30 # ambient temperature [C]
lat =2 # latitude
lon =45 # longitude


# initialisation of cooling or the food storage system1
system1 = EnergySystem(capacity, efficiency, am_temperature, lat, lon, start_date, end_date)


#define EnergyStorage "battery"
batt_capa = batt_kwh *3.6e6 #kWh --> Joule, energy capacity
batt_eff = .98 # energy efficiency
energy_form = "electricity" # the form of energy
energy_density = 300  #kWh/m3, energy density not used
energy_cost = 150/3.6e6 #$/kWh -> $kWh/J, energy cost
storage_name = "battery" # energy storage name

#initialise battery energy storage
battery = EnergyStorage(batt_capa, batt_eff, energy_form, storage_name, energy_density, energy_cost)

#define cold storage "ces"
# batt_capa = 0 #kWh --> Joule, energy storage not used here, as the capacity is determined by the mass below
# batt_eff = 0 # efficiency, not used here
energy_form = "cold"
# energy_density = 0  #kWh/m3
energy_cost = 5.0 # $/kg
storage_name = "ces"

T_melt = 5.0 # melting temperature of the PCM
h_fg = 250e3 #J/kg, latent heat of the PCM
heat_capacity = 720.0 # heat capacity of the PCM
mass = ces_mass #kg, the mass of teh cold storage used in the system

# initialise the cold storage in the simulation
ces = ColdStorage(batt_capa, batt_eff, energy_form, storage_name, energy_density, energy_cost, T_melt, h_fg, heat_capacity, mass)

# currently only a lumped single type food is considered
#defien Food "food1"
food_type = "fruit"
weight = food_mass #kg
name = "apple"
heat_capacity = 3.7e3 #J/kgK, heat capacity
surface_area = .01/.15 #m2/kg [notes] check this data or find more data
initial_temperature = 30 # initial food tempearature
target_temperature = 5 # target tempearture
max_tem = 8 # set the upper bound of the food storage temperature
min_tem = 3 # set the lower bound of the food storage temperature
shelf_life = 30 #days
life_remaining = 30 #days

#initialise the food class
food1 = Food(food_type, weight, name, heat_capacity, surface_area, initial_temperature, target_temperature,
                 max_tem, min_tem, shelf_life, life_remaining)

# system1.set_food_schedule(weight)


## define solar parameters
solar_area= PV_area # solar panel area [m2]

## define ColdHubs "coldhubs"
volume = coldhub_volume #m3, the physical volume
u_value = 0.1 #W/m2K, the overall heat transfer coefficieint
temperature = 0 #am_temperature # intial temperature of the coldhub
surface_area = coldhub_volume * .05 #m2, surface area of the coldhub
coldhub_cost = 100 #$/m3
# initialise the coldhub object
coldhubs=ColdHubs(volume, u_value, temperature, surface_area, coldhub_cost)

# assemble everything into the system1
# system1.time_variant_analysis(solar_area, battery, food1, coldhubs)


battery_soc, T_hub, T_food, solar_generation, cold_in, cold_out, day, sys_total_cost = system1.time_variant_analysis_ces(solar_area, battery, ces, food1, coldhubs)

print('the system total capital cost is ' + str(sys_total_cost) + ' $')

# plot results
fig, (ax1, ax2, ax3) = plt.subplots(3,1)
# make a little extra space between the subplots
fig.subplots_adjust(hspace=0.5)





print(idx1,idx2)

# battery state of the charge (SOC)
ax1.plot(day[idx1:idx2], battery_soc[idx1:idx2]/battery.capacity, label = 'batt')
ax1.set_ylabel('SOC [%]')
ax1.legend()

# the temperature profile of the codlhub
ax2.plot(day[idx1:idx2], T_hub[idx1:idx2], label = 'coldhub')
ax2.plot(day[idx1:idx2], system1.coldhubs.T_hub_max*np.ones(len(day[idx1:idx2])),'b--', day[idx1:idx2], system1.coldhubs.T_hub_min*np.ones(len(day[idx1:idx2])),'b--')
ax2.set_ylabel('Temp [C]')
ax2.plot(day[idx1:idx2], T_food[idx1:idx2],label = 'food' ) # day[idx1:idx2], system1.coldhubs.T_hub_max*np.ones(len(day[idx1:idx2])),'--', day[idx1:idx2], system1.coldhubs.T_hub_min*np.ones(len(day[idx1:idx2])),'--')
# ax3.set_ylabel('T_food')
ax2.legend()

# the power profiles of solar power, heat brough by the food, and cooling power
ax3.plot(day[idx1:idx2], solar_generation[idx1:idx2]/3600/system1.res, label = 'solar')
ax3.plot(day[idx1:idx2], cold_in[idx1:idx2]/3600/system1.res, label = 'cooling power')
ax3.plot(day[idx1:idx2], cold_out[idx1:idx2]/3600/system1.res, label = 'food heat')
# ax3.plot(day[idx1:idx2], cold_in[idx1:idx2], day[idx1:idx2], cold_out[idx1:idx2])
ax3.legend()

ax3.set_ylabel('Power [W]')
ax3.set_xlabel('hours in a year')

plt.show()

