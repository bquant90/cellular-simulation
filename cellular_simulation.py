# This program simulates cellular life using matrices.
# Time Complexity: O(rows * cols), where rows is the number of rows and cols is the number of columns.
# Space Complexity: O(rows * cols) as well.
import random
import os
from typing import List

# Constants for program configuration
MIN_DIMENSION = 3
MAX_DIMENSION = 20
MIN_TIME_STEP = 1
MAX_TIME_STEP = 99

# Cell states
ALIVE = 'O'
DEAD = '.'

def main() -> None:
    """Main function to run the cellular simulation program."""
    print("Cellular Life Simulation")
    print("-------------------------")
    print("This program simulates cellular life using matrices.")
    print(f"The final matrix will be saved to \"final_time_step.txt\" in your current directory.")

    while (True):
        # Get simulation parameters from the user
        print() # Extra initial spacing
        rows = get_dimension("rows") 
        cols = get_dimension("columns")
        seed = get_seed_value() 
        iterations = get_iterations()

        # Generate and display the initial matrix
        matrix = generate_matrix(rows, cols, seed)
        print()
        print("Initial Matrix (Time Step 1):")
        display_matrix(matrix)

        # Run the simulation for the specified number of iterations
        for i in range(iterations):
            matrix = step_matrix(matrix)
            print()
            print(f"Matrix at Time Step {i + 2}:") 
            display_matrix(matrix)

        # Write the final matrix to a file
        write_final_time_step(matrix, iterations)
        print()
        print("Simulation complete! The final matrix has been saved to \"final_time_step.txt\".")

        # Ask if the user wants to run another simulation
        if not prompt_to_continue():
                print("Thank you for using the Cellular Life Simulation program. Goodbye!")
                break

def get_dimension(dimension_name: str) -> int:
    """
    Get a valid dimension (rows or columns) from the user.

    Args:
        dimension_name (str): The name of the dimension (rows or columns)

    Returns:
        int: A valid dimension between MIN_DIMENSION and MAX_DIMENSION
    """
    while True:
        try:
            value = input(f"Enter the number of {dimension_name} for the simulation matrix ({MIN_DIMENSION} - {MAX_DIMENSION}): ")
            dimension = int(value)

            if MIN_DIMENSION <= dimension <= MAX_DIMENSION:
                return dimension
            else:
                print(f"Error: Number of {dimension_name} must be between {MIN_DIMENSION} and {MAX_DIMENSION}.")
        except ValueError:
            print("Error: Please enter a valid integer.")


def get_seed_value() -> int:
    """
    Get a seed value for random matrix generation.

    Returns:
        int: The seed value (user-provided or random)
    """
    while True:
        seed_input = input("Enter the seed value (integer) for matrix generation or press enter for a random seed: ")

        if seed_input == "":
            # Generate a random seed
            seed = random.randint(1, 100000000)
            print(f"Using random seed: {seed}")
            return seed

        try:
            return int(seed_input)
        except ValueError:
            print("Error: Please enter a valid integer or press Enter for a random seed.")
        

def get_iterations() -> int:
    """
    Get the number of time steps to simulate.

    Returns:
        int: A valid number of iterations between MIN_TIME_STEP and MAX_TIME_STEP
    """
    while True:
        try:
            value = input(f"Enter the number of time steps to simulate ({MIN_TIME_STEP} - {MAX_TIME_STEP}): ")
            iterations = int(value)

            if MIN_TIME_STEP <= iterations <= MAX_TIME_STEP:
                return iterations
            else:
                print(f"Error: Number of time steps must be between {MIN_TIME_STEP} and {MAX_TIME_STEP}.")
        except ValueError:
            print("Error: Please enter a valid integer.")

def generate_matrix(rows: int, cols: int, seed: int) -> List[List[str]]:
    """
    Generate a random matrix with cells that are either alive or dead.

    Args:
        rows (int): Number of rows in the matrix
        cols (int): Number of columns in the matrix
        seed (int): Random seed for reproducibility

    Returns:
        List[List[str]]: A matrix with randomly assigned cell states
    """
    random.seed(seed)
    matrix = []
    return [[ALIVE if random.randint(0, 1) == 1 else DEAD for _ in range(cols)] for _ in range (rows)]

def display_matrix(matrix: List[List[str]]) -> None:
    """
    Display the matrix to the console.

    Args:
        matrix (List[List[str]]): The matrix to display
    """
    for row in matrix:
        print("".join(row))

def step_matrix(matrix: List[List[str]]) -> List[List[str]]:
    """
    Create a new matrix based on the current matrix according to simulation rules.

    Args:
        matrix (List[List[str]]): The current matrix

    Returns:
        List[List[str]]: The new matrix after applying simulation rules
    """
    rows = len(matrix)
    cols = len(matrix[0])
    new_matrix = [[DEAD for _ in range(cols)] for _ in range(rows)]
    
    # Modify the newly-created matrix's cells based on the previous matrix
    for row in range(rows):
        for col in range(cols):
            new_matrix[row][col] = determine_cell_state(matrix, row, col)
    
    return new_matrix

def determine_cell_state(matrix: List[List[str]], row: int, col: int) -> str:
    """
    Determine the state of a cell in the next time step based on simulation rules

    Simulation Rules:
    1. Any position in the matrix with a period '.' is considered "dead" during the current time step.
    2. Any position in the matrix with a capital 'O' is considered "alive" during the current time step.
    3. If an "alive" cell has exactly 2, 3, or 4 living neighbors, it continues to be "alive".
    4. If a "dead" cell has an even number greater than 0 living neighbors, it becomes "alive".
    5. Every other cell dies or remains dead.

    Args:
        matrix (List[List[str]]): The current matrix
        row (int): Row index of the cell
        col (int): Column index of the cell

    Returns:
        str: The state of the cell in the next time step (ALIVE or DEAD)
    """
    alive_neighbors = count_alive_neighbors(matrix, row, col)

    if matrix[row][col] == ALIVE:
        # Rule 3. If alive and has 2, 3, or 4 alive neighbors, stays alive
        return ALIVE if alive_neighbors in [2, 3, 4] else DEAD
    else:
        # Rule 4. If dead and has an even number of alive neighbors > 0, becomes alive
        return ALIVE if alive_neighbors > 0 and alive_neighbors % 2 == 0 else DEAD

def count_alive_neighbors(matrix: List[List[str]], row: int, col: int) -> int:
    """
    Count the number of alive neighbors around a cell.

    Args:
        matrix (List[List[str]]): The matrix
        row (int): Row index of the cell
        col (int): Column index of the cell

    Returns:
        int: THe number of alive neighbors
    """
    rows = len(matrix)
    cols = len(matrix[0])
    alive_count = 0

    # Check all 8 neighboring cells
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            # Skip the cell itself
            if r == row and c == col:
                continue

            # Use modulo to wrap around the edges of the matrix
            wrapped_r = r % rows
            wrapped_c = c % cols

            if matrix[wrapped_r][wrapped_c] == ALIVE:
                alive_count += 1

    return alive_count

def write_final_time_step(matrix: List[List[str]], iterations: int) -> None:
    """
    Write the final matrix to a file.

    Args:
        matrix[List[List[str]]): The final matrix
        iterations (int): The number of time steps simulated
    """
    try:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(current_directory, "final_time_step.txt")
                                            
        with open(file_name, 'w') as file:
            # Write header information
            time_step_text = "time step" if iterations == 1 else "time steps"
            file.write("Cellular Life Simulation Results")
            file.write("\n")
            file.write("-" * 50)
            file.write("\n")                          
            file.write(f"You ran {iterations} {time_step_text}.")
            file.write("\n\n") 
            file.write("Final matrix:")
            file.write("\n")

            # Write the matrix
            for row in matrix:
                file.write(''.join(row) + '\n')

        return True
    except Exception as e:
        print(f"Error writing to file: {e}")
        return False

def prompt_to_continue() -> bool:
    """
    Ask the user if they want to run another simulation.
    
    Returns:
        bool: True if the user wants to continue, False otherwise
    """
    while True:
        again = input("Run another simulation (Y/N)?: ").upper()
        if again == 'Y':
            return True
        elif again == 'N':
            return False
        else:
            print("Not a valid answer. Please enter Y or N.")
    
if __name__ == "__main__":
    main()


        
    




