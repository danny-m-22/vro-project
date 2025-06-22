import openrouteservice
import os
import pandas as pd
from src.config import ORS_API_KEY

base_dir = os.path.dirname(os.path.dirname(__file__))
input_file = os.path.join(base_dir, "data", "durations.csv")
#output_file = os.path.join(base_dir, "data", "durations.csv")

duration_df = pd.read_csv(input_file)
duration_df = duration_df.drop(columns="Unnamed: 0")

# Path Characteristics
path_length = len(duration_df)

# BEST PATH
best_time = 0
best_start_node = 0
best_list = [0,1,2,3,4,5,6,7,8,9]

# CURRENT PATH VARIABLES
visited_list = []
not_visited_list = [0,1,2,3,4,5,6,7,8,9]
current_time = 0

print(duration_df)

for starting_loc in range(path_length):
    visited_list.append(starting_loc)
    not_visited_list.remove(starting_loc)

    # NN IMPLEMENTATION & TIME TRACKER
    while not_visited_list:
        min_index = duration_df[str(starting_loc)].idxmin(axis=0)  # get location of min
        print(min_index)
        current_time += min(duration_df.iloc[not_visited_list, starting_loc])  # add min to current time
        not_visited_list.remove(min_index)  # remove address from not visited
        visited_list.append(min_index)      # add new address

    current_time += duration_df.iloc[visited_list[0], visited_list[0]]  # get end to start value

    # IF NEW BEST
    if current_time < best_time  or best_time == 0:
      best_time = current_time
      best_list = list(visited_list)

    # RESET VARS
    current_time = 0
    visited_list.clear()
    not_visited_list = [0,1,2,3,4,5,6,7,8,9]

print(best_list)

   # i = 0
    # while i+1 < path_length:
    #   current_time += duration_df.iloc[visited_list[i], visited_list[i+1]]
    #   i+= 1
    # current_time += duration_df.iloc[visited_list[i], visited_list[0]]


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