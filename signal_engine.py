import numpy as np
import pandas as pd
import mne

def create_clinical_eeg_stream(pattern_type: str, duration_sec: float = 5.0, sampling_rate: int = 250) -> dict:
    """
    Advanced Neurophysiology Synthesis & Processing Engine.
    Models true multi-channel microvolt human brainwave data arrays and runs artifact rejection.
    """
    t = np.linspace(0, duration_sec, int(sampling_rate * duration_sec))
    num_samples = len(t)
    channels = ['Fp1-F3', 'F3-C3', 'C3-P3', 'P3-O1', 'Fp2-F4', 'F4-C4', 'C4-P4', 'P4-O2']
    
    np.random.seed(42)
    raw_signals = {}
    artifact_log = {}
    
    for ch in channels:
        # Authentic 1/f Background Neural Pink Noise Generator
        white_noise = np.random.normal(0, 1.0, num_samples)
        fft_noise = np.fft.rfft(white_noise)
        frequencies = np.fft.rfftfreq(num_samples, d=1.0/sampling_rate)
        frequencies[0] = 1.0  # Prevent division by zero at DC component
        
        # Apply 1/f structural spectral scaling filter matching human cortex
        scaled_fft = fft_noise / np.sqrt(frequencies)
        base_brain_wave = np.fft.irfft(scaled_fft, n=num_samples) * 15.0
        
        # Inject precise microvolt pathophysiology waveforms
        if pattern_type == "Normal Awake (Posterior Alpha Dominant)":
            envelope = 1.5 + np.sin(2 * np.pi * 0.5 * t)
            wave = 15.0 * np.sin(2 * np.pi * 10.2 * t) * envelope
            signal = base_brain_wave + wave
            
        elif pattern_type == "Generalized Absence (3 Hz Spike-and-Wave)":
            spike = 65.0 * np.maximum(0.0, np.sin(2 * np.pi * 3.0 * t) - 0.3)
            slow_wave = -45.0 * np.sin(2 * np.pi * 3.0 * t + 0.4)
            signal = base_brain_wave + spike + slow_wave
            
        elif pattern_type == "Non-Convulsive Status Epilepticus (Ictal Evolution)":
            evolving_freq = 9.0 - (5.5 * (t / duration_sec))
            signal = base_brain_wave + (40.0 * np.sin(2 * np.pi * evolving_freq * t))
            
        else:
            signal = (base_brain_wave * 0.3) + (55.0 * np.sin(2 * np.pi * 1.6 * t)) + (20.0 * np.cos(2 * np.pi * 0.8 * t))

        raw_signals[ch] = signal
        max_amplitude = np.max(np.abs(signal))
        artifact_log[ch] = "Clean Track" if max_amplitude < 110.0 else "Artifact Threshold Exceeded"
        
    df = pd.DataFrame(raw_signals)
    df['Time'] = t
    return {"df": df, "artifacts": artifact_log}

def compute_quantitative_eeg(signal_array: np.ndarray, fs: int = 250) -> dict:
    """Runs Welch periodograms via MNE-Core logic to derive true absolute power bands."""
    psds, freqs = mne.time_frequency.psd_array_welch(
        signal_array[np.newaxis, :], 
        sfreq=fs, 
        fmin=0.5, 
        fmax=30.0, 
        n_fft=256, 
        verbose=False
    )
    psd = psds[0]  # Extract first channel array row safely
    
    delta = np.mean(psd[(freqs >= 0.5) & (freqs <= 4.0)])
    theta = np.mean(psd[(freqs > 4.0) & (freqs <= 8.0)])
    alpha = np.mean(psd[(freqs > 8.0) & (freqs <= 13.0)])
    beta = np.mean(psd[(freqs > 13.0) & (freqs <= 30.0)])
    
    adr = alpha / (delta + 1e-6)
    
    cumulative_power = np.cumsum(psd)
    threshold = 0.95 * cumulative_power[-1]
    sef95_idx = np.where(cumulative_power >= threshold)[0]
    sef95 = float(freqs[sef95_idx[0]]) if len(sef95_idx) > 0 else 30.0
    
    return {
        "Delta": float(delta), 
        "Theta": float(theta), 
        "Alpha": float(alpha), 
        "Beta": float(beta), 
        "AD_Ratio": float(adr), 
        "SEF95": sef95, 
        "freqs": freqs.tolist(), 
        "psd": psd.tolist()
    }

