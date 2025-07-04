import openrouteservice
import os
import pandas as pd
import numpy as np
from src.config import ORS_API_KEY
from utils.coordinates_standardizer import main as standard_coords

def load_duration_matrix():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_file = os.path.join(base_dir, "data", "durations.csv")
    df = pd.read_csv(input_file)
    df = df.drop(columns="Unnamed: 0")
    return df.replace(0, np.nan)

def save_best_path_df(output_df):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_file = os.path.join(base_dir, "data", "best_path.csv")
    output_df.to_csv(output_file, index=False)

def nn_solver(current_loc, input_df):
    begin_loc = current_loc
    visited_list = [current_loc]
    dist_list = []
    current_dist = 0
    matrix_df = input_df.copy()
    while len(visited_list) < len(input_df):
        matrix_df = matrix_df.drop(str(current_loc), axis=1)
        min_index = matrix_df.loc[int(current_loc)].idxmin()  # get location of min
        current_dist += matrix_df.loc[int(current_loc), str(min_index)]  # add min to current dist
        dist_list.append(matrix_df.loc[int(current_loc), str(min_index)]) # keep track of transitions
        # print(f"{matrix_df.loc[current_loc, str(min_index)]} from {current_loc} to {min_index}")
        current_loc = int(min_index)  # update current_loc
        visited_list.append(int(min_index))  # add new address
    current_dist += input_df.loc[current_loc, str(begin_loc)]  # get end to start value
    visited_list.append(begin_loc)
    dist_list.append(input_df.loc[current_loc, str(begin_loc)])
    dist_list.append(0)
    return current_dist, visited_list, dist_list


def nn_runner(duration_matrix, fixed_start=False, start_loc="0"):
    best_dist = 0
    best_list = []
    best_transitions = []
    if not fixed_start:
        for loc in range(len(duration_matrix)):
            total_dist, path_list, distance_list = nn_solver(loc, duration_matrix)
            # IF NEW BEST
            if total_dist < best_dist  or best_dist == 0:
              best_dist = total_dist
              best_list = path_list
              best_transitions = distance_list
        else:
            total_dist, path_list, distance_list = nn_solver(start_loc, duration_matrix)
            best_dist = total_dist
            best_list = path_list
            best_transitions = distance_list

    coordinates_df = standard_coords()
    best_df = pd.DataFrame(columns=coordinates_df.columns)
    for address_index in best_list:
        row = coordinates_df.iloc[[address_index]]
        best_df = pd.concat([best_df, row], ignore_index=True)
    best_df.insert(3, "dist_to_next", best_transitions)
    return best_df


def two_opt(path_list, path_time):

    print("temporary")

def main():
    df = load_duration_matrix()
    results = nn_runner(df)

    print(results)


if __name__ == "__main__":
    main()