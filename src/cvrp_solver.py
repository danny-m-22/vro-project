import openrouteservice
import os
import pandas as pd
from src.config import ORS_API_KEY

base_dir = os.path.dirname(os.path.dirname(__file__))
input_file = os.path.join(base_dir, "data", "durations.csv")
#output_file = os.path.join(base_dir, "data", "durations.csv")

duration_df = pd.read_csv(input_file)
duration_df = duration_df.rename(columns={"Unnamed: 0": "Location"})



n = len(duration_df)
i = list(range(0, n))  # address that is being left
j = list(range(0, n))  # address that is being entered
col_names = duration_df.columns.to_list()
x_ij_matrix = (pd.DataFrame(index=list(range(0, n)), columns=col_names)).drop("Location", axis=1)
print(x_ij_matrix)

# PLAN:
# Nearest neighbor approach (NN)
# Start at 0
# Go to next CLOSEST node
# Get back to 0
# Iterate: start at another node (MNN)
# overwrite results if newest tour is better
# Attempt 2-opt (or k-opt) to smooth kinks

# NN + MNN


# 2 (k?) opt