even_set = set()
odd_set = set()
for x in range(11):
    if x % 2 == 0:
        even_set.add(x)
    else:
        odd_set.add(x)
all_nums = even_set.union(odd_set)
print(all_nums)
