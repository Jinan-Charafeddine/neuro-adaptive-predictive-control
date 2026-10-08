# Data dictionary

Each row in `synthetic_emg_windows.csv` is one 200 ms window with 50% overlap.

| Field | Description |
|---|---|
| `profile_id` | Virtual profile identifier; not a participant identifier |
| `profile_type` | `CP-inspired` or `TD-inspired` |
| `split` | Train, validation, or test assignment made before windowing |
| `trial` | Simulated repetition index |
| `time_s` | Window-center time |
| `intention` | Flexion, hold, or extension |
| `load_kg` | Known simulated external load |
| `*_rms` | RMS of the synthetic EMG-like channel |
| `shoulder_deg`, `elbow_deg` | Simulated joint-angle references |
| `fds_proxy_rms` | Synthetic grasp-effort proxy; not measured FDS EMG |

The workbook `synthetic_emg_dataset.xlsx` contains data, profile metadata, split assignments, and generation parameters.

