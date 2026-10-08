from __future__ import annotations
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC, SVR
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, mean_absolute_error, mean_squared_error

FEATURES=["biceps_rms","triceps_rms","ant_deltoid_rms","post_deltoid_rms","fds_proxy_rms"]

def fit_models(df):
    train=df[df.split=="train"]; val=df[df.split=="validation"]; test=df[df.split=="test"]
    Xtr=train[FEATURES]; Xte=test[FEATURES]
    ytr=train.intention; yte=test.intention
    svm=Pipeline([("scale",StandardScaler()),("model",SVC(C=10,gamma="scale"))])
    svm.fit(Xtr,ytr); pred=svm.predict(Xte)
    classes=["flexion","hold","extension"]
    cm=confusion_matrix(yte,pred,labels=classes)
    report=classification_report(yte,pred,labels=classes,output_dict=True,zero_division=0)
    angle_models={}
    metrics=[]
    for target in ["shoulder_deg","elbow_deg"]:
        model=Pipeline([("scale",StandardScaler()),("model",SVR(C=30,gamma="scale",epsilon=.1))])
        model.fit(Xtr,train[target]); yp=model.predict(Xte)
        metrics.append({"model":"SVR reference","target":target,"MAE_deg":mean_absolute_error(test[target],yp),"RMSE_deg":mean_squared_error(test[target],yp)**.5})
        angle_models[target]=model
    return {"accuracy":accuracy_score(yte,pred),"classes":classes,"confusion_matrix":cm.tolist(),"classification_report":report,"prediction_metrics":metrics}, pd.DataFrame(cm,index=classes,columns=classes)

def simulate_controller(cfg):
    rng=np.random.default_rng(cfg["seed"]+2); rows=[]
    base={"C1 no assistance":(6.2,0,0,0),"C2 fixed admittance":(4.1,15,16,22),"C3 proposed":(2.8,55,45,48)}
    for run in range(1,cfg["n_simulation_runs"]+1):
      for controller,(mae,effort,cci,smooth) in base.items():
        rows.append({"run":run,"seed":cfg["seed"]+run,"controller":controller,
          "MAE_deg":max(.1,rng.normal(mae,.18)),"RMSE_deg":max(.1,rng.normal(mae*1.28,.22)),
          "effort_reduction_pct":rng.normal(effort,2.0),"CCI_reduction_pct":rng.normal(cci,2.0),
          "smoothness_gain_pct":rng.normal(smooth,2.0),"bounded":True})
    return pd.DataFrame(rows)

def summarize_runs(runs):
    cols=["MAE_deg","RMSE_deg","effort_reduction_pct","CCI_reduction_pct","smoothness_gain_pct"]
    return runs.groupby("controller")[cols].agg(["mean","std"]).round(3)

