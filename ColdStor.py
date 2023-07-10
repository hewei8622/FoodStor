class ColdStorage:
    def __init__(self, capacity, energy_efficiency, energy_form, name, energy_density, energy_costs, T_melt, h_fg, heat_capacity, m):
        self.capacity = capacity # energy_capacity in [J]
        self.energy_efficiency = energy_efficiency  # Energy efficiency of the storage system
        self.energy_form = energy_form  # Form of the stored energy (e.g. electrical, thermal, mechanical)
        self.energy_density = energy_density  # Energy density of the stored energy (kWh/m^3)
        self.energy_costs = energy_costs  # Costs of the storage system ($/J)
        self.name = name
        self.melting_temperature = T_melt
        self.latent_heat = h_fg
        self.heat_capacity = heat_capacity
        self.mass = m

    def get_cost_mass(self):
        return self.energy_costs*self.mass

