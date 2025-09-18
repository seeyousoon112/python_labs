def f(n):
    return [[x] for x in n[0]]
arr=[[1,2,3]]
print(f(arr))

def f(n):
    res=[sum(x) for x in n]
    return res
test=[[1,2,3],[4,5,6]]
print(f(test))

def f(n):
    return [sum(x) for x in zip(*n)]
arr=[[1,2,3],[4,5,6]]
print(f(arr))