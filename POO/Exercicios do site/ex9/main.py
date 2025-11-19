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
    
print(issubclass(Dog, Animal))
print(issubclass(Animal, Dog))
print(issubclass(Cat, Animal))
print(issubclass(Puppy, Animal))
