import time, random

UserName = input("What is your name? >>> ")
print("Hello, " + str(UserName))
time.sleep(0.5)
Answer = "Y"
NumStars = 0
while Answer.lower() in ["y", "yes", "1", "one"]:
    while NumStars <= 0:
        try:
            NumStars = int(input("How many stars do you want >>> "))
        except ValueError:
            NumStars = 0
            print("Please write a valid answer.")
            time.sleep(0.5)
        if NumStars <= 0:
            print("Please write an answer greater than 0.")
            time.sleep(0.5)
    Spread = -1
    while Spread < 0:
        try:
            Spread = int(input("How distant do you want these stars >>> "))
        except ValueError:
            Spread = -1
            print("Please write a valid answer.")
            time.sleep(0.5)
        if Spread < 0:
            print("Please write an answer greater than 0.")
            time.sleep(0.5)
    stars = ""
    while NumStars > 0:
        if random.randint(1, Spread) == 1:
            stars += "*"
            NumStars -= 1
        else:
            stars += " "
    print(stars)
    Answer = ""
    while Answer == "":
        Answer = input("""Do you want more stars? 
1) Yes
2) No
>>> """)
        if Answer.lower() not in ["n", "no", "2", "two", "y", "yes", "1", "one"]:
            print("Please put in a valid answer.")
            time.sleep(0.5)
            Answer = ""
print("Goodbye, " + str(UserName))
