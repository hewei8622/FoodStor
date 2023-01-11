import requests
import json
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
from scipy import interpolate
class EnergySystem:
    def __init__(self, capacity, efficiency, am_temperature, lat, lon, start_date, end_date):
        self.cooling_power = capacity  # electrical capacity of the system (W)
        self.cop = efficiency  # Efficiency of the system, namely COP
        # self.temperature = temperature  # The system temperature [K]
        self.am_temperature = am_temperature # the envioronmental temperature, ambient temperature [K]
        self.cooling_demand = [] # system's cooling demand for reducing/maintaining food's storage temperature [J]
        self.lat = lat # latitude
        self.lon = lon # longitude
        self.start_date = start_date # date
        self.end_date = end_date # date
        self.coldhubs = [] # coldhub class
        self.energystorage = [] # energystorage class
        self.food = [] # food class
        self.time4plot= []
        self.food_schedule = []
        self.res = 1 / 60


    def get_temperature(self):

        return self.temperature

    def set_food_schedule(self):
        len_day = len(np.arange(0, 24, self.res))
        day_schedule = np.zeros(len_day)

        for i in np.arange(1, len_day, 1):
            if i * self.res == 16:
                day_schedule[i] = -200

            if i * self.res == 10:
                day_schedule[i] = 200

        for i in np.arange(0,365,1):
            self.food_schedule = np.concatenate((self.food_schedule, day_schedule), axis=None)

    def get_hours_btw_dates(self):
        date1 = datetime.strptime(self.start_date+" 00:00:00", "%Y-%m-%d %H:%M:%S")
        date2 = datetime.strptime(self.end_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")

        # Calculate the difference between the two dates
        difference = date2 - date1

        # Get the number of hours by dividing the difference in seconds by the number of seconds in an hour
        hours = difference.total_seconds() / 3600
        return int(hours)

    def get_energy_loss(self, output_energy):
        """
        Calculates the energy loss of the system.

        Parameters:
        output_energy (float): Output energy from the system (MWh)

        Returns:
        float: Energy loss of the system (MWh)
        """
        return output_energy * self.energy_loss



    def get_storage_capacity(self, output_energy):
        """
        Calculates the remaining storage capacity of the system.

        Parameters:
        output_energy (float): Output energy from the system (MWh)

        Returns:
        float: Remaining storage capacity of the system (MWh)
        """
        return self.storage_capacity

    def get_solar_from_renewable_ninja(self):

        token = '5fcfba5a33a4d78ff07a1267ecab58e36fd29695'
        api_base = 'https://www.renewables.ninja/api/'

        s = requests.session()
        # Send token header with each request
        s.headers = {'Authorization': 'Token ' + token}

        ##
        # PV example
        ##

        url = api_base + 'data/weather'

        args = {
            'lat': self.lat,
            'lon': self.lon,
            'date_from': self.start_date,
            'date_to': self.end_date,
            'dataset': 'merra2',
            'var_t2m': True,  # Air temperature (°C)
            'var_prectotland': False,  # Precipitation (mm / hour)
            'var_precsnoland': False,  # Snowfall (mm / hour)
            'var_snomas': False,  # Snow mass (kg / m²)
            'var_rhoa': False,  # Air density (kg / m³)
            'var_swgdn': True,  # Ground-level solar irradiance (W / m²)
            'var_swtdn': False,  # "Top of atmosphere solar irradiance (W / m²)",
            'var_cldtot': False,  # "name": "Cloud cover fraction", ...
            # "help": "Fraction of cloud cover, averaged over grid cell and ...
            # summed over all height above ground. CLDTOT variable in MERRA-2, ...
            # in native units (a [0, 1] scale)."
            'format': 'json'
        }
        print("-----------")
        print("Start to get weather data from renewable.ninja for the location")
        r = s.get(url, params=args)

        # Parse JSON to get a pandas.DataFrame of data and dict of metadata
        parsed_response = json.loads(r.text)

        data = pd.read_json(json.dumps(parsed_response['data']), orient='index')
        print("Weather data collection is completed")
        print("-----------")
        return data

    def get_solar_from_file(self, file):
        df =  pd.read_csv(file)

        return df


    def energybalance(self, solar_area, energy_storage1, food1):

        print("loading energy storage's data")
        print(energy_storage1.name + " is used for storing " + energy_storage1.energy_form)

        # Assume the battery has a capacity of 10 kWh and a round-trip efficiency of 0.9
        battery_capacity = energy_storage1.capacity  # J
        battery_efficiency = energy_storage1.energy_efficiency

        # # Assume the flywheel has a capacity of 5 kWh and a round-trip efficiency of 0.95
        # flywheel_capacity = energy_storage2.capacity  # kWh
        # flywheel_efficiency = energy_storage2.energy_efficiency

        print("loading solar power's data")
        # Generate random solar generation data for a year (8760 hours)
        solar_data = self.get_solar_from_file('solar_data_2019.csv')
        solar_irr = solar_data['GHI']
        solar_generation = solar_area * solar_irr * 0.15 * 3600 * self.res # solar efficiency is 15%

        len_data = len(solar_irr)
        # Initialize the battery and flywheel state of charge (SOC)
        battery_soc = np.zeros(1+len_data)  # kWh
        battery_soc[0] = battery_capacity
        # tes_soc = 0.0  # kWh



        h_conv = 1 #heat transfer coeffcient
        print("The food is " + food1.name)
        print("loading food's heat demand")
        load1 = food1.get_cooling_demand(self.temperature, h_conv)

        self.cooling_demand = load1

        performance = np.zeros(len_data)
        # Loop through the solar generation data and simulate the battery charging and discharging
        for i in range(len_data):
            # Calculate the excess solar generation that is not used by the load
            # excess_solar = max(solar_generation[i] - load1[i], 0)

            excess_solar = solar_generation[i] - self.cooling_demand

            if excess_solar > 0: # solar_generation is more than load

                battery_soc[i+1] = battery_soc[i] + min(excess_solar, battery_capacity - battery_soc[i]) / battery_efficiency
                performance[i] = 1
            else: # solar_generation is less than load
                battery_soc[i+1] = battery_soc[i] - min(self.cooling_demand - solar_generation[i], battery_soc[i])

                if battery_soc[i] > self.cooling_demand - solar_generation[i]:
                    performance[i] = 1


        fig, (ax1, ax2, ax3) = plt.subplots(3,1)
        # make a little extra space between the subplots
        fig.subplots_adjust(hspace=0.5)

        day = np.arange(0, len_data, 1)
        ax1.plot(day, battery_soc[1:])
        ax2.plot(day, performance)
        ax3.plot(day, solar_generation)

        plt.show()

    def set_energystorage(self, energystorage):

        self.energystorage = energystorage


    def set_food(self, food):

        self.food = food

    def get_total_cooling_deamnd(self):
        print("loading food's data")
        cooling_demand = np.zeros(len(self.food))

        for i in range(len(self.food)):
            print("The " + str(i) + "th food is " + self.food[i].name)
            print("Its current temperature is " + str(self.food[i].temperature))

            cooling_demand[i] = self.food[i].get_cooling_demand(self.temperature, 1)

        return cooling_demand

    def set_coldhubs(self, coldhubs):
        self.coldhubs = coldhubs

    def set_solar(self, solar_area):
        print("loading solar power's data")
        # read solar irradiance data for a year (8760 hours) in Nigeria
        solar_data = self.get_solar_from_file('solar_data_2019.csv')
        solar_irr = solar_data['GHI']
        solar_generation = solar_area * solar_irr * 0.15 * 3600 * self.res  # solar efficiency is 15% and change power (X time in seconds) to energy
        return solar_generation

    def time_variant_analysis(self, solar_area, energystorage, food, coldhubs):

        solar_generation = self.set_solar(solar_area)
        # length of analysis duration (i.e., 8760 [hours])
        len_data = len(solar_generation)

        day = np.arange(0, len_data, 1)
        self.time4plot = np.arange(0, len_data, self.res)


        f = interpolate.interp1d(day, solar_generation, fill_value="extrapolate")
        solar_generation = f(self.time4plot)
        len_data = len(solar_generation)


        self.set_energystorage(energystorage)
        self.set_food(food)
        self.set_coldhubs(coldhubs)

        #Battery capacity
        battery_capacity = self.energystorage.capacity  # J

        #this is currently not used. It could be accounted in one way, charging or discharging
        battery_efficiency = self.energystorage.energy_efficiency




        # Initialize the battery state of charge (SOC)
        battery_soc = np.zeros(1+len_data)  # kWh
        # battery_soc[0] = 0 #battery starts at zeor kWh
        battery_soc[0] = battery_capacity #battery starts at the full capacity
        #this needs to be refined later particulary when cost analysis is added
        #a min SOC (like 50%) needs to be considered here

        ## initialisation of time-variant variables
        # the time-variant food
        self.set_food_schedule()# [notes] food schedule testing

        # food_status = np.zeros(len_data)
        # food_status[0] = self.food_schedule[0]
        # init food temperature
        T_food = np.zeros(len_data)
        # food_weight = np.zeros(len_data)
        food_weight_in_hub = self.food.weight

        # the air temperature in the coldhub
        T_hub = np.zeros(len_data) #T_hub should be bounded within a pre-defiend range in the coldhubs class
        # time-variant cold power provided to the coldhub
        cold_power = np.zeros(len_data)



        # Loop through the solar generation data and simulate the battery charging and discharging, as well as T_food and T_hub
        for i in range(len_data):

            # the convective heat transfer coeff
            h_conv_food = 10 # in W/m2K
            # heat exchanged between the food to the env

            food_weight_in_hub = food_weight_in_hub + self.food_schedule[i]

            if food_weight_in_hub == 0:
                cold_out = 0
            else:
                cold_out = self.food.food_temperature_update(self.coldhubs.temperature, h_conv_food, self.food_schedule[i], self.am_temperature, food_weight_in_hub, self.res)  # Joule

            # update T_food
            T_food[i] = self.food.temperature

            if solar_generation[i] > 0: # if solar PV is generating power
                if self.coldhubs.temperature > self.coldhubs.T_hub_max: # if the coldhub is too hot

                    # enough energy from the combined solar and battery to run the cooling system (in kW_e)
                    if battery_soc[i] + solar_generation[i] > self.cooling_power*3600 * self.res:
                        # converting electrical power to thermal/cold power
                        cold_in = self.cooling_power * 3600 * self.res
                        # update battery_soc
                        if self.cooling_power * 3600 * self.res - solar_generation[i] >0:
                            battery_soc[i+1] = battery_soc[i] - max(0, self.cooling_power * 3600 * self.res - solar_generation[i])
                        else:
                            battery_soc[i+1] = battery_soc[i] +  solar_generation[i] - self.cooling_power * 3600 * self.res
                    else:# not enough energy to run the cooling device
                        # run the cooling device at a reduced power
                        cold_in = battery_soc[i] + solar_generation[i]
                        # update battery_soc to the min_soc
                        battery_soc[i+1] = battery_soc[i] - max(0, battery_soc[i])
                else: # if the coldhub is not too hot
                    # if the coldhub is not too cold
                    if self.coldhubs.temperature > self.coldhubs.T_hub_min:
                        # the cooling device runs at a reduced power level if there is a solar available
                        cold_in = 0 #min(solar_generation[i], self.cooling_power * 3600 * self.res) # Joule
                        # charge battery using the remaining power if any, and limit battery_soc with the battery_capacity that is soc_max
                        battery_soc[i+1] = min(battery_capacity, battery_soc[i] + max(solar_generation[i] - self.cooling_power * 3600 * self.res, 0) * battery_efficiency)
                        # charging efficiency is updated 9 Jan
                    else: # if the coldhub is too cold, then stop cooling it
                        battery_soc[i+1] = min(battery_capacity, battery_soc[i] + solar_generation[i] * battery_efficiency)
                        cold_in = 0

            else:# if solar generation is zero
                if self.coldhubs.temperature > self.coldhubs.T_hub_max:# too hot
                    # enough energy from battery for a good cooling (at the rated power)
                    if battery_soc[i] > self.cooling_power * 3600 * self.res:
                        cold_in = self.cooling_power * 3600 * self.res
                        battery_soc[i+1] = battery_soc[i] - self.cooling_power * 3600 * self.res
                    else: # if not enough energy in battery for a good cooling.
                        # Cooling operates at whatever energy available in battery
                        cold_in = max(battery_soc[i], 0)
                        # update battery_soc
                        battery_soc[i+1] = battery_soc[i] - max(battery_soc[i], 0)
                else:
                    if self.coldhubs.temperature > self.coldhubs.T_hub_min: # nor too cold or hot
                        # cooling operates at the rated power or a reduced power due to low battery_soc
                        # [notes] this could be zero, as T_hub is good to store food at this timestep
                        cold_in = max(min(battery_soc[i], self.cooling_power * 3600 * self.res),0) # Joule
                        battery_soc[i+1] = battery_soc[i] - cold_in
                    else: #  too cold
                        battery_soc[i+1] = battery_soc[i]
                        cold_in = 0

            # print(cold_in)
            # coldhub temperature update
            self.coldhubs.get_air_temperature(cold_in/self.cop, cold_out, self.am_temperature, self.res)
            # update time-variant variables
            T_hub[i] = self.coldhubs.temperature

            cold_power[i] = cold_in

        # plot results
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4,1)
        # make a little extra space between the subplots
        fig.subplots_adjust(hspace=0.5)
        day = self.time4plot

        idx1 = 0
        idx2 = len_data

        ax1.plot(day[idx1:idx2], battery_soc[idx1:idx2])
        ax2.plot(day[idx1:idx2], T_hub[idx1:idx2], day[idx1:idx2], self.coldhubs.T_hub_max*np.ones(len(day[idx1:idx2])),'--', day[idx1:idx2], self.coldhubs.T_hub_min*np.ones(len(day[idx1:idx2])),'--')
        ax2.set_ylabel('T_hub')
        ax3.plot(day[idx1:idx2], T_food[idx1:idx2],day[idx1:idx2], self.coldhubs.T_hub_max*np.ones(len(day[idx1:idx2])),'--', day[idx1:idx2], self.coldhubs.T_hub_min*np.ones(len(day[idx1:idx2])),'--')
        ax3.set_ylabel('T_food')
        ax4.plot(day[idx1:idx2], solar_generation[idx1:idx2], day[idx1:idx2], cold_power[idx1:idx2])
        # ax4.plot(day[idx1:idx2], cold_power[idx1:idx2])

        plt.show()


