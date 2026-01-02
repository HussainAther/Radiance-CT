import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader

class JanusDataset(Dataset):
    """
    Utility for loading steerable X-ray projection data.
    Handles sparse sinograms and associated Selective Occlusion masks.
    """
    def __init__(self, sinogram_path, mask_path=None, num_angles=180):
        # In a real scenario, you'd load DICOM-CT-PD or HDF5 files
        self.sinogram = torch.load(sinogram_path) 
        self.angles = torch.linspace(0, 3.14159, num_angles)
        
        # The mask represents the 'Active Collimation' state for each ray
        if mask_path:
            self.mask = torch.load(mask_path)
        else:
            self.mask = torch.ones_like(self.sinogram)

    def __len__(self):
        return 1 # For reconstruction, we often treat the full sinogram as one sample

    def __getitem__(self, idx):
        return {
            "projections": self.sinogram,
            "angles": self.angles,
            "mask": self.mask
        }

def load_janus_data(batch_size=1):
    """
    Wrapper to initialize the data pipeline.
    Ensures the data is formatted for the 'Dose Currency' calculations.
    """
    # Use synthetic paths for now; replace with real clinical data later
    dataset = JanusDataset("data/raw_sinogram.pt", "data/janus_mask.pt")
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
    
    # Return a single batch for the reconstruction loop
    batch = next(iter(loader))
    return batch["projections"], batch["angles"], batch["mask"]
