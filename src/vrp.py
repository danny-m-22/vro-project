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

def nn_solver(current_loc, duration_df):
    begin_loc = current_loc
    path = [int(current_loc)]
    current_time = 0
    matrix_df = duration_df.copy()
    while len(path) < len(duration_df):
        matrix_df = matrix_df.drop(current_loc, axis=1)
        min_index = matrix_df.loc[current_loc].idxmin()  # get location of min
        current_time += matrix_df.loc[current_loc, min_index]  # add min to current dist
        current_loc = min_index  # update current_loc
        path.append(min_index)  # add new address
    current_time += duration_df.loc[current_loc, begin_loc]  # get end to start value
    path.append(begin_loc)
    return current_time, path


def solver(duration_df, fixed_start=False, start_loc=0):
    duration_df.index = duration_df.index.astype(int)
    duration_df.columns = duration_df.columns.astype(int)
    best_total = 0
    best_path = []

    if not fixed_start:
        for location in range(len(duration_df)):
            total_time, path_list = nn_solver(location, duration_df)
            # IF NEW BEST
            if total_time < best_total  or best_total == 0:
              best_total = total_time
              best_path = path_list
        else:
            best_total, best_path = nn_solver(start_loc, duration_df)

    updated_path, updated_times = two_opt(best_path, duration_df)
    coordinates_df = standard_coords()
    best_df = pd.DataFrame(columns=coordinates_df.columns)

    for address_index in updated_path:
        row = coordinates_df.iloc[[address_index]]
        best_df = pd.concat([best_df, row], ignore_index=True)
    best_df.insert(3, "time_to_next", updated_times)
    best_df.insert(4, "order", updated_path)

    return best_df


def two_opt(best_list, duration_df):
    current_path = best_list
    current_cost = sum(duration_df.loc[i, j] for i, j in zip(current_path[:-1], current_path[1:]))
    transitions_list = []

    for i in range (1, len(current_path) - 2):
        for j in range(i + 1, len(current_path) - 1):
            new_path = current_path[:i + 1] + current_path[i + 1:j + 1][::-1] + current_path[j + 1:]
            new_cost = sum(duration_df.loc[i, j] for i, j in zip(new_path[:-1], new_path[1:]))
            if new_cost < current_cost:
                current_path = new_path
                current_cost = new_cost

    for i, j in zip(current_path, current_path[1:]):
        transitions_list.append(duration_df.loc[i, j])

    transitions_list.append(0)

    return current_path, transitions_list


def main():
    df = load_duration_matrix()
    results = solver(df)
    print(results)
    print(results['time_to_next'].sum())
    return results

if __name__ == "__main__":
    main()