import os

class InvalidMatrixFormat(Exception):
    pass

class SparseMatrix:
    """
    Class to represent a sparse matrix.
    Sparse matrix stores only non-zero elements in a dictionary with keys as (row, col).
    """
    def __init__(self, filepath=None):
        self.rows = 0
        self.cols = 0
        self.elements = {}
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
            lines = [line.strip() for line in file if line.strip()]
            if len(lines) < 2:
                raise InvalidMatrixFormat("Input file has insufficient data.")

            # Parse rows
            if not lines[0].startswith("rows="):
                raise InvalidMatrixFormat("First line must specify rows=<number>.")
            try:
                self.rows = int(lines[0].split('=')[1])
            except ValueError:
                raise InvalidMatrixFormat("Rows value must be an integer.")

            # Parse cols
            if not lines[1].startswith("cols="):
                raise InvalidMatrixFormat("Second line must specify cols=<number>.")
            try:
                self.cols = int(lines[1].split('=')[1])
            except ValueError:
                raise InvalidMatrixFormat("Cols value must be an integer.")

            # Parse elements
            for line in lines[2:]:
                if not (line.startswith("(") and line.endswith(")")):
                    raise InvalidMatrixFormat(f"Invalid element line format: {line}")
                line = line.strip('()')
                parts = line.split(',')
                if len(parts) != 3:
                    raise InvalidMatrixFormat(f"Element line must have three values: {line}")
                try:
                    row, col, val = int(parts[0]), int(parts[1]), int(parts[2])
                except ValueError:
                    raise InvalidMatrixFormat(f"Element values must be integers: {line}")

                # Check indices are within bounds
                if not (0 <= row < self.rows) or not (0 <= col < self.cols):
                    raise InvalidMatrixFormat(f"Element position out of bounds: ({row}, {col})")

                self.elements[(row, col)] = val

        print("Loading complete.\n")

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition.")
        result = SparseMatrix()
        result.rows = self.rows
        result.cols = self.cols
        result.elements = self.elements.copy()
        for key, value in other.elements.items():
            result.elements[key] = result.elements.get(key, 0) + value
            if result.elements[key] == 0:
                del result.elements[key]
        return result

    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for subtraction.")
        result = SparseMatrix()
        result.rows = self.rows
        result.cols = self.cols
        result.elements = self.elements.copy()
        for key, value in other.elements.items():
            result.elements[key] = result.elements.get(key, 0) - value
            if result.elements[key] == 0:
                del result.elements[key]
        return result

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError("Matrix sizes do not allow multiplication.")
        result = SparseMatrix()
        result.rows = self.rows
        result.cols = other.cols

        b_map = {}
        for (r, c), v in other.elements.items():
            b_map.setdefault(r, []).append((c, v))

        for (r1, c1), v1 in self.elements.items():
            if c1 in b_map:
                for c2, v2 in b_map[c1]:
                    current = result.get_element(r1, c2)
                    new_val = current + v1 * v2
                    result.set_element(r1, c2, new_val)

        return result

    def get_element(self, currRow, currCol):
        return self.elements.get((currRow, currCol), 0)

    def set_element(self, currRow, currCol, value):
        if value != 0:
            self.elements[(currRow, currCol)] = value
        else:
            self.elements.pop((currRow, currCol), None)

