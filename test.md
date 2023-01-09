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
- check/build a database of food including thermal/mechanical properties, shelf life at different temperatures, preferred storage temperature, HX surface/total surface ratio or similar
- check/build a cost model of food, which could be as simple as $/kg per each food
- check/find suitable/credible convective heat transfer coefficients used in the modelling
- check/build storage cost model
  









