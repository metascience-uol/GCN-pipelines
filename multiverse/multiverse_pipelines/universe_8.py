# Ordering information was provided. The ordered decisions for this universe are:
forking_paths = {'preprocessing': 'hcp_minimal', 'parcellation': 'schaefer_400', 'confounds': 'combined', 'filtering': False, 'graph_measure': 'global_efficiency'}

import os
import pandas as pd
import numpy as np
import nibabel as nib
from matplotlib import pyplot as plt
from comet import cifti, graph, connectivity, utils
from nilearn import signal

datadir = "/gss/work/wowi8711/cifti_HCP" # IMPORTANT: This needs to be the path to the HCP data on your system
subjects_list = "/gss/work/zead9360/GCN-pipelines/multiverse/data/subjects_old_14.txt" # IMPORTANT: This needs to be the path to a list of subject IDs
    
subjects = np.loadtxt(subjects_list).astype(int)
global_eff = {}

for i, subject in enumerate(subjects):
    # Get fmri data
    dtseries = f"{datadir}/Data/{subject}/LR/rfMRI_REST1_LR_Atlas_MSMAll_hp2000_clean.dtseries.nii"
    ts = nib.load(dtseries).get_fdata() 
    
    # Get confounds
    confounds_movement = pd.read_csv(f"{datadir}/Regressors_all/{subject}/rfMRI_REST1_LR/Movement_Regressors.txt", sep="\s+", header=None)
    confounds_csf = pd.read_csv(f"{datadir}/Regressors_all/{subject}/rfMRI_REST1_LR/rfMRI_REST1_LR_CSF.txt", sep="\s+", header=None)
    confounds_wm = pd.read_csv(f"{datadir}/Regressors_all/{subject}/rfMRI_REST1_LR/rfMRI_REST1_LR_WM.txt", sep="\s+", header=None)
    
    # Create confounds data frame
    if forking_paths.get("confounds"):
        if forking_paths["confounds"] == "motion_wm_csf":
            confounds_df = pd.concat([confounds_movement, confounds_csf, confounds_wm], axis=1)
        elif forking_paths["confounds"] == "gsr":
            confounds_df = pd.DataFrame()
            confounds_df["global_signal"] = np.mean(ts, axis=1)
        elif forking_paths["confounds"] == "combined":
            confounds_df = pd.concat([confounds_movement, confounds_csf, confounds_wm], axis=1)
            confounds_df["global_signal"] = np.mean(ts, axis=1)
        elif forking_paths["confounds"] == "none":
            confounds_df = None
        else:
            raise ValueError("Invalid confounds provided")
    
    # Create filtering variables
    if forking_paths.get("filtering"):
        high_pass = 0.01
        low_pass = 0.1
    else:
        high_pass = None
        low_pass = None

    # Actual pipeline:
    # The pipeline is ordered according to the the forking_paths dictionary,
    # so this will account for the switch in order between confounds regression and parcellation
    for key in forking_paths:
        if key == "parcellation":
            ts = cifti.parcellate(ts, atlas="schaefer_400_cortical")
        if key == "confounds":
            ts = signal.clean(ts, detrend=True, standardize="zscore_sample", confounds=confounds_df, standardize_confounds="zscore_sample", t_r=0.72, low_pass=low_pass, high_pass=high_pass)
    
    # Graph construction
    fc = connectivity.Static_Pearson(ts).estimate()
    fc = graph.handle_negative_weights(fc, type="discard") 
    fc = graph.threshold(fc, type="density", density=0.5)
    
    # Global efficiency estimation
    global_eff[str(subject)] = graph.efficiency(fc, local=False)
    print(f"Subject {i+1}/100 done. Global efficiency: {global_eff[str(subject)]}")
    
utils.save_universe_results(global_eff, universe=os.path.abspath(__file__))