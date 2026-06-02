# NeuroOS Signal Core: Quantitative EEG Analytics Platform
### Digital Time-Series Neurophysiology & ICU Neuro-Informatics Pipeline

##  Clinical & Scientific Overview
NeuroOS is an open-source, production-grade neuroinformatics dashboard designed for the interactive ingestion, visualization, and quantitative spectral analysis of multi-channel time-series digital electroencephalography (EEG) data. 

The platform addresses browser-level data latency and data privacy restrictions by programmatically synthesizing authentic human brainwave data via inverse Fast Fourier Transforms (IFFT), generating an accurate baseline cortical **Pink Noise ($1/f$ spectral distribution)**. Overlaid onto this physiological baseline are microvolt-calibrated pathological waveforms modeling critical neurophysiological states:
- **Normal Awake:** 10.2 Hz posterior dominant alpha rhythm with waxing/waning amplitude envelopes.
- **Generalized Absence Epilepsy:** Synchronous paroxysmal 3 Hz spike-and-wave discharges.
- **Non-Convulsive Status Epilepticus (NCSE):** Rhythmic ictal discharges demonstrating spatial-temporal frequency evolution (decelerating from 9 Hz to 3.5 Hz).
- **Profound Encephalopathy / Coma:** Generalized high-voltage polymorphic delta slowing with background suppression.

*   **Live Application URL:** https://elite-eeg-analytics-cyqv6sw4pq7mfhzueaaeay.streamlit.app/
*   **Source Code Matrix:** https://github.com/noorfatimacheema249-design/elite-eeg-analytics

##  Technical Architecture & Core Libraries
- **Signal Processing Kernel:** `mne-python` (Industry-standard core library for human neurophysiological data science)
- **Time-Series Matrix Calculus:** `SciPy (Signal)` & `NumPy (FFT)`
- **Dynamic Frontend Architecture:** `Streamlit Framework` (Reactive state configuration)
- **Data Visualization Layer:** `Plotly Graphic Objects (go)` (Continuous stacking oscilloscope array)

##  Core Engineering Modules & ICU Biomarkers
1. **8-Channel Digital Montage Stack:** Simulates standard clinical EEG monitor readouts by looping through electrode channel rows (`Fp1-F3`, `F3-C3`, `C3-P3`, `P3-O1`, etc.) and applying a vertical calibration offset (`offset -= 130`) to render a unified microvolt ($\mu V$) grid canvas.
2. **Quantitative Spectral Power Density Mapping:** Integrates MNE-Core logic to run Welch periodograms (`mne.time_frequency.psd_array_welch`), isolating absolute electrical power within canonical medical wavebands (Delta, Theta, Alpha, Beta).
3. **Advanced Neuro-ICU Telemetry Tracking:** 
   - **SEF95 (Spectral Edge Frequency 95):** Computes the exact frequency boundary below which 95% of total spectral power resides using cumulative array sums, serving as a critical monitor for cerebral metabolic drops.
   - **ADR (Alpha-to-Delta Ratio):** Calculates real-time mathematical ratios to flag subclinical delayed cerebral ischemia (DCI).
4. **Automated Artifact Rejection Monitor:** Evaluates peak-to-peak voltage amplitudes. Signals transcending un-physiological thresholds ($>110\mu V$) are automatically tagged as "Saturated Vector Artifacts" to log transient data distortions.

##  Software Verification & Reproducibility
All algorithmic operations utilize validated mathematical models running on an open-source MNE wrapper layer. The tool serves as an interactive clinical informatics proof-of-concept for automated neurophysiological monitoring systems and institutional portfolio review during the 2027 Residency Match cycle.

##  Open-Source Licensing
This project is deployed under the **MIT License**—permitting free open-source reuse while enforcing standard institutional liability protection.
