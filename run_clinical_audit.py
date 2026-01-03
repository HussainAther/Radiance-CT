import torch
from core.sensitivity_analysis import run_sensitivity_audit
from core.neural_field import NeuralAttenuationField

def test_clinical_benchmarks():
    """Automated test to verify Grainger & Allison standards."""
    model = NeuralAttenuationField()
    model.load_state_dict(torch.load("rbyrct_clinical_v1.pth"))
    
    # Load the ground truth phantom (The 'Gold Standard')
    phantom = torch.load("data/phantom_ground_truth.pt")
    
    results = run_sensitivity_audit(model, phantom)
    
    # ASSERTIONS: These are the hard 'Pass/Fail' gates for the patent
    assert results['calculated_sensitivity'] > 0.85, "FAILED: Sensitivity in dense tissue below 85%"
    assert results['recovery_percentage'] > 30.0, "FAILED: Sensitivity boost insufficient"
    
    print(f"✅ Audit Passed: Sensitivity at {results['calculated_sensitivity']*100:.1f}%")

if __name__ == "__main__":
    test_clinical_benchmarks()
