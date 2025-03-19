class Matrix:
    def __init__(self, array: list[list[int | float]]) -> None:
        """ Vytvoreni matice """
        if not array or not all(isinstance(row, list) for row in array):
            raise ValueError("Matrix Error: Matrix must be a list of lists.")
        if not all(len(row) == len(array[0]) for row in array):
            raise ValueError("Matrix Error: All rows must have the same length.")
        if not all(isinstance(item, (int, float)) for row in array for item in row):
            raise ValueError("Matrix Error: All elements must be int or float.")
        self.rows = len(array)
        self.cols = len(array[0])
        self.data = array

    @staticmethod
    def zero_matrix(height: int, width: int) -> "Matrix":
        """ Staticka metoda na vytvoreni nulove matice """
        if height <= 0 or width <= 0:
            raise ValueError("Matrix Error: Dimensions must be positive integers.")
        return Matrix([[0 for _ in range(width)] for _ in range(height)])

    @staticmethod
    def identity_matrix(side: int) -> "Matrix":
        """ Staticka metoda na vytvoreni jednotkove matice """
        if side <= 0:
            raise ValueError("Matrix Error: Side length must be a positive integer.")
        return Matrix([[1 if i == j else 0 for j in range(side)] for i in range(side)])

    def __str__(self) -> str:
        """ Pretizeni operatoru __str__ na prevod matice na string """
        return "\n".join([" ".join(map(str, row)) for row in self.data]) + "\n"

    def __getitem__(self, tup: tuple[int, int]) -> int | float:
        """ Pretizeni getitemu na vypsani prvku matice """
        row, col = tup
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError("Matrix Error: Index out of bounds.")
        return self.data[row][col]

    def __setitem__(self, tup: tuple[int, int], new_value: int | float) -> None:
        """ Pretizeni setitemu na nastaveni prvku matice """
        row, col = tup
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError("Matrix Error: Index out of bounds.")
        self.data[row][col] = new_value

    def transposition(self) -> "Matrix":
        """ Vrati novou matici, ktera je transpozici puvodni matice """
        transposed_data = [
            [self.data[j][i] for j in range(self.rows)] for i in range(self.cols)
        ]
        return Matrix(transposed_data)

    def get_info(
        self,
    ) -> tuple[tuple[int, int], bool, bool, bool, bool, bool]:
        """ Vypsani informaci o matici """
        is_square = self.rows == self.cols
        is_symmetric = is_square and all(
            self.data[i][j] == self.data[j][i]
            for i in range(self.rows)
            for j in range(i, self.cols)
        )
        is_antisymmetric = is_square and all(
            self.data[i][j] == -self.data[j][i]
            for i in range(self.rows)
            for j in range(i + 1, self.cols)
        )
        is_lower_triangular = all(
            self.data[i][j] == 0
            for i in range(self.rows)
            for j in range(i + 1, self.cols)
        )
        is_diagonal = (
            is_square
            and is_lower_triangular
            and all(self.data[i][i] != 0 for i in range(self.rows))
        )

        return (
            (self.rows, self.cols),
            is_square,
            is_symmetric,
            is_antisymmetric,
            is_lower_triangular,
            is_diagonal,
        )

    def __eq__(self, other_matrix: object) -> bool:
        """ Pretizeni operatoru ==; tzn jestli se dve matice rovnaji """
        if not isinstance(other_matrix, Matrix):
            return False

        if self.rows != other_matrix.rows or self.cols != other_matrix.cols:
            return False

        return all(
            self.data[i][j] == other_matrix.data[i][j]
            for i in range(self.rows)
            for j in range(self.cols)
        )

    # def __eq__(self, other_matrix: object) -> bool:
    #     """ Pretizeni operatoru ==; tzn jestli se dve matice rovnaji """
    #
    #     if not isinstance(other_matrix, Matrix):
    #         return False
    #     return self.data == other_matrix.data

    def __ne__(self, other_matrix: object) -> bool:
        """ Pretizeni operatoru !=; tzn jestli jsou dve matice rozdilne """
        return not self.__eq__(other_matrix)

    def __add__(self, other_matrix: "Matrix") -> "Matrix":
        """ Pretizeni operatoru + na scitani matic """
        if self.rows != other_matrix.rows or self.cols != other_matrix.cols:
            raise ValueError(
                "Matrix Error: Matrices must have the same dimensions for addition."
            )
        return Matrix(
            [
                [
                    self.data[i][j] + other_matrix.data[i][j]
                    for j in range(self.cols)
                ]
                for i in range(self.rows)
            ]
        )

    def __sub__(self, other_matrix: "Matrix") -> "Matrix":
        """ Pretizeni operatoru - na odecitani matic """
        if self.rows != other_matrix.rows or self.cols != other_matrix.cols:
            raise ValueError(
                "Matrix Error: Matrices must have the same dimensions for subtraction."
            )
        return Matrix(
            [
                [
                    self.data[i][j] - other_matrix.data[i][j]
                    for j in range(self.cols)
                ]
                for i in range(self.rows)
            ]
        )

    def __mul__(self, other_matrix: "Matrix") -> "Matrix":
        """ Pretizeni operatoru * na nasobeni matic """
        if self.cols != other_matrix.rows:
            raise ValueError(
                "Matrix Error: Matrices have incompatible dimensions for multiplication."
            )
        result_data = [
            [
                sum(
                    self.data[i][k] * other_matrix.data[k][j]
                    for k in range(self.cols)
                )
                for j in range(other_matrix.cols)
            ]
            for i in range(self.rows)
        ]
        return Matrix(result_data)

    def __rmul__(self, constant: int | float) -> "Matrix":
        """ Pretizeni operatoru * na nasobeni matice konstantou """
        return Matrix(
            [
                [constant * self.data[i][j] for j in range(self.cols)]
                for i in range(self.rows)
            ]
        )

    def determinant(self) -> int | float:
        """ Vrati determinant matice """
        if self.rows != self.cols:
            raise ValueError(
                "Matrix Error: Determinant is only defined for square matrices."
            )

        if self.rows == 1:
            return self.data[0][0]

        if self.rows == 2:
            return (
                self.data[0][0] * self.data[1][1]
                - self.data[0][1] * self.data[1][0]
            )

        det = 0
        for col in range(self.cols):
            submatrix = [
                [self.data[i][j] for j in range(self.cols) if j != col]
                for i in range(1, self.rows)
            ]
            cofactor = (
                (-1) ** col
                * self.data[0][col]
                * Matrix(submatrix).determinant()
            )
            det += cofactor

        return det

    def inverse(self) -> "Matrix":
        """ Vrati inverzni matici """
        if self.rows != self.cols:
            raise ValueError("Matrix Error: Inverse is only defined for square matrices.")

        # Create an identity matrix of the same size
        identity = Matrix.identity_matrix(self.rows)

        # Create a copy of the current matrix
        augmented = [row[:] + identity_row[:] for row, identity_row in zip(self.data, identity.data)]

        n = self.rows

        for i in range(n):
            # Find the pivot
            pivot = augmented[i][i]
            if abs(pivot) < 1e-10:
                for k in range(i + 1, n):
                    if abs(augmented[k][i]) > abs(pivot):
                        augmented[i], augmented[k] = augmented[k], augmented[i]
                        pivot = augmented[i][i]
                        break
            if abs(pivot) < 1e-10:
                raise ValueError("Matrix Error: Matrix is singular and cannot be inverted.")

            # Normalize the pivot row
            for j in range(2 * n):
                augmented[i][j] /= pivot

            # Eliminate column i for other rows
            for k in range(n):
                if k != i:
                    factor = augmented[k][i]
                    for j in range(2 * n):
                        augmented[k][j] -= factor * augmented[i][j]

        # Extract the inverse from the augmented matrix
        inverse_data = [row[n:] for row in augmented]
        return Matrix(inverse_data)

class Matrix3D:
    def __init__(self, array: list[list[list[int]]]) -> None:
        """ Vytvoreni matice 3D"""
        if (
            not array
            or not all(isinstance(matrix, list) for matrix in array)
            or not all(
                isinstance(row, list) for matrix in array for row in matrix
            )
        ):
            raise ValueError(
                "Matrix3D Error: Matrix must be a list of 2D matrices."
            )

        self.layers = len(array)
        self.rows = len(array[0])
        self.cols = len(array[0][0])

        if not all(len(matrix) == self.rows for matrix in array):
            raise ValueError(
                "Matrix3D Error: All layers must have the same number of rows."
            )

        for layer in array:
            if not all(len(row) == self.cols for row in layer):
                raise ValueError(
                    "Matrix3D Error: All rows in a layer must have the same number of columns."
                )

        if not all(
            isinstance(item, (int, float))
            for matrix in array
            for row in matrix
            for item in row
        ):
            raise ValueError(
                "Matrix3D Error: All elements must be int or float."
            )

        self.data = array

    def __eq__(self, other_matrix: object) -> bool:
        """ Pretizeni operatoru ==; tzn jestli se dve 3D matice rovnaji """
        if not isinstance(other_matrix, Matrix3D):
            return False

        return self.data == other_matrix.data

    def __ne__(self, other_matrix: object) -> bool:
        """ Pretizeni operatoru !=; tzn jestli jsou dve 3D matice rozdilne """
        return not self.__eq__(other_matrix)

    def determinant_3d(self) -> int:
        """ Vrati determinant 3D matice """
        if self.layers != self.rows or self.rows != self.cols:
            raise ValueError("Matrix3D Error: Determinant can only be computed for cubic matrices.")

        if self.layers == 1 and self.rows == 1 and self.cols == 1:
            return self.data[0][0][0]

        if self.layers == 2 and self.rows == 2 and self.cols == 2:
            return (
                self.data[0][0][0] * self.data[1][1][1]
                - self.data[1][1][0] * self.data[0][0][1]
                + self.data[0][1][1] * self.data[1][0][0]
                - self.data[0][1][0] * self.data[1][0][1]
            )

        determinant = 0
        for i in range(self.rows):
            for j in range(self.cols):
                sign = (-1) ** (i + j + 1)
                minor_data = [
                    [[self.data[layer][x][y] for y in range(self.cols) if y != j] for x in range(self.rows) if x != i]
                    for layer in range(1, self.layers)
                ]
                minor = Matrix3D(minor_data)
                sub_determinant = minor.determinant_3d()
                determinant += sign * self.data[0][i][j] * sub_determinant

        return determinant
