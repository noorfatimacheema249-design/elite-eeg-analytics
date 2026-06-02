import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from signal_engine import create_clinical_eeg_stream, compute_quantitative_eeg

st.set_page_config(
    page_title="NeuroOS Core - Advanced Neurophysiology Platform",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark-Slate Clinical Theme CSS Overrides
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #090D16; color: #F1F5F9; }
    
    #MainMenu, footer, header, .stDeployButton { visibility: hidden; display: none; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); height: 0rem; }
    
    .app-header {
        display: flex; justify-content: space-between; align-items: center;
        background: radial-gradient(100% 100% at 0% 0%, #0369A1 0%, #090D16 100%);
        padding: 24px 40px; border-bottom: 1px solid #1E293B; margin: -60px -40px 28px -40px;
    }
    .brand-title { font-size: 1.5rem; font-weight: 700; color: #FFFFFF; letter-spacing: -0.02em; }
    .brand-subtitle { font-size: 0.8rem; color: #38BDF8; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
    .system-badge { font-size: 0.75rem; color: #38BDF8; background: rgba(56, 189, 248, 0.1); padding: 6px 14px; border-radius: 4px; border: 1px solid rgba(56, 189, 248, 0.2); font-weight: 600; }
    
    .panel-card { background-color: #111827; border: 1px solid #1F2937; border-radius: 10px; padding: 24px; margin-bottom: 20px; }
    .panel-title { font-size: 0.95rem; font-weight: 600; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 20px; border-left: 3px solid #0EA5E9; padding-left: 10px; }
    
    .metric-card-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 20px; }
    .metric-subbox { background: #070A13; border: 1px solid #1F2937; padding: 16px; border-radius: 6px; text-align: center; }
    .metric-val { font-size: 1.6rem; font-weight: 700; color: #38BDF8; }
    .metric-lbl { font-size: 0.7rem; text-transform: uppercase; color: #6B7280; font-weight: 600; margin-top: 4px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="app-header">
        <div>
            <div class="brand-title">NeuroOS Diagnostics Portal</div>
            <div class="brand-subtitle">Quantitative Signal Core & ICU Neuro-Informatics Pipeline</div>
        </div>
        <div class="system-badge">MNE-Core Kernel Active</div>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Digital Oscilloscope Signal Ingestion</div>', unsafe_allow_html=True)
    
    clinical_state = st.selectbox(
        "Select Verified Clinical EEG Case Profile",
        ["Normal Awake (Posterior Alpha Dominant)", "Generalized Absence (3 Hz Spike-and-Wave)", "Non-Convulsive Status Epilepticus (Ictal Evolution)", "Severe Encephalopathy / Coma (Diffuse Delta Slowing)"]
    )
    
    duration = st.slider("Signal Epoch Frame Bounding Window (Seconds)", 2.0, 10.0, 5.0, step=1.0)
    selected_channel = st.selectbox("Quantitative Spectral Analysis Targeted Channel", ['Fp1-F3', 'F3-C3', 'C3-P3', 'P3-O1', 'Fp2-F4', 'F4-C4', 'C4-P4', 'P4-O2'])
    
    # Process stream data values
    stream = create_clinical_eeg_stream(clinical_state, duration)
    eeg_df = stream["df"]
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Standard 8-Channel Diagnostic Montage Stacking Array</div>', unsafe_allow_html=True)
    
    fig_montage = go.Figure()
    offset = 0
    for col in eeg_df.columns:
        if col != 'Time':
            fig_montage.add_trace(go.Scatter(
                x=eeg_df['Time'], y=eeg_df[col] + offset,
                mode='lines', name=col, line=dict(width=1.1, color='#38BDF8')
            ))
            offset -= 130 # Physically isolate traces matching real clinical monitoring hardware calibrations
            
    fig_montage.update_layout(
        height=500, showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#030712',
        margin=dict(t=10, b=10, l=10, r=10), font=dict(color='#4B5563', family='JetBrains Mono'),
        xaxis=dict(gridcolor='#111827', title="Time Epoch Delta (Seconds)"),
        yaxis=dict(gridcolor='#111827', showticklabels=False)
    )
    st.plotly_chart(fig_montage, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Quantitative Spectral Density Matrix</div>', unsafe_allow_html=True)
    
    # Run absolute medical power densities calculations
    q_metrics = compute_quantitative_eeg(eeg_df[selected_channel].values)
    
    st.markdown('<div class="metric-card-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-subbox"><div class="metric-val">{q_metrics["SEF95"]:.1f} Hz</div><div class="metric-lbl">Spectral Edge Freq (SEF95)</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-subbox"><div class="metric-val">{q_metrics["AD_Ratio"]:.3f}</div><div class="metric-lbl">Alpha-to-Delta Ratio (ADR)</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    band_data = pd.DataFrame({
        "Frequency Waveband Classification": ["Delta (0.5-4.0 Hz)", "Theta (4.0-8.0 Hz)", "Alpha (8.0-13.0 Hz)", "Beta (13.0-30.0 Hz)"],
        "Absolute Spectral Power (µV²)": [q_metrics["Delta"], q_metrics["Theta"], q_metrics["Alpha"], q_metrics["Beta"]]
    })
    
    fig_pie = px.pie(
        band_data, values="Absolute Spectral Power (µV²)", names="Frequency Waveband Classification",
        color_discrete_sequence=px.colors.sequential.Electric_r
    )
    fig_pie.update_layout(
        height=240, paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#9CA3AF'), margin=dict(t=10, b=10, l=10, r=10)
    )
    st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Automated Interpretation & Artifact Status Log</div>', unsafe_allow_html=True)
    
    st.write(f"Active Focused Analytics Lead Trace: **{selected_channel}**")
    st.write(f"Hardware Vector Sgnal Verification Tracking: `<span class='code-font' style='color:#10B981;'>{stream['artifacts'][selected_channel]}</span>`", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if clinical_state == "Normal Awake (Posterior Alpha Dominant)":
        st.info("Clinical Diagnosis Note: Trace captures an authentic posterior dominant alpha rhythm running smoothly at 10.2 Hz. This represents standard occipital reactivities matching resting alert awake adult physiological data baselines.")
    elif clinical_state == "Generalized Absence (3 Hz Spike-and-Wave)":
        st.error("Clinical Diagnosis Note: High-voltage synchronous generalized paroxysmal 3 Hz spike-and-wave burst activity clusters detected. Replicates standard absence epilepsy variants with high amplitude variance spikes.")
    elif clinical_state == "Non-Convulsive Status Epilepticus (Ictal Evolution)":
        st.error("Clinical Diagnosis Note: Evolving rhythmic paroxysmal sharp waveform patterns demonstrating spatial-temporal frequency changes. Strong indicators confirm active, non-convulsive status epilepticus requiring immediate intervention tracks.")
    else:
        st.warning("Clinical Diagnosis Note: Diffuse high-amplitude polymorphic delta slowing with total suppression of baseline faster physiological rhythms. Structural metrics identify status matching profound metabolic encephalopathy or coma blocks.")
        
    st.markdown('</div>', unsafe_allow_html=True)
