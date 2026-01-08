class RBYRCTWorkflow:
    def __init__(self, phantom_size=(128, 128)):
        self.size = phantom_size
        # Initial estimate x0 > 0 
        self.recon = np.ones(phantom_size) * 0.1 
        self.dose_currency = 0
        
    def scout_phase(self, num_rays=5000):
        """Phase 1: Low-dose random scout scan[cite: 96, 459]."""
        for _ in range(num_rays):
            # Stochastic per-ray sampling [cite: 335]
            # p_i = measure_random_ray()
            # self.recon = rbyrct_mart_update(self.recon, p_i, ...)
            self.dose_currency += 1
            
    def adaptive_phase(self, roi_coords, num_rays=15000):
        """Phase 2: Targeted Interrogation for Lesion Verification[cite: 97, 459]."""
        # Steering authority shift of 1.1577 cm used here [cite: 125]
        for _ in range(num_rays):
            # Focus rays on suspicious 2mm ROIs [cite: 126]
            # p_i = measure_steered_ray(roi_coords)
            # self.recon = rbyrct_mart_update(self.recon, p_i, ...)
            self.dose_currency += 1
            
    def check_convergence(self, tau=1e-3):
        """Full convergence strategy inner-loop."""
        # Iterate until relative change < tau
        pass
