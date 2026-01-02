import torch
import torch.optim as optim
from core.neural_field import NeuralAttenuationField
from core.janus_projector import JanusProjector
from core.mart_optimizer import MARTOptimizer

def train_rbyrct():
    # 1. Setup Device (MPS for Mac, CUDA for NVIDIA)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # 2. Initialize the Patent Train™ Components
    model = NeuralAttenuationField().to(device)
    projector = JanusProjector().to(device)
    optimizer = MARTOptimizer(learning_rate=0.01, relaxation=0.8)
    
    # 3. Load Synthetic or Real Data (e.g., from a Huda-validated phantom)
    # measured_sino: The raw data from the scanner
    # angles: The specific angles used by the Janus Selective Occlusion
    measured_sino, angles = load_janus_data() 
    measured_sino = measured_sino.to(device)
    
    print(f"Starting Reconstruction: Target 64% Dose Reduction...")
    
    # 4. The Reconstruction Loop
    for epoch in range(1000):
        # Step the MART Optimizer
        # This updates the Neural Field based on Selective Occlusion physics
        loss = optimizer.step(model, projector, measured_sino, angles)
        
        if epoch % 100 == 0:
            # Calculate the Dose Concentration Ratio (DCR)
            dcr = projector.compute_dose_currency(measured_sino)
            print(f"Epoch {epoch} | KL Loss: {loss:.4f} | DCR: {dcr:.2f}")

    # 5. Export the Final Volume for DICOM/Flythrough
    final_volume = model.get_density_grid(resolution=512)
    torch.save(model.state_dict(), "rbyrct_engine_v1.pth")
    print("Reconstruction Complete. Artifact Starvation Successful.")

if __name__ == "__main__":
    train_rbyrct()
