import numpy as np
from .solver import RBYRCT_MART
from .projector import RBYRCTProjector
from .utils.topas_loader import TopasLoader

class TopasPhysicsOptimizer:
    def __init__(self, mart_solver: RBYRCT_MART, projector: RBYRCTProjector):
        self.solver = mart_solver
        self.projector = projector
        self.learning_rate = 0.01

    def optimize_weights_from_topas(self, topas_output_path, sim_geometry):
        """
        Calculates the discrepancy between our Light Field engine 
        and the TOPAS Monte Carlo truth.
        """
        loader = TopasLoader(topas_output_path)
        
        # 1. Load the 'Golden Truth' from TOPAS (e.g., DoseToMedium or Fluence)
        topas_truth, meta = loader.load_scorer_output("BinnedScorer.csv")
        
        # 2. Run our analytical Forward Projector on the same geometry
        analytical_estimate = self.projector.generate_projections(
            self.solver.volume, sim_geometry
        )
        
        # 3. Calculate Error Map
        # We look for where Beer-Lambert fails (usually due to scatter)
        error_map = topas_truth - analytical_estimate
        
        # 4. Update MART Weights
        # If TOPAS shows more energy in a voxel than Beer-Lambert predicts,
        # it's likely scatter. We adjust the MART weights to compensate.
        self.solver.weights += self.learning_rate * error_map
        
        print(f"Physics Optimization Complete. Mean Error: {np.mean(np.abs(error_map))}")
