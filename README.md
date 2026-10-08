# Neuro-Adaptive Predictive Control Reproducibility Package

This repository provides a transparent, simulation-only reference implementation for the manuscript **Neuro-Adaptive Predictive Control for Upper-Limb Rehabilitation Using EMG and Intention-Aware Assistance**.

## Scope and provenance

- No human-participant recordings or identifiable clinical data are included.
- The dataset contains 27 literature-informed **virtual profiles**: 20 CP-inspired and 7 typically developing-inspired profiles.
- EMG-like signals are synthetic. They must not be interpreted as measured pediatric EMG.
- The included lightweight simulator is a deterministic surrogate used for reproducibility and testing.
- `src/opensim_adapter.py` documents the interface for running the same controller with OpenSim 4.3 when an OpenSim model is available.
- The FDS-like channel is a simulated grasp-effort proxy, not a measured muscle channel.

## Repository structure

```text
config/                  Reproducible simulation settings
data/generated/          Generated CSV and Excel datasets
docs/                    Data dictionary and methods notes
results/figures/         Generated manuscript-style figures
results/tables/          Generated CSV and Excel result tables
scripts/                 Command-line entry points
src/                     Dataset, controller, models, metrics, and plotting code
tests/                   Lightweight integrity tests
```

## Quick start

```bash
python -m pip install -r requirements.txt
python scripts/run_all.py
```

The command regenerates the dataset, evaluates 20 randomized perturbation seeds, trains the reference learning modules, and exports CSV, Excel, PNG, PDF, and JSON outputs.

## Important interpretation

The exported performance values are outputs of this openly documented synthetic protocol. They are not clinical estimates, biological replicates, or evidence of effectiveness in children with cerebral palsy. Repeated seeds quantify numerical variability only.

## Data split

Profiles are split before windowing:

- Training: 19 profiles (14 CP-inspired, 5 TD-inspired)
- Validation: 4 profiles (3 CP-inspired, 1 TD-inspired)
- Test: 4 profiles (3 CP-inspired, 1 TD-inspired)

No profile appears in more than one subset. Preprocessing parameters are fitted on training data only.

## License

Code: MIT License. Generated synthetic data: CC BY 4.0.

