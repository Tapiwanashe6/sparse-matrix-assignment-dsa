import os

# Custom exception to handle invalid matrix file format
class InvalidMatrixFormat(Exception):
    pass

class SparseMatrix:
    """
    Class to represent a sparse matrix.
    Sparse matrix stores only non-zero elements in a dictionary with keys as (row, col).
    """
    def __init__(self, filepath=None):
        self.rows = 0        # Number of rows in matrix
        self.cols = 0        # Number of columns in matrix
        self.elements = {}   # Dictionary to store non-zero elements as {(row, col): value}
        if filepath:
            self.load_from_file(filepath)

    def load_from_file(self, filepath):
        """
        Load matrix data from a file.
        Expected file format:
        rows=<number_of_rows>
        cols=<number_of_columns>
        (row, col, value)
        ...
        """
        print(f"Loading matrix from '{filepath}'...")
        with open(filepath, 'r') as file:
            # Read all non-empty lines and strip whitespace
            lines = [line.strip() for line in file if line.strip()]
            if len(lines) < 2:
                raise InvalidMatrixFormat("Input file has insufficient data.")
            
            # Parse number of rows and columns from first two lines
            self.rows = int(lines[0].split('=')[1])
            self.cols = int(lines[1].split('=')[1])
            
            # Parse each element line in the form (row, col, value)
            for line in lines[2:]:
                if not line.startswith("(") or not line.endswith(")"):
                    raise InvalidMatrixFormat("Input file has wrong format")
                line = line.strip('()')  # Remove parentheses
                row, col, val = map(int, line.split(','))
                self.elements[(row, col)] = val
        print("Loading complete.\n")

    def add(self, other):
        """
        Add two sparse matrices.
        Dimensions must be the same.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition.")
        result = SparseMatrix()
        result.rows = self.rows
        result.cols = self.cols
        # Copy elements of the first matrix
        result.elements = self.elements.copy()
        # Add elements of the second matrix
        for key, value in other.elements.items():
            result.elements[key] = result.elements.get(key, 0) + value
        return result

    def subtract(self, other):
        """
        Subtract one sparse matrix from another.
        Dimensions must be the same.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for subtraction.")
        result = SparseMatrix()
        result.rows = self.rows
        result.cols = self.cols
        # Copy elements of the first matrix
        result.elements = self.elements.copy()
        # Subtract elements of the second matrix
        for key, value in other.elements.items():
            result.elements[key] = result.elements.get(key, 0) - value
        return result

    def multiply(self, other):
        """
        Multiply two sparse matrices.
        Number of columns of first matrix must equal number of rows of second.
        """
        if self.cols != other.rows:
            raise ValueError("Matrix sizes do not allow multiplication.")
        
        result = SparseMatrix()
        result.rows = self.rows
        result.cols = other.cols

        # Create a map from rows in 'other' matrix to list of (col, value) pairs
        b_map = {}
        for (r, c), v in other.elements.items():
            if r not in b_map:
                b_map[r] = []
            b_map[r].append((c, v))

        # Perform multiplication by checking matching row-col pairs
        for (r1, c1), v1 in self.elements.items():
            if c1 in b_map:
                for c2, v2 in b_map[c1]:
                    current = result.get_element(r1, c2)
                    result.set_element(r1, c2, current + v1 * v2)

        return result

    def get_element(self, currRow, currCol):
        """Return value at (currRow, currCol). Return 0 if not set."""
        return self.elements.get((currRow, currCol), 0)

    def set_element(self, currRow, currCol, value):
        """
        Set the value at position (currRow, currCol).
        Remove the element from dictionary if value is zero.
        """
        if value != 0:
            self.elements[(currRow, currCol)] = value
        elif (currRow, currCol) in self.elements:
            del self.elements[(currRow, currCol)]

