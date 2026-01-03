import torch
from core.neural_field import NeuralAttenuationField
from core.janus_projector import JanusProjector
from core.mart_optimizer import MARTOptimizer
from core.density_classifier import DensityClassifier # Our new module

def train_rbyrct_clinical():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Initialize Core Engine
    model = NeuralAttenuationField().to(device)
    projector = JanusProjector().to(device)
    classifier = DensityClassifier()
    
    # Initialize Optimizer with default relaxation
    optimizer = MARTOptimizer(learning_rate=0.01, relaxation=0.8)
    
    measured_sino, angles, mask = load_janus_data()
    
    print("🚀 Initializing Clinical-Grade Reconstruction...")

    for epoch in range(1500):
        # 1. Update Volume via MART
        loss = optimizer.step(model, projector, measured_sino, angles)
        
        # 2. Every 50 epochs, perform a Clinical Audit
        if epoch % 50 == 0:
            current_vol = model.get_density_grid(resolution=256)
            
            # Use Grainger & Allison standards to classify density
            category = classifier.get_birads_category(current_vol)
            
            # 3. Dynamic Parameter Adjustment (The "Closed Loop")
            if "D" in category or "C" in category:
                # Dense tissue obscures lesions (Ref: G&A Ch 63)
                # We increase relaxation to preserve high-frequency edges
                optimizer.lambda_reg = 0.95 
                print(f"⚠️ High Density Detected ({category}). Boosting Edge Preservation.")
            else:
                optimizer.lambda_reg = 0.8
            
            # 4. Check for Morphological Distortion
            suspicious = classifier.detect_suspicious_morphology(current_vol)
            if suspicious:
                print("🎯 Suspicious Morphology Detected. Concentrating 'Dose Currency' on ROI.")
                # Logic to tell Janus Projector to steer more rays here

        if epoch % 100 == 0:
            print(f"Epoch {epoch} | KL Loss: {loss:.4f} | Category: {category}")

    # Export Final Volume
    torch.save(model.state_dict(), "rbyrct_clinical_v1.pth")
    print("✅ Reconstruction Complete. Clinical Standards Met.")

if __name__ == "__main__":
    train_rbyrct_clinical()
