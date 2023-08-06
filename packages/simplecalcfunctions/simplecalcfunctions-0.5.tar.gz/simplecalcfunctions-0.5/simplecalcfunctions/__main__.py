print("You Have Imported Simple Calculation Module")

def add(a,b):
    c=a+b
    print(f"The Sum of {a} and {b} is {c}")
def sub(a,b):
    c=a-b
    print(f"The Difference of {a} and {b} is {c}")
def mul(a,b):
    c=a*b
    print(f"The Product of {a} and {b} is {c}")
def div(a,b):
    c=a/b
    print(f"The Quotient of {a} and {b} is {c}")
def rem(a,b):
    c=a%b
    print(f"The Remainder of {a} and {b} is {c}")
def exp(a,b):
    c=a**b
    print(f"The Exponential Value of {a} power {b} is {c}")
def feb(n):
    a,b=0,1
    while a < n:
        print(a,end=" ")
        a,b=b,a+b
    print()
def arm(a):
    sum = 0
    temp = a
    while temp> 0:
        digit = temp % 10
        sum += digit ** 3
        temp //= 10
    if a == sum:
        print(a,"is an Armstrong Number")
    else:
        print(a,"is not an Armstrong Number")
def helpcalc():
    print("""Syntax for this modlue calc_name(num1,num2)
Operation names are \'add\' for addition, \'sub\' for subtraction,
\'mul\' for multiplication, \'div\' for quotient,
\'rem\' for getting remainder,\'exp\' for exponential multiplication.
\'feb(num)\' for getting febnacci series until n number
\'arm(num) for seeing if given number is a armstrong number or not\'""")

helpcalc=helpcalc()
