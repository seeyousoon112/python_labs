def f(n):
    a=[x for x in n]
    return min(a),max(a)
arr1=[1.5, 2,-3.1]
arr2=[42]
arr3=[-5,-2,-9]
arr4=[1.5,2,2.0,-3.1]
print(f(arr1),f(arr2),f(arr3),f(arr4))

def f(n):
    a=sorted(set(x for x in n))
    return a
arr3=[1.0,1,2.5,2.5,0]
arr2=[-1,-1,0,2,2]
arr1=[3,1,2,1,3]

print(f(arr1),f(arr2),f(arr3))

def f(n):
    res=[]
    for x in n:
        for y in x:
            res+=[y]
    return res
arr3=[[1],[],[2,3]]
arr2=[[1,2],(3,4,5)]
arr1=[[1,2],[3,4]]
print(f(arr1),f(arr2),f(arr3))