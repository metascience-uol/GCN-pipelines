import numpy as np
import random

all_subjects_file = "/gss/work/zead9360/GCN-pipelines/multiverse/data/available_subjects.txt"
all_subjects = np.loadtxt(all_subjects_file).astype(int)
all_subjects = all_subjects.tolist()
output_file = "/gss/work/zead9360/GCN-pipelines/multiverse/data/subjects.txt"

# Randomly choose 100 subjects
selected_subjects = random.sample(all_subjects, min(100, len(all_subjects)))

# Save the selected subject IDs to a text file
with open(output_file, "w") as file:
    for subject in selected_subjects:
        file.write(f"{subject}\n")

print(f"Selected subset of subjects saved to {output_file}.")
