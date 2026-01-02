import torch
import torch.nn as nn

class MARTOptimizer:
    """
    Differentiable MART Optimizer for RBYRCT.
    Optimizes the Neural Attenuation Field (NAF) by maximizing entropy
    and enforcing non-negativity through multiplicative updates.
    """
    def __init__(self, learning_rate=0.01, relaxation=1.0):
        self.lr = learning_rate
        self.lambda_reg = relaxation

    def step(self, model, projector, measured_sinogram, angles):
        """
        Performs one MART iteration:
        1. Forward Project the current model state.
        2. Calculate the Ratio (Measured / Projected).
        3. Update the weights multiplicatively.
        """
        # Get current state from the Neural Attenuation Field
        current_density = model.get_density_grid() 
        
        # 1. Forward Projection (using your Janus Projector)
        projected_sinogram = projector(current_density, angles)
        
        # 2. Compute the Multiplicative Correction Factor
        # Note: We add a small epsilon to avoid division by zero
        eps = 1e-8
        ratio = (measured_sinogram + eps) / (projected_sinogram + eps)
        
        # 3. Back-projection of the correction
        # This uses the transpose of the projector logic to distribute error
        correction_map = projector.back_project(ratio, angles)
        
        # 4. Multiplicative Update
        # f_new = f_old * (correction)^lambda
        new_density = current_density * torch.pow(correction_map, self.lambda_reg)
        
        # Update model parameters
        model.update_density(new_density)
        
        return self.compute_loss(projected_sinogram, measured_sinogram)

    def compute_loss(self, projected, measured):
        """Kullback-Leibler (KL) Divergence is the natural loss for MART."""
        return torch.sum(measured * torch.log(measured / projected))
