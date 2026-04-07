import numpy as np
A = np.array([
    [2, 5, 7],
    [1, 2, 3],
    [7, 8, 2]
])

B = np.array([
    [5, 0, 5],
    [3, 0, 4],
    [1, 6, 2]
])
#matrix(row,column)
print(A[0,1])
#Summation
print(A+B)
#Subtraction
print(A-B)
#dot product
print(A.dot(B))
#element-wise multiplication
print(A*B)
#inverse
print(np.linalg.inv(A))

