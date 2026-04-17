#DataType in python

name ="Barani"
age = 21
Hieght = 5
isTrainer = False
#string
print(name , type(name))
#integer
print(age,type(age))
#float
print(Hieght,type(Hieght))
#boolean
print(isTrainer,type(isTrainer))
#ctrl+shift+~ =open treminal
#python filename.py  - run python code


#Non primitive DataType: List, Tuple, Set & Dictionary
#list is ordered, mutable(changeable) it allows duplicates values
languages_Known =["c","c++","java","python","PHP"]

print(languages_Known,type(languages_Known))

#tuple is representedusing '()' paranthesis
#tuple is ordered, imutable(unchangeable)& allows duplicate values
even_number = (2,4,8,12,18,20,4,6,12)
print(even_number,type(even_number))

#set is repersented using '{}' flower Brackets
#set is unordered, imutable & doesn't duplicate values
odd_number={1,5,17,21,33,27}
print(odd_number,type(odd_number))

#dictionary is represented using key-value pairs

profile={
     "name":"Barani",
     "age":21,
     "company":"microsoft",
     "role": "Developer",
     "technologies":["Django","Laravel","Spring","React"]
}
print(profile,type(profile))