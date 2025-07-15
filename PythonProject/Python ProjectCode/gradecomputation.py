inputs = input().split()
inp =[]

for grade in inputs:
    inp.append(int(grade))

average = sum (inp) / len (inp)
fail = 0

for grade in inp:
    if grade < 72:
        fail+=1
if fail == 0:
    msg = "You didn't fail in any subject." 
elif fail == 1:
    msg = "You failed in one subject"
elif fail == len(inp):
   msg = " You failed in all your subjects"
else:
    msg = "You failed in " +str(fail)+ " subjects."

print("Average: {:.2f} {}".format(average, msg))

