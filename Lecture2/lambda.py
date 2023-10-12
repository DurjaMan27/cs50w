people = [
    {"name": "Harry", "house": "Gryffindor"},
    {"name": "Cho", "house": "Ravenclaw"},
    {"name": "Draco", "house": "Slytherin"}
]

# cannot use .sort() because it doesn't know how to sort dictionaries

'''
def f(person):
    return person["house"]

people.sort(key=f) # allows you to sort by the function defined above
'''

# using a lambda function to shorten the above code
people.sort(key=lambda person: person["name"])

print(people)