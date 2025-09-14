# minutes=int(input())
# count=0
# hours=(minutes-minutes%60)//60
# resmin=minutes%60
# result=f'{str(hours)}' + ':' + f'{str(resmin)}'
# print(result)

m = int(input().strip())
hours = m // 60
minutes = m % 60
print(f"{hours}:{minutes:02d}")