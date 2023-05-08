# Define a list of dictionaries representing people with their names and houses.
people = [
    {"name": "Harry", "house": "Gryffindor"},
    {"name": "Cho", "house": "Ravenclaw"},
    {"name": "Draco", "house": "Slytherin"},
]

# Sort the "people" list based on the value of the "name" key in each dictionary using a lambda function as the sorting key.
people.sort(key=lambda person: person["name"])

# Print the sorted "people" list.
print(people)

# Print the "name" of the sorted "people" list
for person in people:
    print(person["name"])
