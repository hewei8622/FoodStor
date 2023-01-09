class Food:
    def __init__(self, food_type, weight, name, heat_capacity, surface_area, initial_temperature, target_temperature, max_tem, min_tem,
                 shelf_life, life_remaining):
        self.food_type = food_type  # Type of food (e.g. fruit, vegetable, meat, etc.)
        self.weight = weight  # Weight of the food (kg)
        self.name = name  # Name of the food
        self.heat_capacity = heat_capacity  # Heat capacity of the food (J/kg*K)
        self.surface_area = surface_area  # Surface area of the food (m^2)
        self.temperature = initial_temperature  # Initial temperature of the food (°C)
        self.target_temperature = target_temperature  # Target storage temperature of the food (°C)
        self.max_tem = max_tem # max storage temperature [C]
        self.min_tem = min_tem # min storage temperature [C]

        # Shelf life of the food (days)
        # [notes] need to check
        self.shelf_life = shelf_life
        self.life_remaining = life_remaining

        # the ratio of the total surface area for heat transfer, i.e., the percentage of surface area is accounted for heat transfer
        # [notes] needs to check if supoorting data could be found or find a credible way to calculate the heat transfer
        self.area_coff = .3

    def get_cooling_demand(self, am_temperature, h_conv):

        # Calculate the heat transfer rate using the equation from the previous message
        Q2E = h_conv * self.surface_area * self.weight * (am_temperature - self.target_temperature)  # h x A x delta_T

        Q2T = self.heat_capacity * self.weight * (self.temperature - self.target_temperature)

        Q = Q2T + Q2E

        print("the cooling demand is " + str(Q) + " J")

        return Q

    def food_temperature_update(self, hub_temperature, h_conv):
        # hub_temperature -- coldhub's temperature [K]
        # h_conv -- conv heat transfer coeff [W/m2K]

        Q = 3600 * h_conv * self.surface_area * self.weight * self.area_coff * (self.temperature - hub_temperature) #J

        dT = Q / (self.heat_capacity * self.weight) # K or oC does not matter as dT is considered

        self.temperature = self.temperature - dT

        return Q








