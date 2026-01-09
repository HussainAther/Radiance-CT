import numpy as np

def localized_mart_step(recon_volume, p_i, wu_weights, lmbda=0.1):
    """
    Performs the Multiplicative Update: f_j^(k+1) = f_j^k * (p_i / sum(a_il*f_l))^(lambda * a_ij)
    """
    # 1. Forward Projection: Calculate the current ray sum
    current_ray_sum = sum(a_ij * recon_volume[idx] for idx, a_ij in wu_weights)
    
    if current_ray_sum > 0:
        # 2. Ratio Calculation (p_i is the measured data)
        ratio = p_i / current_ray_sum
        
        # 3. Multiplicative Update
        for idx, a_ij in wu_weights:
            # Artifact Starvation happens here: non-consistent ghosts lose density
            recon_volume[idx] *= (ratio ** (lmbda * a_ij))
            
    return recon_volume
