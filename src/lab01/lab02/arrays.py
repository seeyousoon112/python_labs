def f(n):
    a=[x for x in n]
    return min(a),max(a)
arr=[1.5, 2,-3.1]
print(f(arr))

def f(n):
    a=sorted(set(x for x in n))
    return a
arr=[1.0,1,2.5,2.5,0]
print(f(arr))

def f(n):
    res=[]
    for x in n:
        for y in x:
            res+=[y]
    return res
arr=[[1],[],[2,3]]
print(f(arr))