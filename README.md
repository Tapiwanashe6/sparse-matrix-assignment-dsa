# 🧪 Sparse Matrix Operations

This project provides a tool for performing efficient operations (Addition, Subtraction, Multiplication) on sparse matrices. It includes a command-line interface that loads matrices from text files, executes operations, and displays or saves the result.

---

## 📁 Project Structure

```
/dsa/
└── sparse_matrix/
    ├── code/
    │   └── src/
    │       ├── main.py        # Main execution script
    │       └── matrix.py      # Contains SparseMatrix class
    ├── sample_inputs/         # Input .txt files with sparse matrices
    ├── sample_outputs/        # Result files for large matrix operations
    └── README.md              # Project documentation
```

---

## 🚀 Features

* Load and parse sparse matrix files
* Perform matrix:

  * Addition
  * Subtraction
  * Multiplication
* Display small results in the console
* Save large results to `sample_outputs/`
* Built-in error handling for invalid formats and operations

---

## 👄 Input Format

Each matrix file must follow this format:

```
<rows> <cols>
<row_index> <col_index> <value>
...
```

**Example:**

```
3 3
0 0 5
1 2 8
2 1 -3
```

---

## 📅 How to Run

### Requirements

* Python 3.x

### Steps

1. Navigate to the project directory:

```bash
cd dsa/sparse_matrix/code/src
```

2. Run the program:

```bash
python3 main.py
```

3. Follow the prompts to:

   * Select matrix files
   * Choose an operation (Add, Subtract, Multiply)
   * View or save the result

---

## ⚠️ Error Handling

The program handles:

* Missing input files or folders
* Unsupported or malformed file formats
* Mismatched matrix dimensions for the selected operation

---

## 👩‍💼 Author

Developed by Tapiwanashe Gift Marufu.

Contributions are welcome. Feel free to fork and improve the project.

---

## 📚 License

This project is licensed under the MIT License. See `LICENSE` for details.

