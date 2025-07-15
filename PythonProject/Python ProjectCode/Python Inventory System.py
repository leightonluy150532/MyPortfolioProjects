import tkinter as AA
AB = AA.Tk()

def savecust():
    print("Saved")

def products():
    print("Products menu clicked")
    # Create a new window for products
    AC = AA.Toplevel(AB)
    AC.title("Python Window")
    AC.geometry("1050x440")
    AC.configure(bg="white")
    label = AA.Label(AC, text="Products Information System", height=1, bg="yellow")
    label.config(font=("Times New Roman", 10))
    label.grid(column=1, row=1)

def supplier():
    print("Supplier menu clicked")

AB.title("Python Window")
AB.geometry("1050x440")
AB.configure(bg="white")

label = AA.Label(AB, text="Customer Information System", height=1, bg="yellow")
label.config(font=("Times New Roman", 10))
label.grid(column=1, row=1)

label = AA.Label(AB, text="Enter Name:", height=1, bg="yellow")
label.config(font=("Courier", 10))
label.grid(column=1, row=2)

cname = AA.StringVar()
custname = AA.Entry(AB, textvariable=cname)
custname.grid(column=2, row=2)

label = AA.Label(AB, text="Enter Address:", height=1, bg="yellow")
label.config(font=("Courier", 10))
label.grid(column=1, row=3)

caddress_var = AA.StringVar()
caddress = AA.Entry(AB, textvariable=caddress_var)
caddress.grid(column=2, row=3)

savebtn = AA.Button(AB, text="Save Customer", command=savecust)
savebtn.grid(column=1, row=4)

menubar = AA.Menu(AB)
filemenu = AA.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="products", command=products)
filemenu.add_command(label="Supplier", command=supplier)
filemenu.add_separator()
filemenu.add_command(label="close", command=AB.quit)
AB.config(menu=menubar)
