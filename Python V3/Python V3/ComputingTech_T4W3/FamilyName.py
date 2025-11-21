firstname, familyname = input("What is your first name? "),input("What is your family name? ")
print("Hello,", firstname, familyname + "!")
print("Welcome to the sequence control structure!")
stars = int(input("Do you want to meet some stars? How many? "))
print(firstname, familyname, "meets")
for i in range(stars):
    print("*", end=' ')
