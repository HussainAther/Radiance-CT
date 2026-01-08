import numpy as np

class JanusActiveCollimator:
    def __init__(self, dose_budget=0.36): # 36% of standard dose = 64% reduction
        self.dose_budget = dose_budget
        self.current_dose = 0.0
        
    def evaluate_ray_priority(self, ray_path, current_volume, variance_map):
        """
        Calculates if a ray should be fired based on the uncertainty 
        in the tissue it traverses.
        """
        # 1. Sum the variance along the ray path
        # High variance = high uncertainty (needs more photons)
        path_uncertainty = np.sum(variance_map[ray_path])
        
        # 2. Check for BI-RADS Pattern 4 (Dense Tissue)
        # We prioritize rays passing through high-density regions
        is_dense_tissue = np.any(current_volume[ray_path] > 0.22) # Glandular threshold
        
        # 3. Decision Logic: Fire if uncertainty is high OR it's a dense "priority" area
        priority_score = path_uncertainty * (2.0 if is_dense_tissue else 1.0)
        
        return priority_score > self.get_dynamic_threshold()

    def get_dynamic_threshold(self):
        # Adjust threshold as we approach the dose limit
        return 0.5 * (1 + (self.current_dose / self.dose_budget))

#
