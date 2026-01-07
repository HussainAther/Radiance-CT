import numpy as np

def get_siddon_path_lengths(source, detector_pixel, voxel_size, volume_origin, volume_dims):
    """
    Siddon's Algorithm: Calculates the intersection length of a single ray 
    through every voxel it touches in the RBYRCT volume.
    """
    # 1. Parameterize the ray: R(alpha) = P1 + alpha*(P2 - P1)
    p1 = source
    p2 = detector_pixel
    
    # 2. Calculate entry and exit alphas for the entire volume bounding box
    # (Standard ray-box intersection)
    
    # 3. Find the set of 'alphas' where the ray crosses voxel planes (x, y, z)
    # This is the 'Ray-By-Ray' magic—we find every single intersection point.
    
    # simplified representation for the loop:
    alphas = sorted(np.concatenate([alphas_x, alphas_y, alphas_z]))
    
    path_segments = []
    for k in range(1, len(alphas)):
        # Midpoint of the segment in alpha-space
        mid_alpha = (alphas[k] + alphas[k-1]) / 2.0
        
        # Find the voxel index (i, j, k) for this segment
        voxel_idx = find_voxel_at_alpha(p1, p2, mid_alpha)
        
        # Calculate the actual physical length (ds) of this segment
        # Length = distance(p1, p2) * (alpha[k] - alpha[k-1])
        dist = np.linalg.norm(p2 - p1) * (alphas[k] - alphas[k-1])
        
        path_segments.append((voxel_idx, dist))
        
    return path_segments
