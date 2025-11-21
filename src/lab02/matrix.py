def f(matrix):
    return [list(row) for row in zip(*matrix)]


arr1 = [[1, 2, 3]]
arr2 = [[1], [2], [3]]
arr3 = [[1, 2], [3, 4]]
print(f(arr3), f(arr2), f(arr1))


def f(n):
    res = [sum(x) for x in n]
    return res


arr1 = [[1, 2, 3], [4, 5, 6]]
arr2 = [[-1, 1], [10, -10]]

print(f(arr1), f(arr2))


def f(n):
    return [sum(x) for x in zip(*n)]


arr1 = [[1, 2, 3], [4, 5, 6]]
arr2 = [[-1, 1], [10, -10]]
arr3 = [[0, 0], [0, 0]]
print(f(arr1), f(arr2), f(arr3))
