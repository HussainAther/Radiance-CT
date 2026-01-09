import rbyrct_solver
import rbyrct_geometry

class RBYRCT_Engine:
    """
    Standardized API for integrating RBYRCT into clinical research workflows.
    """
    def __init__(self, mode='adaptive'):
        self.mode = mode # 'scout' or 'adaptive'
        
    def reconstruct(self, projections, geometry_data):
        # 1. Generate Wu Weights
        # 2. Run MART Power-Law update
        # 3. Return voxelized density map
        pass

    def get_dose_report(self):
        # Calculate MGD (Mean Glandular Dose) based on ray count
        pass
