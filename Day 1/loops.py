#while loop
#syntax
#while condition:
    #code to execute while condition is true

i = 0
while i <= 10:
    print(i)
    i += 1

i = 1
print("Numbers from 1 to 10:")
while i <= 10:
    print(i)
    i += 1
    print("even number from 20 to 40:")

while i <=40:
    if i % 2==0:
        print(i)
    i += 1
#for loop

numbers = [3, 7, 13, 19, 23, 12]
total = 0    
product = 1      

print("printing the list items:")
for num in numbers:
    print(num)

for num in numbers:
    total += num
print(f"Sum of all numbers:{total}")


for num in numbers:
    product *= num
print("Final product of the numbers:", product)