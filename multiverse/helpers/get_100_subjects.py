import os
import random
import numpy as np

datadir = "/mnt/hpc_daniel"
output_file = "/home/mibur/GCN-pipelines/multiverse/data/subjects.txt"

subject_dirs = [name for name in os.listdir(f"{datadir}/Data") if os.path.isdir(os.path.join(f"{datadir}/Data", name)) and name.isdigit()]
complete_subjects = []

for subject in subject_dirs:
    # Construct file paths
    dtseries_path = f"{datadir}/Data/{subject}/LR/rfMRI_REST1_LR_Atlas_MSMAll_hp2000_clean.dtseries.nii"
    confounds_movement_path = f"{datadir}/Regressors_all/{subject}/rfMRI_REST1_LR/Movement_Regressors.txt"
    confounds_csf_path = f"{datadir}/Regressors_all/{subject}/rfMRI_REST1_LR/rfMRI_REST1_LR_CSF.txt"
    confounds_wm_path = f"{datadir}/Regressors_all/{subject}/rfMRI_REST1_LR/rfMRI_REST1_LR_WM.txt"
    
    # List of file paths for validation
    file_paths = [dtseries_path, confounds_movement_path, confounds_csf_path, confounds_wm_path]
    
    # Check if all required files are present
    if all(os.path.exists(path) for path in file_paths):
        complete_subjects.append(subject)

print("Available subjects:", len(complete_subjects))

# Randomly choose 100 subjects
selected_subjects = random.sample(complete_subjects, min(100, len(complete_subjects)))

# Save the selected subject IDs to a text file
with open(output_file, "w") as file:
    for subject in selected_subjects:
        file.write(f"{subject}\n")

print(f"Selected subjects saved to {output_file}.")

