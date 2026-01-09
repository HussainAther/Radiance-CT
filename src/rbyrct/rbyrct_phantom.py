import numpy as np

def generate_rbyrct_phantom(size=128, density_level='Pattern4'):
    """
    Generates a digital breast phantom for RBYRCT validation.
    Pattern 4 = Extremely Dense (>75% glandular tissue).
    """
    # Initialize with fatty tissue density (~0.9 g/cm^3)
    phantom = np.ones((size, size)) * 0.18 
    
    # Create the 'Extremely Dense' glandular structure (Pattern 4)
    center = size // 2
    y, x = np.ogrid[:size, :size]
    mask = (x - center)**2 + (y - center)**2 <= (size // 2.5)**2
    phantom[mask] = 0.22 # Increased density for glandular tissue
    
    # Insert a 2mm 'Suspicious' Lesion (High Contrast +)
    # At 128x128, 2mm is roughly a 2-3 pixel radius
    lesion_center = (int(size * 0.4), int(size * 0.6))
    lesion_mask = (x - lesion_center[1])**2 + (y - lesion_center[0])**2 <= 2**2
    phantom[lesion_mask] = 0.45 # Tumor density
    
    return phantom
