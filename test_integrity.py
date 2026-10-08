from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def test_profile_leakage():
    df=pd.read_csv(ROOT/"data/generated/synthetic_emg_windows.csv")
    assert df.groupby("profile_id").split.nunique().max()==1

def test_virtual_profile_count():
    p=pd.read_csv(ROOT/"data/generated/virtual_profiles.csv")
    assert len(p)==27
    assert (p.profile_type=="CP-inspired").sum()==20
    assert (p.profile_type=="TD-inspired").sum()==7

