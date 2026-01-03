import torch
import numpy as np
from core.janus_projector import JanusProjector

def create_mock_phantom(size=128):
    """Creates a synthetic 3D phantom (e.g., a cylinder with a 'metal' implant)."""
    phantom = torch.zeros((size, size, size))
    # Create soft tissue body (Water-like HU ~0-100)
    z, y, x = torch.meshgrid(torch.linspace(-1, 1, size), 
                             torch.linspace(-1, 1, size), 
                             torch.linspace(-1, 1, size), indexing='ij')
    dist = torch.sqrt(x**2 + y**2 + z**2)
    phantom[dist < 0.8] = 50.0 
    
    # Create high-Z metal implant (Artifact source HU ~3000)
    phantom[0.4:0.5, 0.4:0.5, 0.4:0.5] = 3000.0
    return phantom

def generate_janus_simulation():
    """Simulates the Janus Hardware producing a Sinogram and an Occlusion Mask."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    projector = JanusProjector().to(device)
    phantom = create_mock_phantom().to(device)
    
    # Generate 180 sparse projection angles
    angles = torch.linspace(0, 3.14159, 180).to(device)
    
    # 1. Generate Ground Truth Sinogram (The 'Target')
    with torch.no_grad():
        raw_sinogram = projector(phantom, angles)
        
    # 2. Generate the Janus Selective Occlusion Mask
    # In reality, your hardware 'steers' rays. Here we mock it by 
    # identifying rays that hit the 'metal' and giving them 64% less 'weight'.
    mask = torch.ones_like(raw_sinogram)
    metal_indices = (raw_sinogram > 1500) # Simple threshold for mock metal
    mask[metal_indices] = 0.36 # 64% attenuation by the Janus shield
    
    # 3. Save for use in train.py
    torch.save(raw_sinogram, "data/raw_sinogram.pt")
    torch.save(mask, "data/janus_mask.pt")
    print("Mock Janus Data Generated: Artifact Starvation Mask applied.")

if __name__ == "__main__":
    generate_janus_simulation()
