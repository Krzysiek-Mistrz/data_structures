import numpy as np


def chio_det(matrix):
    n = len(matrix)
    sign = 1

    #Warunek końca
    if n == 1:
        return matrix[0][0]
    elif n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    a_11 = matrix[0][0]
    #Sprawdzamy 1 elem po kolei w rows zeby != 0 w matrix i najwyzej zamienimy wiersz 0 z wybranym wierszem i zmieniamy znak
    if a_11 == 0:
        for k in range(1, n):
            if matrix[k][0] != 0:
                matrix = np.array(matrix)
                matrix[[0, k], :] = matrix[[k, 0], :]
                a_11 = matrix[0][0]
                sign = -1
                break
        else:
            raise ValueError("The matrix is singular and cannot be processed")
    
    subm = np.zeros((n-1, n-1))
    for i in range(1, n):
        for j in range(1, n):
            #Kazdy elem wyznaczamy jako a_ij * a_11 - a_i1 * a_1j (zgodnie ze trescia)
            subm[i-1][j-1] = (matrix[i][j] * a_11 - matrix[i][0] * matrix[0][j])
    
    #Wywolujemy rekurencyjnie aż do n = 1 lub n = 2
    return sign * chio_det(subm) / (a_11 ** (n-2))


matrix1 = [
    [5, 1, 1, 2, 3],
    [4, 2, 1, 7, 3],
    [2, 1, 2, 4, 7],
    [9, 1, 0, 7, 0],
    [1, 4, 7, 2, 2]
]
matrix2 = [
    [0 , 1 , 1 , 2 , 3],
    [4 , 2 , 1 , 7 , 3],
    [2 , 1 , 2 , 4 , 7],
    [9 , 1 , 0 , 7 , 0],
    [1 , 4 , 7 , 2 , 2]
] 
result = chio_det(matrix1)
print("wynik:", result)
result = chio_det(matrix2)
print("wynik:", result)