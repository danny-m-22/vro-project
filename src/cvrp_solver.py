import openrouteservice
import os
import pandas as pd
import numpy as np
from src.config import ORS_API_KEY

def load_duration_matrix():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_file = os.path.join(base_dir, "data", "durations.csv")
    df = pd.read_csv(input_file)
    df = df.drop(columns="Unnamed: 0")
    return df.replace(0, np.nan)

def load_coordinates_df():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_file = os.path.join(base_dir, "data", "coordinates.csv")
    df = pd.read_csv(input_file)

def save_best_path_df(output_df):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_file = os.path.join(base_dir, "data", "best_path.csv")
    output_df.to_csv(output_file, index=False)

def nn_solver(current_loc, input_df):
    begin_loc = current_loc
    visited_list = [current_loc]
    current_dist = 0
    matrix_df = input_df.copy()
    while len(visited_list) < len(input_df):
        matrix_df = matrix_df.drop(str(current_loc), axis=1)
        min_index = matrix_df.loc[int(current_loc)].idxmin()  # get location of min
        current_dist += matrix_df.loc[int(current_loc), str(min_index)]  # add min to current time
        # print(f"{matrix_df.loc[current_loc, str(min_index)]} from {current_loc} to {min_index}")
        current_loc = int(min_index)  # update current_loc
        visited_list.append(int(min_index))  # add new address
    current_dist += input_df.loc[current_loc, str(begin_loc)]  # get end to start value
    visited_list.append(begin_loc)
    return current_dist, visited_list


def nn_runner(duration_matrix, fixed_start=False, start_loc="0"):
    best_dist = 0
    best_list = []
    if not fixed_start:
        for loc in range(len(duration_matrix)):
            total_dist, path_list = nn_solver(loc, duration_matrix)
            # IF NEW BEST
            if total_dist < best_dist  or best_dist == 0:
              best_dist = total_dist
              best_list = list(path_list)

        else:
            total_dist, path_list = nn_solver(start_loc, duration_matrix)

    coordinates_df = load_coordinates_df()
    coordinates_df[['lon', 'lat']] = coordinates_df['Coordinates'].str.split(',', expand=True)
    coordinates_df = coordinates_df.drop('Coordinates', axis=1)
    coordinates_df['lon'], coordinates_df['lat'] = ((coordinates_df['lon'].str[1:]).str.strip(),
                                                    (coordinates_df['lat'].str[0:-1]).str.strip())
    coordinates_df['lon'], coordinates_df['lat'] = (coordinates_df['lon'].astype(float),
                                                    coordinates_df['lat'].astype(float))
    best_df = DataFrame(columns=['Address', 'lon', 'lat', 'dist'])
    for i in range(len(best_list)):
        coordinates_list.append([lat_list[i], lon_list[i]])


    return best_df


def two_opt(path_list, path_time):

    print("name")

def main():
    df = load_duration_matrix()
    best_path, best_cost = nn_runner(df)

    print(best_path, best_cost)


if __name__ == "__main__":
    main()