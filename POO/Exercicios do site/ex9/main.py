# OOP Exercise 9: Check object is a subclass of a particular class

"""
Write a code to check the following

    Dog is a subclass of Animal? –> True
    Animal is a subclass of Dog? –> False
    Cat is a subclass of Animal? –> False
    Puppy is a subclass of Animal –> True

"""

class Animal:
    pass

class Dog(Animal):
    pass

class Puppy(Dog):
    pass

class Cat:
    pass
    
if issubclass(Dog, Animal):
    print(True)
else:
    print(False)
    
if issubclass(Animal, Dog):
    print(True)
else:
    print(False)
    
if issubclass(Cat, Animal):
    print(True)
else:
    print(False)
    
if issubclass(Puppy, Animal):
    print(True)
else:
    print(False)
    

