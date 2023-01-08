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
- 

  









