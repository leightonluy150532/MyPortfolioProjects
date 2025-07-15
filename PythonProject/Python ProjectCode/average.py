inp = input().split()
l = []

for item in inp:
    l.append(int(item))

average = sum(l)/len(l)
print(average)
