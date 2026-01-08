import numpy as np

class RBYRCTProjector:
    def __init__(self, volume_dims=(128, 128), voxel_size=1.0):
        self.dims = volume_dims
        self.voxel_size = voxel_size

    def forward_project_ray(self, source, pixel, volume):
        """
        Calculates the line integral of attenuation coefficients along a ray.
        Implements Beer-Lambert: I = I0 * exp(-sum(mu_i * l_i))
        """
        # Vector from source to detector pixel
        ray_vector = pixel - source
        distance = np.linalg.norm(ray_vector)
        unit_vector = ray_vector / distance
        
        # Sampling along the ray (step size = half a voxel for accuracy)
        step_size = self.voxel_size / 2.0
        num_steps = int(distance / step_size)
        
        total_attenuation = 0.0
        
        for i in range(num_steps):
            # Current position in 3D space
            current_pos = source + (i * step_size * unit_vector)
            
            # Convert spatial coordinates to voxel indices
            idx = (current_pos / self.voxel_size).astype(int)
            
            # Check if we are still inside the phantom volume
            if np.all(idx >= 0) and np.all(idx < self.dims):
                # Beer-Lambert: mu is the attenuation coefficient at this voxel
                mu = volume[idx[0], idx[1]]
                total_attenuation += mu * step_size
                
        return total_attenuation
