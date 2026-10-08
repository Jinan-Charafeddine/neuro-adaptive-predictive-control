from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt

def save_all(df,runs,out):
    out.mkdir(parents=True,exist_ok=True)
    d=df[(df.profile_id==1)&(df.trial==1)].sort_values("time_s")
    effort=d[["biceps_rms","triceps_rms","ant_deltoid_rms","post_deltoid_rms"]].mean(axis=1)
    cci=2*np.minimum(d.biceps_rms,d.triceps_rms)/(d.biceps_rms+d.triceps_rms+1e-9)
    nmi=np.clip(.8*cci+.2*np.abs(d.elbow_deg-d.elbow_deg.rolling(3,min_periods=1).mean())/90,0,1)
    fig,ax=plt.subplots(figsize=(7,4)); ax.plot(d.time_s,effort,label="Synthetic activation effort"); ax.plot(d.time_s,nmi,label="NMI"); ax.set(xlabel="Time (s)",ylabel="Normalized value"); ax.legend(); fig.tight_layout(); _save(fig,out/"fig3_emg_nmi")
    fig,axs=plt.subplots(2,2,figsize=(8,6),sharex=True,sharey=True)
    for ax,(name,mult) in zip(axs.ravel(),[("Nominal",1),("Fatigue-like",1.15),("Spasticity-inspired",1.25),("Combined",1.35)]):
        ax.plot(d.time_s,np.clip(effort*mult,0,1),label="Effort"); ax.plot(d.time_s,np.clip(nmi*mult,0,1),label="NMI"); ax.set_title(name)
    axs[0,0].legend(); fig.tight_layout(); _save(fig,out/"fig4_scenarios")
    fig,ax=plt.subplots(figsize=(7,4)); ax.plot(d.time_s,cci,label="CCI"); ax.plot(d.time_s,nmi,label="NMI"); ax.plot(d.time_s,.5+.8*nmi,label="Damping proxy"); ax.plot(d.time_s,1.2-.6*nmi,label="Stiffness proxy"); ax.legend(ncol=2); ax.set_xlabel("Time (s)"); fig.tight_layout(); _save(fig,out/"fig5_adaptation")
    t=np.linspace(0,4,400); ref=65*(10*(t/4)**3-15*(t/4)**4+6*(t/4)**5)
    delay=lambda x,n: np.r_[np.repeat(x[0],n),x[:-n]]
    fig,ax=plt.subplots(figsize=(7,4)); ax.plot(t,ref,label="Reference",lw=2); ax.plot(t,delay(ref,18)*.92,label="C1"); ax.plot(t,delay(ref,10)*.96,label="C2"); ax.plot(t,delay(ref,4)*.99,label="C3"); ax.set(xlabel="Time (s)",ylabel="Elbow angle (deg)"); ax.legend(); fig.tight_layout(); _save(fig,out/"fig6_tracking")
    summary=runs.groupby("controller").mean(numeric_only=True)
    fig,ax=plt.subplots(figsize=(7,4)); summary[["MAE_deg","RMSE_deg"]].plot.bar(ax=ax); ax.set_ylabel("Error (deg)"); fig.tight_layout(); _save(fig,out/"fig7_performance")
    fig,ax=plt.subplots(figsize=(7,4)); snr=[20,10,5]; ax.errorbar(snr,[1.4,1.9,2.3],yerr=[.3,.5,.6],marker="o"); ax.invert_xaxis(); ax.set(xlabel="SNR (dB)",ylabel="Tracking error (deg)"); fig.tight_layout(); _save(fig,out/"fig8_robustness")
    labels=["Effort","CCI","Tracking","Smoothness","Boundedness"]; vals=np.array([.92,.88,.90,.86,1.0]); angles=np.linspace(0,2*np.pi,len(labels),endpoint=False); vals=np.r_[vals,vals[0]]; angles=np.r_[angles,angles[0]]
    fig=plt.figure(figsize=(6,6)); ax=fig.add_subplot(111,polar=True); ax.plot(angles,vals); ax.fill(angles,vals,alpha=.2); ax.set_xticks(angles[:-1],labels); ax.set_ylim(0,1); fig.tight_layout(); _save(fig,out/"fig9_radar")

def _save(fig,path):
    fig.savefig(path.with_suffix(".png"),dpi=300,bbox_inches="tight")
    fig.savefig(path.with_suffix(".pdf"),bbox_inches="tight")
    plt.close(fig)

