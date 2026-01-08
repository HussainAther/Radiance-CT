import numpy as np

def get_weighted_attenuation(mu_adipose, mu_glandular, ratio, voltage_kvp=28):
    """
    Calculates weighted attenuation based on the Molybdenum spectrum.
    """
    # Characteristic peaks for Mo target
    peaks = {17.5: 0.6, 19.6: 0.4} 
    total_mu = 0
    for energy, weight in peaks.items():
        # Apply energy-dependent attenuation logic here
        total_mu += (mu_adipose * (1-ratio) + mu_glandular * ratio) * weight
    return total_mu
