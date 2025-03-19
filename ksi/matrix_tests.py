from assignment import Matrix, Matrix3D


a = Matrix3D([[[1, 2, 3]]])
print(Matrix([[1, 2, 3], [4, 5, 6]]))
print(Matrix([[1, 2, 3], [4, 5, 6]]))

import numpy as np


def test_init():
    # Test 1: Valid matrix with floats
    matrix = Matrix([[1.1, 2.2], [3.3, 4.4]])
    assert (
        matrix.rows == 2 and matrix.cols == 2
    ), "Test failed! Matrix size is incorrect."

    # Test 2: Invalid matrix (rows with different lengths)
    try:
        matrix = Matrix([[1.1, 2.2], [3.3]])
    except ValueError as e:
        assert (
            str(e) == "Matrix Error: All rows must have the same length."
        ), f"Test failed! {e}"

    # Test 3: Empty matrix
    try:
        matrix = Matrix([])
    except ValueError as e:
        assert (
            str(e) == "Matrix Error: Matrix must be a list of lists."
        ), f"Test failed! {e}"

    print("Initialization tests passed!")


def test_zero_matrix():
    # Test 1: Create a zero matrix of size 3x3
    matrix = Matrix.zero_matrix(3, 3)
    expected_matrix = np.zeros((3, 3))
    assert np.allclose(
        matrix.data, expected_matrix
    ), f"Test failed! Expected {expected_matrix}, got {matrix.data}"

    # Test 2: Edge case with size 0 (should raise an error)
    try:
        matrix = Matrix.zero_matrix(0, 3)
    except ValueError as e:
        assert (
            str(e) == "Matrix Error: Dimensions must be positive integers."
        ), f"Test failed! {e}"

    print("Zero matrix tests passed!")


def test_identity_matrix():
    # Test 1: Create a 3x3 identity matrix
    matrix = Matrix.identity_matrix(3)
    expected_matrix = np.eye(3)
    assert np.allclose(
        matrix.data, expected_matrix
    ), f"Test failed! Expected {expected_matrix}, got {matrix.data}"

    # Test 2: Edge case with size 0 (should raise an error)
    try:
        matrix = Matrix.identity_matrix(0)
    except ValueError as e:
        assert (
            str(e) == "Matrix Error: Side length must be a positive integer."
        ), f"Test failed! {e}"

    print("Identity matrix tests passed!")


def test_str():
    # Test 1: Convert matrix to string
    matrix = Matrix([[1.1, 2.2], [3.3, 4.4]])
    expected_str = "1.1 2.2\n3.3 4.4\n"
    assert (
        str(matrix) == expected_str
    ), f"Test failed! Expected {expected_str}, got {str(matrix)}"

    print("String conversion tests passed!")


def test_getitem_setitem():
    # Test 1: Get and set matrix elements
    matrix = Matrix([[1.1, 2.2], [3.3, 4.4]])
    assert (
        matrix[0, 0] == 1.1
    ), "Test failed! Incorrect value in position (0,0)"

    matrix[0, 0] = 5.5
    assert (
        matrix[0, 0] == 5.5
    ), "Test failed! Incorrect value in position (0,0) after setting."

    # Test 2: Invalid index access
    try:
        matrix[2, 2]
    except IndexError as e:
        assert (
            str(e) == "Matrix Error: Index out of bounds."
        ), f"Test failed! {e}"

    # Test 3: Invalid index assignment
    try:
        matrix[2, 2] = 9.9
    except IndexError as e:
        assert (
            str(e) == "Matrix Error: Index out of bounds."
        ), f"Test failed! {e}"

    print("Get/Set item tests passed!")


def test_transposition():
    # Test 1: Transpose of a 2x3 matrix
    matrix = Matrix([[1.1, 2.2, 3.3], [4.4, 5.5, 6.6]])
    transposed_matrix = matrix.transposition()
    expected_matrix = np.transpose([[1.1, 2.2, 3.3], [4.4, 5.5, 6.6]])
    assert np.allclose(
        transposed_matrix.data, expected_matrix
    ), f"Test failed! Expected {expected_matrix}, got {transposed_matrix.data}"

    # Test 2: Edge case: 1x1 matrix
    matrix = Matrix([[1.1]])
    transposed_matrix = matrix.transposition()
    assert np.allclose(
        transposed_matrix.data, [[1.1]]
    ), f"Test failed! Expected [[1.1]], got {transposed_matrix.data}"

    print("Transposition tests passed!")


def test_get_info():
    # Test 1: Get info for a 2x2 matrix
    matrix = Matrix([[1.1, 2.2], [3.3, 4.4]])
    info = matrix.get_info()
    expected_info = (
        (2, 2),
        True,
        False,
        False,
        False,
        False,
    )  # 2x2, square, not symmetric, etc.
    assert (
        info == expected_info
    ), f"Test failed! Expected {expected_info}, got {info}"

    print("Get info tests passed!")


def test_addition():
    # Test 1: Matrix addition
    matrix1 = Matrix([[1.1, 2.2], [3.3, 4.4]])
    matrix2 = Matrix([[5.5, 6.6], [7.7, 8.8]])
    result = matrix1 + matrix2
    expected_result = np.array(
        [[1.1 + 5.5, 2.2 + 6.6], [3.3 + 7.7, 4.4 + 8.8]]
    )
    assert np.allclose(
        result.data, expected_result
    ), f"Test failed! Expected {expected_result}, got {result.data}"

    print("Addition tests passed!")


def test_subtraction():
    # Test 1: Matrix subtraction
    matrix1 = Matrix([[5.5, 6.6], [7.7, 8.8]])
    matrix2 = Matrix([[1.1, 2.2], [3.3, 4.4]])
    result = matrix1 - matrix2
    expected_result = np.array(
        [[5.5 - 1.1, 6.6 - 2.2], [7.7 - 3.3, 8.8 - 4.4]]
    )
    assert np.allclose(
        result.data, expected_result
    ), f"Test failed! Expected {expected_result}, got {result.data}"

    print("Subtraction tests passed!")


def test_multiplication():
    # Test 1: Matrix multiplication
    matrix1 = Matrix([[1.1, 2.2], [3.3, 4.4]])
    matrix2 = Matrix([[5.5, 6.6], [7.7, 8.8]])
    result = matrix1 * matrix2
    expected_result = np.array(
        [
            [1.1 * 5.5 + 2.2 * 7.7, 1.1 * 6.6 + 2.2 * 8.8],
            [3.3 * 5.5 + 4.4 * 7.7, 3.3 * 6.6 + 4.4 * 8.8],
        ]
    )
    assert np.allclose(
        result.data, expected_result
    ), f"Test failed! Expected {expected_result}, got {result.data}"

    print("Multiplication tests passed!")


def test_scalar_multiplication():
    # Test 1: Scalar multiplication
    matrix = Matrix([[1.1, 2.2], [3.3, 4.4]])
    result = 2.0 * matrix
    expected_result = np.array(
        [[1.1 * 2.0, 2.2 * 2.0], [3.3 * 2.0, 4.4 * 2.0]]
    )
    assert np.allclose(
        result.data, expected_result
    ), f"Test failed! Expected {expected_result}, got {result.data}"

    print("Scalar multiplication tests passed!")


def test_determinant():
    # Test 1: 2x2 matrix with floats
    matrix = Matrix([[4.5, 7.2], [2.3, 6.8]])
    expected_det = np.linalg.det(np.array([[4.5, 7.2], [2.3, 6.8]]))
    assert np.isclose(
        matrix.determinant(), expected_det
    ), f"Test failed! Expected {expected_det}, got {matrix.determinant()}"

    # Test 2: 3x3 matrix with floats
    matrix = Matrix([[1.1, 2.5, 3.6], [0.9, 4.3, 5.1], [1.2, 0.7, 6.4]])
    expected_det = np.linalg.det(
        np.array(
            [
                [1.1, 2.5, 3.6],
                [0.9, 4.3, 5.1],
                [1.2, 0.7, 6.4],
            ]
        )
    )
    assert np.isclose(
        matrix.determinant(), expected_det
    ), f"Test failed! Expected {expected_det}, got {matrix.determinant()}"

    np.random.seed(42)  # For reproducibility
    random_matrix_data = np.random.rand(
        7, 7
    )  # Generate a 7x7 matrix with random floats
    expected_det = np.linalg.det(random_matrix_data)
    random_matrix = Matrix(
        random_matrix_data.tolist()
    )  # Convert to list and create the Matrix object
    assert np.isclose(
        random_matrix.determinant(), expected_det
    ), f"Test failed! Expected {expected_det}, got {matrix.determinant()}"

    print("Determinant tests passed!")


def test_inverse():
    # Test 1: 2x2 matrix with floats
    matrix = Matrix([[4.5, 7.2], [2.3, 6.8]])
    expected_inv = np.linalg.inv(np.array([[4.5, 7.2], [2.3, 6.8]]))
    computed_inv = matrix.inverse().data
    assert np.allclose(
        computed_inv, expected_inv
    ), f"Test failed! Expected {expected_inv}, got {computed_inv}"

    # Test 2: 3x3 matrix with floats
    matrix = Matrix([[1.1, 2.5, 3.6], [0.9, 4.3, 5.1], [1.2, 0.7, 6.4]])
    expected_inv = np.linalg.inv(
        np.array(
            [
                [1.1, 2.5, 3.6],
                [0.9, 4.3, 5.1],
                [1.2, 0.7, 6.4],
            ]
        )
    )
    computed_inv = matrix.inverse().data
    assert np.allclose(
        computed_inv, expected_inv
    ), f"Test failed! Expected {expected_inv}, got {computed_inv}"

    np.random.seed(42)  # For reproducibility
    random_matrix_data = np.random.rand(
        7, 7
    )  # Generate a 7x7 matrix with random floats
    random_matrix = Matrix(
        random_matrix_data.tolist()
    )  # Convert to list and create the Matrix object

    inverse_matrix = random_matrix.inverse()  # Compute the inverse
    identity_matrix = (
        random_matrix * inverse_matrix
    )  # Multiply original matrix with inverse

    # Create the expected identity matrix (7x7)
    expected_identity = np.eye(7)
    assert np.allclose(
        identity_matrix.data, expected_identity
    ), "Test failed! Inverse multiplication did not result in the identity matrix."

    print("Inverse tests passed!")


def test_equality():
    # Test 1: Equal matrices with floats
    matrix1 = Matrix([[4.5, 7.2], [2.3, 6.8]])
    matrix2 = Matrix([[4.5, 7.2], [2.3, 6.8]])
    assert matrix1 == matrix2, "Test failed! Matrices should be equal."

    # Test 2: Non-equal matrices with floats
    matrix1 = Matrix([[4.5, 7.2], [2.3, 6.8]])
    matrix2 = Matrix([[1.2, 3.4], [5.6, 7.8]])
    assert matrix1 != matrix2, "Test failed! Matrices should not be equal."

    print("Equality tests passed!")


# Running the tests
test_init()
test_zero_matrix()
test_identity_matrix()
test_str()
test_getitem_setitem()
test_transposition()
test_get_info()
test_addition()
test_subtraction()
test_multiplication()
test_scalar_multiplication()
test_determinant()
test_inverse()
test_equality()


M = Matrix3D([
    [[1, 2], [3, 4]],
    [[5, 6], [7, 8]]
])

assert M.determinant_3d() == - 4

M = Matrix3D([
    [[1, 1], [1, 1]],
    [[1, 1], [1, 1]]
])

assert M.determinant_3d() == 0

M = Matrix3D([
    [[10, 30], [10, 60]],
    [[50, 60], [0, 70]]
])

assert M.determinant_3d() == 3100

M = Matrix3D([
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    [[10, 11, 12], [420, 69, 15], [16, 17, 18]],
    [[1, 2, 3], [4, 5, 6], [25, 26, 27]]
])

assert M.determinant_3d() == -8910

M = Matrix3D([
    [[10000000, 2, 20], [4, 30, 6], [7, 40, 500]],
    [[10, 11, 12], [420, 69, 15], [16, 17, 18]],
    [[1, 2, 3], [4, 5, 6], [25, 26, 27]]
])

assert M.determinant_3d() == -14609825901

M = Matrix3D([
    [[1, 2, 20], [4, 30, 6], [7, 40, 500]],
    [[10, 11, 12], [420, 69, 15], [16, 17, 18]],
    [[1, 2, 3], [4, 5, 6], [25, 26, 27]]
])

assert M.determinant_3d() == 172638

M = Matrix3D([
    [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
    [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
    [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
    [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]
])

assert M.determinant_3d() == 0

M = Matrix3D([
    [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
    [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
    [[1, 1, 1, 1], [1, 300, 300, 1], [1, 400, 1, 1], [1, 1, 1, 1]],
    [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]
])

assert M.determinant_3d() == 0

M = Matrix3D([
    [[10, 20, 30, 40], [50, 60, 70, 80], [90, 100, 110, 120], [130, 140, 150, 160]],
    [[170, 180, 190, 200], [210, 220, 230, 240], [250, 260, 270, 280], [290, 300, 310, 320]],
    [[330, 340, 350, 360], [370, 380, 390, 400], [410, 420, 430, 440], [450, 460, 470, 480]],
    [[490, 500, 510, 520], [530, 540, 550, 560], [570, 580, 590, 600], [610, 620, 630, 640]]
])

assert M.determinant_3d() == 0

M = Matrix3D([
    [[10, 20, 30, 40], [50, 60, 70, 80], [90, 100, 110, 1274580], [130, 140, 150, 160]],
    [[170, 10148580, 190, 200], [210, 220, 230, 701000], [250, 260, 270, 280], [290, 300, 310, 320]],
    [[330, 340, 350, 360], [370, 380, 390, 400], [410, 420, 430, 4444440], [450, 460, 470, 480]],
    [[490, 500, 510, 548964], [530, 540, 550, 560], [570, 580, 590, 600], [610, 620, 630, 640]]
])
assert M.determinant_3d() == -185706302284800000

M = Matrix3D([
    [[1, 1, 1, 1], [1, 1, 1, 4987], [1, 1, 1, 1], [1, 1, 1, 1]],
    [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [156, 1, 1, 1]],
    [[1, 1, 1, 1], [1, 300, 300, 1], [1, 400, 1, 1], [1, 1, 1, 1]],
    [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]
])
assert M.determinant_3d() == -308359170
