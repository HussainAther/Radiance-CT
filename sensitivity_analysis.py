import torch
import numpy as np

def run_sensitivity_audit(model, phantom_ground_truth, resolution=512):
    """
    Calculates the Sensitivity Gap recovery.
    Standard Mammography in BI-RADS D: ~48-50% Sensitivity.
    RBYRCT Goal: >85% Sensitivity via Artifact Starvation.
    """
    # 1. Generate the Predicted Volume from the Neural Field
    reconstruction = model.get_density_grid(resolution=resolution)
    
    # 2. Identify 'True Positive' Lesions from the Huda-validated Phantom
    # We look for Hounsfield Units in the 'carcinoma' range (100-300 HU)
    tp_mask = (phantom_ground_truth > 100) & (phantom_ground_truth < 300)
    
    # 3. Calculate True Positives in Reconstruction
    # We use a threshold to see if the engine resolved the mass despite density
    detected_mask = (reconstruction > 100) & (reconstruction < 300)
    
    true_positives = torch.sum(tp_mask & detected_mask).item()
    false_negatives = torch.sum(tp_mask & ~detected_mask).item()
    
    sensitivity = true_positives / (true_positives + false_negatives + 1e-8)
    
    # 4. Sensitivity Recovery Metric
    # This represents the "Clinical Value" of your 64% dose reduction
    standard_sensitivity = 0.50 # Baseline for BI-RADS D from G&A
    recovery_boost = (sensitivity - standard_sensitivity) / standard_sensitivity
    
    return {
        "calculated_sensitivity": sensitivity,
        "standard_baseline": standard_sensitivity,
        "recovery_percentage": recovery_boost * 100
    }
