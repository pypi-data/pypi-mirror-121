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

helpcalc = """Syntax for this modlue calc_name(num1,num2)\n
Operation names are \'add\' for addition, \'sub\' for subtraction,\n
\'mul\' for multiplication, \'div\' for quotient,\n \'rem\' for getting
remainder,\'exp\' for exponential multiplication."""
