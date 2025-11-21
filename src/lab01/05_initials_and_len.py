fio = str(input())
res = ""
for i in range(len(fio) - 1):
    if fio[i - 1] == " " and fio[i] in "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ":
        res += str(fio[i])
k = 2
for j in fio:
    if j != " ":
        k += 1
print(res + ".", k)
