year1, year2 =input().split()
year1= int(year1)
year2= int(year2)



if year1 > year2:
    print("Cannot Compute!")
else:
    result = ""
    first = True

    for yr in range(year1, year2 + 1):
        if  yr % 3 == 0 and yr % 4 == 0:
            if first:
                result += str(yr)
                first = False
            else:
               result += " " +str(yr)

print(result)
            
