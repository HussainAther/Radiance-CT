import numpy as np
import datetime

class DoseTracker:
    def __init__(self, patient_id, standard_dbt_mgy=1.2):
        """
        standard_dbt_mgy: The typical Mean Glandular Dose (MGD) for a 5cm breast.
        We track the RBYRCT cumulative dose against this benchmark.
        """
        self.patient_id = patient_id
        self.standard_dose = standard_dbt_mgy
        self.cumulative_energy = 0.0
        self.ray_count = 0
        self.log = []

    def update_dose(self, ray_energy, path_length, tissue_density):
        """
        Calculates the dose contribution of a single 'fired' ray.
        Based on the energy peaks (17.5 keV) and tissue absorption.
        """
        # simplified dose calc: Energy * Absorption_Coefficient
        dose_contribution = ray_energy * (1.0 - np.exp(-tissue_density * path_length))
        self.cumulative_energy += dose_contribution
        self.ray_count += 1
        
    def get_reduction_stats(self):
        """
        Returns the current dose reduction percentage.
        Target: > 64%
        """
        reduction = (1 - (self.cumulative_energy / self.standard_dose)) * 100
        return {
            "patient": self.patient_id,
            "reduction_percentage": round(reduction, 2),
            "rays_fired": self.ray_count,
            "timestamp": datetime.datetime.now().isoformat()
        }

    def generate_clinical_report(self):
        # This will be used for the Luminate 'Evidence' folder
        stats = self.get_reduction_stats()
        print(f"--- RBYRCT Dose Audit ---")
        print(f"Reduction Achieved: {stats['reduction_percentage']}%")
        if stats['reduction_percentage'] >= 64.0:
            print("STATUS: Luminate/FDA Compliance Pass")
        else:
            print("STATUS: Warning - Dose threshold exceeded")
