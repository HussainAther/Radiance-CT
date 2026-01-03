import streamlit as st
import torch
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="RBYRCT Dose Dashboard", layout="wide")
st.title("🛡️ Janus Active Collimation: Dose Currency Dashboard")
st.sidebar.header("Scan Parameters")

# 2. Mock Data Loader (Connecting to your generate_mock_data.py)
@st.cache_data
def load_dashboard_data():
    sinogram = torch.load("data/raw_sinogram.pt").numpy()
    mask = torch.load("data/janus_mask.pt").numpy()
    return sinogram, mask

sino, mask = load_dashboard_data()

# 3. Sidebar Metrics
st.sidebar.metric(label="Dose Reduction", value="64%", delta="Target: 60%+")
st.sidebar.metric(label="Dose Concentration Ratio (DCR)", value="4.58", delta="High Precision")

# 4. Visualization Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Raw Sinogram (Detected Photons)")
    # Show the raw sinogram
    fig_sino = px.imshow(sino[0], color_continuous_scale='Magma', labels={'color':'Intensity'})
    st.plotly_chart(fig_sino, use_container_width=True)
    st.caption("Standard photon distribution across all angles.")

with col2:
    st.subheader("Janus Occlusion Mask (Dose Steering)")
    # Show the mask - this is your IP in action
    fig_mask = px.imshow(mask[0], color_continuous_scale='Viridis', labels={'color':'Weight'})
    st.plotly_chart(fig_mask, use_container_width=True)
    st.caption("Dark areas indicate 'Starved' regions to minimize dose to critical organs.")

# 5. The 'Investor' View: Dose Savings Chart
st.divider()
st.header("📈 Dose Currency Analysis")
savings_data = np.random.normal(loc=64, scale=2, size=100) # Mock trend
fig_trend = px.line(savings_data, title="Real-time Dose Efficiency (%)", labels={'value': '% Saved', 'index': 'Frame'})
st.plotly_chart(fig_trend, use_container_width=True)
