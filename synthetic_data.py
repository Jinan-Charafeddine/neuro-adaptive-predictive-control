from __future__ import annotations
import numpy as np
import pandas as pd

MUSCLES = ["biceps", "triceps", "ant_deltoid", "post_deltoid"]

def minimum_jerk(x):
    x = np.clip(x, 0.0, 1.0)
    return 10*x**3 - 15*x**4 + 6*x**5

def split_lookup(cfg):
    return {pid: name for name, ids in cfg["profile_split"].items() for pid in ids}

def generate_profiles(cfg):
    rng = np.random.default_rng(cfg["seed"])
    rows=[]
    for pid in range(1, cfg["n_profiles"]+1):
        cp = pid <= cfg["n_cp_profiles"]
        rows.append({
            "profile_id": pid,
            "profile_type": "CP-inspired" if cp else "TD-inspired",
            "simulated_age_years": float(np.clip(rng.normal(8.9,1.7),5,13)),
            "coactivation_gain": float(rng.normal(1.28 if cp else 0.82,0.08)),
            "fatigue_gain": float(rng.normal(1.18 if cp else 0.92,0.07)),
            "spasticity_gain": float(rng.normal(0.30 if cp else 0.06,0.04)),
            "split": split_lookup(cfg)[pid],
        })
    return pd.DataFrame(rows)

def _rms(x): return float(np.sqrt(np.mean(np.square(x))))

def generate_windows(cfg, profiles):
    rng=np.random.default_rng(cfg["seed"]+1)
    fs=cfg["emg_hz"]; duration=cfg["duration_s"]
    n=int(fs*duration); t=np.arange(n)/fs
    w=int(cfg["window_ms"]*fs/1000); hop=int(w*(1-cfg["window_overlap"]))
    rows=[]
    for p in profiles.to_dict("records"):
      for trial in range(1,cfg["n_trials_per_profile"]+1):
        load=float(cfg["external_load_kg"][(trial-1)%len(cfg["external_load_kg"])])
        phase=t/duration
        reach=minimum_jerk(np.minimum(phase/0.42,1))-minimum_jerk(np.clip((phase-0.58)/0.42,0,1))
        shoulder=10+55*reach; elbow=15+70*reach
        flex=np.clip(np.gradient(elbow),0,None); ext=np.clip(-np.gradient(elbow),0,None)
        flex=flex/(flex.max()+1e-9); ext=ext/(ext.max()+1e-9)
        base=0.08+0.035*load
        burst=np.zeros(n)
        if p["profile_type"]=="CP-inspired":
            for _ in range(3):
                c=rng.integers(w,n-w); width=rng.integers(20,70)
                burst += p["spasticity_gain"]*np.exp(-0.5*((np.arange(n)-c)/width)**2)
        noise=lambda scale: rng.normal(0,scale,n)
        b=np.clip(base+p["coactivation_gain"]*(0.62*flex+0.16*ext)+burst+noise(.035),0,1)
        tr=np.clip(base+p["coactivation_gain"]*(0.16*flex+0.62*ext)+burst+noise(.035),0,1)
        ad=np.clip(base+.48*reach+.08*load+0.5*burst+noise(.03),0,1)
        pd_=np.clip(base+.35*(1-reach)+.06*load+0.5*burst+noise(.03),0,1)
        fds=np.clip(.07+.18*reach+.15*load+noise(.025),0,1)
        signals={"biceps":b,"triceps":tr,"ant_deltoid":ad,"post_deltoid":pd_}
        for start in range(0,n-w+1,hop):
            stop=start+w; mid=(start+stop)//2; ph=phase[mid]
            intention="flexion" if ph<.42 else ("hold" if ph<.58 else "extension")
            row={"profile_id":p["profile_id"],"profile_type":p["profile_type"],"split":p["split"],
                 "trial":trial,"time_s":t[mid],"intention":intention,"load_kg":load,
                 "shoulder_deg":shoulder[mid],"elbow_deg":elbow[mid],"fds_proxy_rms":_rms(fds[start:stop])}
            row.update({f"{m}_rms":_rms(x[start:stop]) for m,x in signals.items()})
            rows.append(row)
    return pd.DataFrame(rows)

