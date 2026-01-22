"""
vrp.py

Implements a vehicle routing problem (VRP) solver using a nearest neighbor heuristic
combined with 2-opt local search for route improvement. Uses driving duration data
to optimize the route visiting all locations with optional fixed start location.

Inputs:
    - Driving duration matrix CSV (data/durations.csv)
    - Coordinates CSV (from coordinates_standardizer) to map indices to locations

Outputs:
    - Best path saved as CSV (data/best_path.csv) with coordinates and travel times between stops
"""

import openrouteservice
import os
import pandas as pd
import numpy as np
from src.config import ORS_API_KEY
from utils.coordinates_standardizer import main as standard_coords


def load_duration_matrix():
    """
    Load the driving duration matrix CSV into a DataFrame.
    Replace zeros with NaN to avoid zero-duration errors in routing.

    Returns:
        pd.DataFrame: Duration matrix with index and columns as location indices
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_file = os.path.join(base_dir, "data", "durations.csv")
    df = pd.read_csv(input_file)
    df = df.drop(columns="Unnamed: 0")  # Drop auto-index column from CSV
    return df.replace(0, np.nan)


def save_best_path_df(output_df):
    """
    Save the best path DataFrame to CSV.

    Args:
        output_df (pd.DataFrame): DataFrame containing best route coordinates and times
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    output_file = os.path.join(base_dir, "data", "best_path.csv")
    output_df.to_csv(output_file, index=False)


def nn_solver(current_loc, duration_df):
    """
    Solve route using a nearest neighbor heuristic starting from current_loc.

    Args:
        current_loc (int): Starting location index
        duration_df (pd.DataFrame): Duration matrix

    Returns:
        tuple: (total_duration, path_list)
            - total_duration (float): Total travel time for route
            - path_list (list of int): Ordered list of location indices visited, starting and ending at start
    """
    begin_loc = current_loc
    path = [int(current_loc)]
    current_time = 0
    matrix_df = duration_df.copy()

    while len(path) < len(duration_df):
        # Remove current location column so we do not revisit
        matrix_df = matrix_df.drop(current_loc, axis=1)

        # Find nearest unvisited neighbor
        min_index = matrix_df.loc[current_loc].idxmin()

        # Add travel time to nearest neighbor
        current_time += matrix_df.loc[current_loc, min_index]

        # Update current location and append to path
        current_loc = min_index
        path.append(min_index)

    # Return to starting location
    current_time += duration_df.loc[current_loc, begin_loc]
    path.append(begin_loc)

    return current_time, path


def two_opt(best_list, duration_df):
    """
    Perform 2-opt heuristic to improve the given route by iteratively swapping edges
    to reduce total travel time.

    Args:
        best_list (list of int): Initial route as list of location indices
        duration_df (pd.DataFrame): Duration matrix

    Returns:
        tuple:
            - improved_path (list of int): Optimized route indices after 2-opt
            - transitions_list (list of float): Travel times between consecutive stops
    """
    current_path = best_list
    current_cost = sum(duration_df.loc[i, j] for i, j in zip(current_path[:-1], current_path[1:]))

    for i in range(0, len(current_path) - 2):
        for j in range(i + 1, len(current_path) - 1):
            # Create a new path by reversing a subsection between i+1 and j
            new_path = current_path[:i + 1] + current_path[i + 1:j + 1][::-1] + current_path[j + 1:]

            # Calculate new cost for this candidate path
            new_cost = sum(duration_df.loc[a, b] for a, b in zip(new_path[:-1], new_path[1:]))

            # If improvement, update current path and cost
            if new_cost < current_cost:
                current_path = new_path
                current_cost = new_cost

    # Calculate travel times between consecutive stops for final path
    transitions_list = [duration_df.loc[i, j] for i, j in zip(current_path[:-1], current_path[1:])]
    transitions_list.append(0)  # No travel time after last stop

    return current_path, transitions_list


def solver(duration_df, fixed_start=False, start_loc=0):
    """
    Solve the vehicle routing problem using nearest neighbor heuristic
    with optional fixed start location and 2-opt improvement.

    Args:
        duration_df (pd.DataFrame): Driving duration matrix
        fixed_start (bool): If True, route must start at start_loc
        start_loc (int): Starting location index if fixed_start is True

    Returns:
        pd.DataFrame: DataFrame with best route coordinates, travel times to next stop, and order
    """
    # Ensure indices are integers for consistent referencing
    duration_df.index = duration_df.index.astype(int)
    duration_df.columns = duration_df.columns.astype(int)

    best_total = 0
    best_path = []

    if not fixed_start:
        # Try all possible starting locations and choose the best route
        for location in range(len(duration_df)):
            total_time, path_list = nn_solver(location, duration_df)
            if total_time < best_total or best_total == 0:
                best_total = total_time
                best_path = path_list
    else:
        # Use fixed start location
        best_total, best_path = nn_solver(start_loc, duration_df)

    # Improve route with 2-opt local search
    updated_path, updated_times = two_opt(best_path, duration_df)

    # The solver might return a path like [1, 7, ..., 0, ..., 1].
    # Rotate it to ensure it starts and ends at index 0 while keeping the optimal order.

    if 0 in updated_path[:-1]:
        # 1. Get unique stops (remove the duplicate node at the end)
        unique_route = updated_path[:-1]

        # 2. Find where 0 is currently sitting
        zero_index = unique_route.index(0)

        # 3. Rotate the list: [Start...End] becomes [0...End] + [Start...0]
        rotated_route = unique_route[zero_index:] + unique_route[:zero_index]

        # 4. Close the loop by adding 0 to the end
        updated_path = rotated_route + [0]

        # 5. Recalculate travel times for the new sequence
        updated_times = [duration_df.loc[u, v] for u, v in zip(updated_path[:-1], updated_path[1:])]
        updated_times.append(0)


    # Load standardized coordinates
    coordinates_df = standard_coords()

    # Build DataFrame of best route with times and order columns
    best_df = pd.DataFrame(columns=coordinates_df.columns)
    for address_index in updated_path:
        row = coordinates_df.iloc[[address_index]]
        best_df = pd.concat([best_df, row], ignore_index=True)

    best_df.insert(3, "time_to_next", updated_times)
    best_df.insert(4, "order", updated_path)

    return best_df


def main():
    """
    Main entry point: loads duration matrix, solves VRP, prints results,
    and saves best path to CSV.
    """
    df = load_duration_matrix()
    results = solver(df)
    print(results)
    print("Total time:", int(results["time_to_next"].sum()))
    save_best_path_df(results)


if __name__ == "__main__":
    main()
