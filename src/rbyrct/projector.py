import numpy as np
from .geometry import get_siddon_path_lengths
from .spectrum import get_weighted_attenuation

class RBYRCTProjector:
    def __init__(self, volume_dims, voxel_size, source_io=10**6):
        """
        source_io: Initial photon count (I0) from the Molybdenum source.
        """
        self.dims = volume_dims
        self.voxel_size = voxel_size
        self.I0 = source_io

    def forward_project_ray(self, source, detector_pixel, volume):
        """
        Performs the Beer-Lambert calculation for a single ray (Ray-By-Ray).
        I = I0 * exp(-sum(mu_i * ds_i))
        """
        # 1. Get exact path lengths through each voxel using Siddon's Algorithm
        path_segments = get_siddon_path_lengths(
            source, detector_pixel, self.voxel_size, self.dims
        )
        
        # 2. Accumulate the total optical depth (sum of attenuation * distance)
        total_exponent = 0.0
        for voxel_idx, ds in path_segments:
            # Retrieve attenuation (mu) for this specific voxel
            # This is where your BI-RADS density patterns are stored
            mu_v = volume[voxel_idx] 
            
            # Apply the weighted attenuation (accounting for 17.5/19.6 keV peaks)
            weighted_mu = get_weighted_attenuation(mu_v)
            
            total_exponent += weighted_mu * ds
            
        # 3. Apply Beer-Lambert Law
        intensity = self.I0 * np.exp(-total_exponent)
        
        return intensity

    def generate_projections(self, volume, geometry_params, collimator):
        """
        The main loop that generates the 'Janus' detector data.
        Integrates with the active collimator to 'starve' unnecessary rays.
        """
        projections = {}
        for angle in geometry_params.angles:
            detector_frame = np.zeros(geometry_params.detector_shape)
            
            for pixel_idx in np.ndindex(geometry_params.detector_shape):
                # Check with the Collimator: Should we fire this ray?
                if collimator.should_fire_ray(angle, pixel_idx):
                    detector_frame[pixel_idx] = self.forward_project_ray(
                        geometry_params.source_pos[angle],
                        geometry_params.pixel_pos[pixel_idx],
                        volume
                    )
                else:
                    # Dose Reduction: Ray is starved, intensity is 0
                    detector_frame[pixel_idx] = 0.0
                    
            projections[angle] = detector_frame
            
        return projections
