from string import *

# sub='thisisabracadabraHt1eadljjl12ojh.'
sub = str(input())
abc1 = ascii_uppercase
abc2 = ascii_lowercase
count_first_letter = 0
result = ""
count_second_letter = 0
ind1 = -1
ind2 = -1
trueresult = ""

for i in range(len(sub) - 1):
    if sub[i] in ascii_uppercase:
        count_first_letter += 1
    if sub[i] in ascii_uppercase and count_first_letter == 1:
        result += sub[i]
        ind1 = i
    if sub[i] in "0123456789" and sub[i + 1] in abc2:
        count_second_letter += 1
    if count_second_letter == 1 and sub[i] in "0123456789" and sub[i + 1] in abc2:
        ind2 = i + 1
        result += sub[i + 1]
for i in range(ind1, len(sub), ind2 - ind1):
    trueresult += sub[i]
print(trueresult)
