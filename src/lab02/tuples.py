def f(records):
    result = []
    for rec in records:
        fio, group, gpa = rec
        cleaned_fio = [" ".join(fio.strip().split()), group, gpa]
        if len(cleaned_fio[0].split()) >= 3:
            name = cleaned_fio[0].split()[1][0].title() + "."
            otch = cleaned_fio[0].split()[2][0].title() + "."
            famil = cleaned_fio[0].split()[0].title()
            form = f"{famil} {name}{otch}"
            form_res = f"{form}, гр. {cleaned_fio[1]}, GPA {gpa:.2f}"
            result += [form_res]
        if len(cleaned_fio[0].split()) <= 2:
            name = cleaned_fio[0].split()[1][0].title() + "."
            famil = cleaned_fio[0].split()[0].title()
            form = f"{famil} {name}"
            form_res = f"{form}, гр. {cleaned_fio[1]}, GPA {gpa:.2f}"
            result += [form_res]
    return result


test_cases = [
    ("Иванов Иван Иванович", "BIVT-25", 4.6),
    ("Петров Пётр", "IKBO-12", 5.0),
    ("  cидорова  анна   сергеевна ", "ABB-01", 3.999),
]
print(f(test_cases))


# test_cases = [
#     ("Иванов Иван Иванович", "BIVT-25", 4.6),
#     ("Петров Пётр", "IKBO-12", 5.0),
#     ("  cидорова  анна   сергеевна ", "ABB-01", 3.999)
# ]

# count=0
# for rec in test_cases:
#     fio, group, gpa = rec

#     cleaned_fio = [' '.join(fio.strip().split()),group,gpa]
#     if len(cleaned_fio[0].split())>=3:
#         name=cleaned_fio[0].split()[1][0].title()
#         otch=cleaned_fio[0].split()[2][0].title()
#         famil=cleaned_fio[0].split()[0].title()
#         print(famil,name+'.',otch+'., гр.',cleaned_fio[1]+',','GPA '+f'{gpa:.2f}')


#     if len(cleaned_fio[0].split())<=2:
#         name=cleaned_fio[0].split()[1][0].title()
#         famil=cleaned_fio[0].split()[0].title()
#         # print(famil,name+'., гр.',cleaned_fio[1]+',','GPA '+f'{gpa:.2f}')
#         print(cleaned_fio[0].split()[0].title(),cleaned_fio[0][0])
