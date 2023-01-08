class EnergyStorage:
    def __init__(self, capacity, energy_efficiency, energy_form, name, energy_density, energy_costs):
        self.capacity = capacity
        self.energy_efficiency = energy_efficiency  # Energy efficiency of the storage system
        self.energy_form = energy_form  # Form of the stored energy (e.g. electrical, thermal, mechanical)
        self.energy_density = energy_density  # Energy density of the stored energy (J/m^3)
        self.energy_costs = energy_costs  # Costs of the storage system ($/J)
        self.name = name

    def get_storage_capacity(self, volume):
        """
        Calculates the storage capacity of the system.

        Parameters:
        volume (float): Volume of the storage system (m^3)

        Returns:
        float: Storage capacity of the system (J)
        """
        return volume * self.energy_density

    def get_charge_efficiency(self, input_energy, stored_energy):
        """
        Calculates the charge efficiency of the system.

        Parameters:
        input_energy (float): Input energy to the system (J)
        stored_energy (float): Stored energy in the system (J)

        Returns:
        float: Charge efficiency of the system (0-100%)
        """
        return stored_energy / input_energy * 100

    def get_discharge_efficiency(self, output_energy, stored_energy):
        """
        Calculates the discharge efficiency of the system.

        Parameters:
        output_energy (float): Output energy from the system (J)
        stored_energy (float): Stored energy in the system (J)

        Returns:
        float: Discharge efficiency of the system (0-100%)
        """
        return output_energy / stored_energy * 100

    def get_energy_costs(self, input_energy):
        """
        Calculates the energy costs of the system.

        Parameters:
        input_energy (float): Input energy to the system (J)

        Returns:
        float: Energy costs of the system ($)
        """
        return input_energy * self.energy_costs
