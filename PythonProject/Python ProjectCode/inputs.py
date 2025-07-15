from Shape import Shape
# input tester for exer04
# do not edit any part of this file!

inp = input().split() # space separated inputs
inputs=()
for x in inp:
    # convert each input to float, save each input into tuple
    inputs = inputs + (float(x),) 
# initializes inputs as separate values
s = Shape(*inputs)
# prints shape area
s.printArea()
