string = input()
out = ''
num = len(string)
for word in string:
    out = word + out
print(out, num,"characters")
