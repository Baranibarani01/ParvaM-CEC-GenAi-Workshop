#if condition

#syntax
#if condition:
    #code to execute if condition is true

number = 20
if number % 2 == 0:
    print("The number is Even number.")

if number % 2 == 0 and number% 5 ==0:
    print(f"{number} is both mutiples of 2& 5.")

    #if condition

#syntax
#if condition:
    #code to execute if condition is true

number = 20
if number % 2 == 0:
    print("The number is even.")

if number % 2 != 0 and number % 5 == 0:
    print(f"{number} is both multiple of 5 and 2.")

# if-else condition
#syntax
#if condition:
    #code to execute if condition is true
#else:
    #code to execute if condition is false

if number % 2 == 0:
    print("The number is even.")
else:
    print("The number is odd.")

    #if else(elif) condition
#syntax
#if condition1:
    #code to execute if condition1 is true
#elif condition2:
    #code to execute if condition2 is true
#else:
    #code to execute if both condition1 and condition2 are false

marks = 68
if marks > 85:
    print("Distinction")
elif marks > 75:
    print("First Class")
elif marks > 65:
    print("Second Class")
elif marks > 55:
    print("Above Average")
elif marks > 35:
    print("Below Average")
else:
    print("Fail")

 #nested if else:

 #syntax:
 #if condition1:
#if condition2: 
#True
             #else:
             #False
             #else:
             #false

num1 = 35
num2 = 25
num3 = 30
if num1 > num2:
    if num1 > num3:
        print(f"{num1} is the greatest number.")
    else:
        print(f"{num3} is the greatest number.")
else:
    if num2 > num3:
        print(f"{num2} is the greatest number.")
    else:
        print(f"{num3} is the greatest number.")