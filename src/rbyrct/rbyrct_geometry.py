import numpy as np

def rbyrct_mart_update(recon_volume, p_i, ray_path_weights, lmbda=0.1):
    """
    Implements the Multiplicative Algebraic Reconstruction Technique (MART).
    
    Args:
        recon_volume: 1D or 2D array of electronic densities (f_j).
        p_i: Measured projection data for the current ray.
        ray_path_weights: List of (index, a_ij) tuples where a_ij is the Wu weight.
        lmbda: Relaxation parameter (0.1 - 2.0).
    """
    # 1. Calculate the current projection estimate: sum(a_il * f_l)
    current_projection = 0.0
    for idx, a_ij in ray_path_weights:
        current_projection += a_ij * recon_volume[idx]
    
    # 2. Compute the update ratio (p_i / estimate)
    if current_projection > 0:
        ratio = p_i / current_projection
        
        # 3. Apply the localized multiplicative power update
        # f_j^(k+1) = f_j^k * (ratio)^(lambda * a_ij)
        for idx, a_ij in ray_path_weights:
            recon_volume[idx] *= (ratio ** (lmbda * a_ij))
            
    return recon_volume
