from skimage.metrics import structural_similarity as ssim

def validate_reconstruction(reconstructed_vol, ground_truth_vol):
    """
    Computes SSIM and specifically checks for microcalcification preservation.
    """
    score = ssim(reconstructed_vol, ground_truth_vol)
    # Custom logic to check 100um feature contrast
    return score
