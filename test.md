# SolarFoodStor note

This is the note for introducing SolarFoodStore project, which is also used as a doc for recording the development. 

In the current codes, we have several classes

- EnergyStorage: a class to characterise energy storage technologies used in the system. In our research we will have both electrical energy and thermal energy storage considered  
- Food: a class to characterise food to be stored in the system. 
- EnergySystem: a class to assemble all components, including solar pannels, energy storage, food and other parts together and develop simulations and analysis. 


## Modules needed to develop

- The current model is a simplified version. It calculates only the energy flow hour by hour without modelling the temperature variation. It is a simple generate-load balance analysis, so we could figure out imbalance and an index could be used to label that. This analysis could only esimate system-level parameters like the battery capacity, solar capacity, etc.The calculation between the system-level and (food and storage etc) is decoupled.  
- Time-variant temperature variation/profile of food by modelling heat transfers with in food
- This will change the operation mode to **power-driven** analysis in which the power profile could be manipulated (like via a controller) and the temperature profile of the food will depend on the cooling power and cold room temperature. 

## 6 Jan 2023
- The time-variant temperature tracking is implemented, but need to check the results
- Now we can do both simple energy balance and temperature variation analysis 
- The conversion between electricity and cold/thermal doesn't seem right, need to correct


## 9 Jan 2023

### the logic of system.time_variant_analysis()

- T_food and T_hub are tracked at every timestep during the analysis duration, e.g., every hour in a year.
- The purpose is to make sure the T_hub is bounded within a predefined temperature range, which is good for storing the food defiend in Food. 
- To meet the T_hub requirement, cold power is provided from combined solar and battery, depending on the solar generation, battery_soc, and T_hub. 
- The logic to operate battery may be illustrated for clarifying how it works. 

### updates
- battery charging eff is updated (battery efficiency is considered only in the charging, so the discharhing is assumed to be 100%.)
- system./cop is updated (electrical power and thermal power conversion is considered)


### what need to do
- [long] check/build a database of food including thermal/mechanical properties, shelf life at different temperatures, preferred storage temperature, HX surface/total surface ratio or similar
- [long] check/build a cost model of food, which could be as simple as $/kg per each food
- [long] check/find suitable/credible convective heat transfer coefficients used in the modelling
- [long] check/build storage cost model
- [short] need to refine the control timestep from a hour to probably 5 min (there are overshoting and not-converging issues)
- [long] check conv coeffs 
  

## 10 Jan 2023 

### updates
- add a food schedule (daily hot food in and cold food out)
- fix the cop conversion. Now electrical power is considered in the energy flow analysis, cop is considered when the T_hub is updating

### notes 
- the timestep could not be too big, as the current assumption is a semi-steadystate analysis, so in each timestep, the analysis (like the temperature update) is assumed to be steadystate. By updating in each timestep, a time-series of everything could be obtained.

### what can do
- add a value chain analysis: the investment for the cold chain vs. the value of the food
- the shelf life of the food with the storage temperature and time against its time-variant cost
- an operational research of where to store, what to transport (cold chain or not), and where to charge the cold transport 


# 11 Jan 2023

## notes
### to date 

### further development
- [short-term] could add further functions 
  - cold energy storage as an additional storage
  - more complex food inventory and schedules 
  - cost models 

- [longer term] other info about the value chain of food
  - how coldhub can improve the value of food (we want to model it. such as analysing the temperature effect on the shelf life and then the value it could represent for farmers)
  - then, what we may further develop beyond the scope of the project is to model and optimise the planning of solar charging station (if needed) and coldhubs for maximising the value of food/agriculture. 
    







