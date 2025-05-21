import os
import time
from datetime import datetime
from matrix import SparseMatrix, InvalidMatrixFormat  # Local import since matrix.py is in the same folder

def get_base_dirs():
    """
    Calculate input and output directories based on this script's location.
    Assumes folder structure:
    /dsa/sparse_matrix/sample_inputs/
    /dsa/sparse_matrix/results/
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Path to this script
    base_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))  # Go up two levels to sparse_matrix/
    input_dir = os.path.join(base_dir, 'sample_inputs')
    output_dir = os.path.join(base_dir, 'results')
    return input_dir, output_dir

def list_files(input_dir):
    """
    List all .txt files in the input directory for the user to select.
    """
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"The directory {input_dir} does not exist.")
    
    print("📂 Available matrix files:")
    files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")
    return files

def generate_output_filename(output_dir, operation):
    """
    Generate a unique output filename based on the operation and current timestamp.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(output_dir, f"result_{operation}_{timestamp}.txt")

def display_or_save_result(matrix, filename, label, threshold=20):
    """
    Display the result in console if small; otherwise save to file.
    """
    non_zero_elements = sorted((key, val) for key, val in matrix.elements.items() if val != 0)
    
    if len(non_zero_elements) <= threshold:
        print(f"\n🧾 Result of {label} ({matrix.rows}x{matrix.cols}):")
        for (i, j), val in non_zero_elements:
            print(f"({i}, {j}, {val})")
    else:
        with open(filename, 'w') as f:
            f.write(f"Result of {label} ({matrix.rows}x{matrix.cols}):\n")
            for (i, j), val in non_zero_elements:
                f.write(f"({i}, {j}, {val})\n")
        print(f"\n📄 Result has {len(non_zero_elements)} entries, so it was saved to: {filename}")

def main():
    # Set up paths
    input_dir, output_dir = get_base_dirs()

    # Ensure output folder exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # List available matrix input files
    files = list_files(input_dir)

    # Ask user to choose matrix A
    print("\n📝 Select the first matrix file by number:")
    choice_a = int(input()) - 1
    A = SparseMatrix(filepath=os.path.join(input_dir, files[choice_a]))

    # Ask user to choose matrix B
    print("\n📝 Select the second matrix file by number:")
    choice_b = int(input()) - 1
    B = SparseMatrix(filepath=os.path.join(input_dir, files[choice_b]))

    # Ask user for operation type
    print("\n🔧 Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")

    operation = ""
    while operation not in ['1', '2', '3']:
        operation = input("Enter your choice (1, 2, or 3): ").strip()
        if operation not in ['1', '2', '3']:
            print("❌ Invalid operation selected. Please choose 1, 2, or 3.")

    try:
        print("\n⏳ Calculating...")
        start = time.time()

        # Perform the matrix operation
        if operation == '1':
            result = A.add(B)
            label = "Matrix A + Matrix B"
            output_filename = generate_output_filename(output_dir, 'add')
        elif operation == '2':
            result = A.subtract(B)
            label = "Matrix A - Matrix B"
            output_filename = generate_output_filename(output_dir, 'subtract')
        else:
            result = A.multiply(B)
            label = "Matrix A * Matrix B"
            output_filename = generate_output_filename(output_dir, 'multiply')

        duration = time.time() - start
        print(f"✅ Calculation done in {duration:.2f} seconds.")

        # Display or save result
        display_or_save_result(result, output_filename, label)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

