n = input()
l = list()
for k in range(n):
    inputNum = int(input())
    # odd
    if inputNum % 2 != 0:
        min = max = 0
    else:
        # even
        # min
        j = inputNum / 4
        i = inputNum % 4 / 2
        min = i + j
        # max
        max = inputNum / 2
    l += [(min, max)]

for a, b in l:
    print(a,b)
