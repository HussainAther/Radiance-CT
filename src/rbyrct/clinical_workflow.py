class ClinicalThroughputSim:
    def __init__(self, standard_scan_time_min=15):
        self.base_time = standard_scan_time_min

    def calculate_efficiency_gain(self, dose_reduction_pct):
        """
        Calculates throughput increase based on reduced tube cooling 
        requirements and optimized ray-by-ray paths.
        """
        # 64% dose reduction = lower thermal stress on X-ray anode
        thermal_save = dose_reduction_pct * 0.5 
        optimized_time = self.base_time * (1 - (thermal_save / 100))
        
        patients_per_8hr_shift = 480 / optimized_time
        return round(patients_per_8hr_shift, 1)
