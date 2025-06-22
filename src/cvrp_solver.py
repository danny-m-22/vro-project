import openrouteservice
import os
import pandas as pd
import numpy as np
from src.config import ORS_API_KEY

base_dir = os.path.dirname(os.path.dirname(__file__))
input_file = os.path.join(base_dir, "data", "durations.csv")
#output_file = os.path.join(base_dir, "data", "durations.csv")

duration_df = pd.read_csv(input_file)
duration_df = duration_df.drop(columns="Unnamed: 0")
duration_df = duration_df.replace(0, np.nan)   # crucial for min calculations

# BEST PATH
best_dist = 0
best_list = []

# CURRENT PATH VARIABLES
visited_list = []


# NN SOLVER
    #START AT EACH ADDRESS AND FIND SHORTEST PATH; SAVE BEST PATH
    #REMEMBER: FROM-TO MATRIX; ROW TO COL

for loc in range(len(duration_df)):
    current_loc = loc
    duration_copy = duration_df.copy()
    visited_list.append(current_loc)
    current_dist = 0

    # NN IMPLEMENTATION & DISTANCE TRACKER
    while len(visited_list) < len(duration_df):

        duration_copy = duration_copy.drop(str(current_loc), axis=1)
        min_index = duration_copy.loc[int(current_loc)].idxmin()  # get location of min
        current_dist += duration_copy.loc[int(current_loc), str(min_index)]  # add min to current time
        #print(f"{duration_copy.loc[current_loc, str(min_index)]} from {current_loc} to {min_index}")
        current_loc = int(min_index)             # update current_loc
        visited_list.append(int(min_index))      # add new address

    current_dist += duration_df.iloc[current_loc, loc]  # get end to start value
    visited_list.append(loc)  # return to start (optional to include in list)

    # print(f"{duration_df.iloc[current_loc, loc]} from {current_loc} to {loc}")
    # print(f"total: {current_time}, order: {visited_list}")
    # print("\n\n")

    # IF NEW BEST
    if current_dist < best_dist  or best_dist == 0:
      best_dist = current_dist
      best_list = list(visited_list)

    # RESET VARS
    visited_list.clear()


# Attempt 2-opt (or k-opt) to smooth kinks
# NN + MNN


# 2 (k?) opt