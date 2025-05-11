"""
m1 = macierz(
[ [1, 0, 2],
  [-1, 3, 1] ]
)
"""

class Matrix(object):
    def __init__(self, arg, o = 0):
        if isinstance(arg, tuple):
            self.__matrix = [[o for _ in range(arg[1])] for _ in range(arg[0])]
        else:
            self.__matrix = arg

    def __add__(self, other):
        #sprawdzamy wymiary macierzy
        if len(self.__matrix) != len(other.__matrix) or len(self.__matrix[0]) != len(other.__matrix[0]):
            raise ValueError("Matrixes have different shapes, therefore we cannot add them!")
        #najpierw robimy columns a pozniej rows
        return Matrix([[self.__matrix[i][j] + other.__matrix[i][j] for j in range(len(self.__matrix[0]))] for i in range(len(self.__matrix))])

    def __sub__(self, other):
        if len(self.__matrix) != len(other.__matrix) or len(self.__matrix[0]) != len(other.__matrix[0]):
            raise ValueError("Matrixes have different shapes, therefore we cannot sub them!")  
        return Matrix([[self.__matrix[i][j] - other.__matrix[i][j] for j in range(len(self.__matrix[0]))] for i in range(len(self.__matrix))])

    def __mul__(self, other):
        #sprawdzamy czy liczba kolumn 1 macierzy = li wierszy 2 macierzy
        if len(self.__matrix[0]) != len(other.__matrix):
            raise ValueError("Num of columns in matrix 1 != num of rows in matrix 2, therefore we cannot mul them!")
        #k dla obu przypadkow to same bo li. kolumn 1 = li. wierszy 2
        return Matrix([[sum([self.__matrix[i][k] * other.__matrix[k][j] for k in range(len(self.__matrix[0]))]) for j in range(len(other.__matrix[0]))] for i in range(len(self.__matrix))])

    def __getitem__(self, key):
        return self.__matrix[key]

    def __str__(self):
        string = ""
        for row in self.__matrix:
            string += "|" + " ".join(map(str, row)) + "|\n"
        return string

    def size(self):
        return (len(self.__matrix), len(self.__matrix[0]))
    

def transpose(matrix):
    rows, columns = matrix.size()
    return Matrix([[matrix[i][j] for i in range(rows)] for j in range(columns)])


sample_matrix1 = [[1, 0, 2], [-1, 3, 1]]
sample_matrix2 = [[3, 1], [2, 1], [1, 0]]
m1 = Matrix(sample_matrix1)
m2 = Matrix((2, 3), 1)
m3 = Matrix(sample_matrix2)
m1_transposed = transpose(m1)
#print(m1)
print(m1_transposed)
print(m1 + m2)
print(m1 * m3)