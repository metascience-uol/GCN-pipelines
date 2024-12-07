import os
import numpy as np
import nibabel as nib

datadir = "/gss/work/wowi8711/cifti_HCP"
output_file = "/gss/work/zead9360/GCN-pipelines/multiverse/data/available_subjects.txt"

subject_dirs = [
    name for name in os.listdir(f"{datadir}/Data") 
    if os.path.isdir(os.path.join(f"{datadir}/Data", name)) and name.isdigit()
]
complete_subjects = []

for i, subject in enumerate(subject_dirs):
    print(f"{i+1}/{len(subject_dirs)}")
    # Construct file paths
    dtseries_path = f"{datadir}/Data/{subject}/LR/rfMRI_REST1_LR_Atlas_MSMAll_hp2000_clean.dtseries.nii"
    confounds_movement_path = f"{datadir}/Regressors_all/{subject}/rfMRI_REST1_LR/Movement_Regressors.txt"
    confounds_csf_path = f"{datadir}/Regressors_all/{subject}/rfMRI_REST1_LR/rfMRI_REST1_LR_CSF.txt"
    confounds_wm_path = f"{datadir}/Regressors_all/{subject}/rfMRI_REST1_LR/rfMRI_REST1_LR_WM.txt"
    
    # List of file paths for validation
    file_paths = [dtseries_path, confounds_movement_path, confounds_csf_path, confounds_wm_path]
    
    # Check if all required files are present
    if not all(os.path.exists(path) for path in file_paths):
        print(f"Failed to find one of the files for subject {subject}.")
        continue
    
    # Check if dtseries.nii file can be loaded with nibabel
    try:
        nib.load(dtseries_path)
    except Exception as e:
        print(f"Failed to load NIfTI file for subject {subject}: {e}")
        continue
    
    # Check if the text files can be loaded as NumPy arrays with 1200 rows
    txt_files = [confounds_movement_path, confounds_csf_path, confounds_wm_path]
    valid_txt_files = True
    for txt_file in txt_files:
        try:
            data = np.loadtxt(txt_file)
            if data.shape[0] != 1200:
                print(f"File {txt_file} for subject {subject} does not have 1200 rows.")
                valid_txt_files = False
                break
        except Exception as e:
            print(f"Failed to load text file {txt_file} for subject {subject}: {e}")
            valid_txt_files = False
            break
    
    if not valid_txt_files:
        continue
    
    # If all checks pass, add subject to the list
    complete_subjects.append(subject)

print("Available subjects:", len(complete_subjects))

# Save the selected subject IDs to a text file
with open(output_file, "w") as file:
    for subject in complete_subjects:
        file.write(f"{subject}\n")