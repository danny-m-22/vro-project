"""
main.py

Orchestrates full VRO pipeline:
1. Solve VRP
2. Generate route visualization
"""

from src.vrp import main as solve_vrp
from src.visualizer import main as generate_map


def main():
    print("Running vehicle routing solver...")
    solve_vrp()

    print("Generating route map...")
    generate_map()

    print("Process completed.")


if __name__ == "__main__":
    main()
