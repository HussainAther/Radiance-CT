# Contributing to Radiance-CT (RBYRCT)

Thank you for contributing to the future of ultra-low-dose medical imaging. To maintain our **64% dose reduction** target and ensure clinical validity against **Grainger & Allison (7th Ed)**, all contributors must follow this workflow.

## 🩺 Clinical Validation Requirements
Any code affecting the reconstruction engine (`core/`) must pass the following benchmarks:
1. **Dose Integrity:** Must maintain a Dose Concentration Ratio (DCR) >= 4.5.
2. **Sensitivity:** Must achieve >85% sensitivity in simulated BI-RADS D (Extremely Dense) phantoms.
3. **Artifact Starvation:** No introduction of new streak artifacts in high-Z (metal) scenarios.

## 🚀 Git Workflow (The "Patent Train" Process)

### 1. Branching Policy
Create a feature branch for every update. Use the following naming convention:
- `feat/` for new physics or AI modules (e.g., `feat/janus-steering`)
- `fix/` for bug fixes
- `val/` for new clinical validation scripts

```bash
git checkout -b feat/your-feature-name
2. Commit Message Standards

We use Conventional Commits. This allows us to generate an automated "Evidence Log" for patent filings.

Format: type(scope): description

Example: feat(projector): implement 17.5keV Molybdenum spectral peaks

3. Pull Request (PR) Process

When opening a PR, you must include the Clinical Audit Report:

Run python run_clinical_audit.py.

Attach the generated metrics (Sensitivity, SSIM, PSNR) to the PR description.

Reference the specific chapter of Grainger & Allison or Huda that justifies your changes.

🧪 Testing Environment
Before pushing, ensure your local environment matches the production requirements:

PyTorch 2.0+

CUDA 11.8+ (for differentiable ray-tracing)

Streamlit (for the Dose Dashboard)

⚖️ Intellectual Property
By contributing, you agree that all code remains under the primary project license and supports the "Active Collimation" patent family.

“In medical imaging, we don’t move fast and break things. We move precisely and save lives.”


