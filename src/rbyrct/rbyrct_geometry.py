import numpy as np

def get_wu_weights(x0, y0, x1, y1, grid_shape):
    """
    Implements Wu's anti-aliasing to calculate voxel weights a_ij.
    Ensures smooth ray-sum integration across voxel boundaries.
    """
    weights = []
    # Normalized coordinates
    dx, dy = x1 - x0, y1 - y0
    steep = abs(dy) > abs(dx)
    
    if steep:
        x0, y0, x1, y1 = y0, x0, y1, x1
        dx, dy = dy, dx
    if x0 > x1:
        x0, x1, y0, y1 = x1, x0, y1, y0
        
    gradient = dy / dx if dx != 0 else 1.0
    
    # Iterate through x-coordinates to find pixel coverage
    x_end = round(x0)
    y_end = y0 + gradient * (x_end - x0)
    xpxl1 = x_end
    ypxl1 = int(y_end)
    
    for x in range(xpxl1, int(x1) + 1):
        inter_y = y0 + gradient * (x - x0)
        y_idx = int(inter_y)
        # Wu weights: fractional part determines the split between two adjacent voxels
        f_part = inter_y - y_idx
        
        if steep:
            weights.append(((y_idx, x), 1 - f_part))
            weights.append(((y_idx + 1, x), f_part))
        else:
            weights.append(((x, y_idx), 1 - f_part))
            weights.append(((x, y_idx + 1), f_part))
            
    return [w for w in weights if 0 <= w[0][0] < grid_shape[0] and 0 <= w[0][1] < grid_shape[1]]
