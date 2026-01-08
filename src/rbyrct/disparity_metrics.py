def analyze_density_bias(reconstruction_volume, ground_truth):
    """
    Specifically calculates the SSIM (Structural Similarity Index) 
    for high-density voxels vs low-density voxels.
    """
    # High-density mask (Glandular tissue)
    mask = ground_truth > 0.22 
    
    error_in_dense_regions = np.mean(np.abs(reconstruction_volume[mask] - ground_truth[mask]))
    return {"dense_tissue_accuracy": 1 - error_in_dense_regions}
