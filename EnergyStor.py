class EnergyStorage:
    def __init__(self, capacity, energy_efficiency, energy_form, name, energy_density, energy_costs):
        self.capacity = capacity # energy_capacity in [J]
        self.energy_efficiency = energy_efficiency  # Energy efficiency of the storage system
        self.energy_form = energy_form  # Form of the stored energy (e.g. electrical, thermal, mechanical)
        self.energy_density = energy_density  # Energy density of the stored energy (kWh/m^3)
        self.energy_costs = energy_costs  # Costs of the storage system ($/J)
        self.name = name

