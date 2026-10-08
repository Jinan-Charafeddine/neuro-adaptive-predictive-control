from pathlib import Path
import sys, json, yaml
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.synthetic_data import generate_profiles, generate_windows
from src.analysis import fit_models, simulate_controller, summarize_runs
from src.figures import save_all

def main():
    cfg=yaml.safe_load((ROOT/"config/default.yaml").read_text())
    profiles=generate_profiles(cfg); windows=generate_windows(cfg,profiles)
    data_dir=ROOT/"data/generated"; table_dir=ROOT/"results/tables"; fig_dir=ROOT/"results/figures"
    for p in [data_dir,table_dir,fig_dir]: p.mkdir(parents=True,exist_ok=True)
    windows.to_csv(data_dir/"synthetic_emg_windows.csv",index=False)
    profiles.to_csv(data_dir/"virtual_profiles.csv",index=False)
    with pd.ExcelWriter(data_dir/"synthetic_emg_dataset.xlsx",engine="openpyxl") as xw:
        windows.to_excel(xw,sheet_name="windows",index=False); profiles.to_excel(xw,sheet_name="profiles",index=False)
        pd.DataFrame([{"parameter":k,"value":str(v)} for k,v in cfg.items()]).to_excel(xw,sheet_name="parameters",index=False)
    model_results,cm=fit_models(windows); runs=simulate_controller(cfg); summary=summarize_runs(runs)
    runs.to_csv(table_dir/"simulation_runs.csv",index=False); cm.to_csv(table_dir/"intention_confusion_matrix.csv")
    pd.DataFrame(model_results["prediction_metrics"]).to_csv(table_dir/"prediction_metrics.csv",index=False)
    summary.to_csv(table_dir/"controller_summary.csv")
    with pd.ExcelWriter(table_dir/"all_results.xlsx",engine="openpyxl") as xw:
        runs.to_excel(xw,sheet_name="simulation_runs",index=False); summary.to_excel(xw,sheet_name="controller_summary")
        cm.to_excel(xw,sheet_name="confusion_matrix"); pd.DataFrame(model_results["prediction_metrics"]).to_excel(xw,sheet_name="prediction_metrics",index=False)
    (table_dir/"model_results.json").write_text(json.dumps(model_results,indent=2))
    save_all(windows,runs,fig_dir)
    print(f"Generated {len(windows):,} windows from {len(profiles)} virtual profiles")
    print(f"Reference SVM test accuracy: {model_results['accuracy']:.3f}")

if __name__=="__main__": main()

