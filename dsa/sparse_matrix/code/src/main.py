import os
import time
from datetime import datetime
from matrix import SparseMatrix, InvalidMatrixFormat

def get_base_dirs():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))
    input_dir = os.path.join(base_dir, 'sample_inputs')
    output_dir = os.path.join(base_dir, 'sample_outputs')
    return input_dir, output_dir

def list_files(input_dir):
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"The directory {input_dir} does not exist.")
    
    files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    if not files:
        raise FileNotFoundError("No .txt files found in the input directory.")
    print("📂 Available matrix files:")
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")
    return files

def get_user_choice(prompt, valid_range):
    while True:
        choice = input(prompt).strip()
        if not choice.isdigit():
            print("❌ Please enter a valid number.")
            continue
        idx = int(choice)
        if idx not in valid_range:
            print(f"❌ Choice must be between {valid_range.start} and {valid_range.stop - 1}.")
            continue
        return idx - 1

def generate_output_filename(output_dir, operation):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(output_dir, f"result_{operation}_{timestamp}.txt")

def display_or_save_result(matrix, filename, label):
    non_zero_elements = sorted((key, val) for key, val in matrix.elements.items() if val != 0)
    if len(non_zero_elements) == 0:
        print(f"\n🧾 Result of {label} is an empty matrix (all zeros).")
        return
    
    # For small matrix, print on console
    if matrix.rows <= 20 and matrix.cols <= 20:
        print(f"\n🧾 Result of {label} ({matrix.rows}x{matrix.cols}):")
        for (i, j), val in non_zero_elements:
            print(f"({i}, {j}, {val})")
    else:
        # For large matrix, save to file
        with open(filename, 'w') as f:
            f.write(f"Result of {label} ({matrix.rows}x{matrix.cols}):\n")
            for (i, j), val in non_zero_elements:
                f.write(f"({i}, {j}, {val})\n")
        print(f"\n📄 Result saved to: {filename}")

def main():
    try:
        input_dir, output_dir = get_base_dirs()
        os.makedirs(output_dir, exist_ok=True)

        files = list_files(input_dir)

        print("\n📝 Select the first matrix file by number:")
        choice_a = get_user_choice("Enter choice: ", range(1, len(files)+1))
        A = SparseMatrix(filepath=os.path.join(input_dir, files[choice_a]))

        print("\n📝 Select the second matrix file by number:")
        choice_b = get_user_choice("Enter choice: ", range(1, len(files)+1))
        B = SparseMatrix(filepath=os.path.join(input_dir, files[choice_b]))

        print("\n🔧 Select operation:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")

        operation = get_user_choice("Enter your choice (1, 2, or 3): ", range(1, 4))

        print("\n⏳ Calculating...")
        start = time.time()

        if operation == 0:
            result = A.add(B)
            label = "Matrix A + Matrix B"
            output_filename = generate_output_filename(output_dir, 'add')
        elif operation == 1:
            result = A.subtract(B)
            label = "Matrix A - Matrix B"
            output_filename = generate_output_filename(output_dir, 'subtract')
        else:
            result = A.multiply(B)
            label = "Matrix A * Matrix B"
            output_filename = generate_output_filename(output_dir, 'multiply')

        duration = time.time() - start
        print(f"✅ Calculation done in {duration:.2f} seconds.")

        display_or_save_result(result, output_filename, label)

    except InvalidMatrixFormat as imf:
        print(f"❌ Invalid matrix file format: {imf}")
    except FileNotFoundError as fnf:
        print(f"❌ File error: {fnf}")
    except ValueError as ve:
        print(f"❌ Value error: {ve}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()

