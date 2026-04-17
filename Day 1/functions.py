# functions:
#syntax:
#def functions_name(parameters):
#rules of function

#parts of function:
# 1) Function Declaration
# 2) Function Definition
# 3) Function Call

#function Declaration
def greet():
    pass
#function definition
def greet():
    print("Good morning sir")    
#function call   
greet()
greet()
greet()

#function with parameters:
#variables within paranthesis while calling a function is called as arguments
#name is a parameter


def sayHello(name):
    print(f"Hello, {name}!")

# Akshay Rao, Akash & Hemanth are examples of arguments
sayHello("Akshay Rao")
sayHello("Akash")
sayHello("Hemanth")

def sum(a, b):
    print(f"Sum of (a) & (b) is (a + b)")

sum(10, 20)
sum(25, 40)
#default parameter
def printDetails(name, company="Parvam"):
    print(f"I'm {name} and I work at {company}.")
printDetails("Soumya")
printDetails("Alice", "Google")

# *args - Variable Positional Arguments

def findSum(*args):
    sum = 0
    for num in args:
        sum += num
    print(f"Sum of given numbers: {sum}")

# Function calls
findSum(20, 30)
findSum(20, 30, 50)
findSum(20, 30, 50, 60, 80)
findSum(20, 30, 50, 60, 80, 95, 100)

def findEvenOdd(*args):
    print("The given numbers are as follows:")
    for num in args:
        print(num)

    print("Even numbers out of given numbers are as follows:")
    for num in args:
        if num % 2 == 0:
            print(num)

    print("Odd numbers out of given numbers are as follows:")
    for num in args:
        if num % 2 != 0:
            print(num)


# Function calls
findEvenOdd(2, 4, 7, 9, 11)
findEvenOdd(1, 3, 6, 8, 11, 14, 16, 19)
# Function calls for even/odd
findEvenOdd(2, 4, 7, 9, 11)
findEvenOdd(1, 3, 6, 8, 11, 14, 16, 19)
findEvenOdd(5, 8, 11, 12, 18, 22, 23)


# **kwargs - Variable length keyword arguments
def printInfo(**person):
    print(f"He is {person['name']}, he is working at {person['company']}")


# Function calls
printInfo(name="Akshay Rao", age=24, company="Parvah", address="Bengaluru")

printInfo(name="Varun", company="Infosys", address="Bengaluru", pincode=560090)

# Function call from previous part
printInfo(name="Varun", company="Infosys", address="Bengaluru", pincode=560090)


# Function using **kwargs
def userInfo(**user):
    print("User Details are as follows:")
    print(f"Name: {user['name']}")
    print(f"Email ID: {user['email']}")
    print(f"Phone Number: {user['phone']}")


# Function calls
userInfo(
    name="Akshay",
    id=123,
    email="akshay@gmail.com",
    company="Parvah",
    phone="9623145123",
    mode_of_transport="Bus"
)

userInfo(
    name="Ajay",
    usn="AJ456",
    email="akshay@gmail.com",
    college="RVCE",
    phone="9623145123")