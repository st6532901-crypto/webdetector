#calculator.py  
a=int(input("Enter first number: "))
operation=input("Enter operation (+, -, *, /): ")
b=int(input("Enter second number: "))
if operation=='+':
    print("result:", a+b)
elif operation=="-":
    print("result:", a-b)
elif operation=="/":
    if b!=0:
        print("result:", a/b)
    else:
        print("Error : This number cannot be divided by zero")
elif operation=="*":
    print("result:", a*b)
else:
    print("Error: your operation is invalid")