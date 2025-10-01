def count_freq(tokens: list[str]):
    d={x:tokens.count(x) for x in set(tokens)}
    return sorted(d.items(),key=lambda x:-x[1])
test_case1 = (["a","b","a","c","b","a"])
test_case2=["bb","aa","bb","aa","cc"]
print(count_freq(test_case1),count_freq(test_case2))