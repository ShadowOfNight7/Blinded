import time, random

randomNum = random.randint(1, 1000)
while True:
    Guess = ""
    while Guess == "":
        try:
            Guess = int(input("Guess a random number. >>> "))
        except ValueError:
            print("Please type a valid answer.")
            Guess = ""
    randomHint = 0
    while (Guess != randomHint):
        randomHint = random.randint(1, 100)
        if randomHint > 50:
            if Guess < randomNum:
                print("Higher!")
            elif Guess > randomNum:
                print("Lower!")
            break
        if 50 >= randomHint > 0:
            print("The random number is within", random.randint(abs(Guess - randomNum), min(3 * abs(Guess - randomNum), abs(Guess - 1000), abs(1000 - Guess))))
            break
    if Guess == randomNum:
        print("You guessed correctly! The random number was", str(randomNum) + ".")
        time.sleep(0.5)
        Again = input("Try again? >>> ")
        if Again.lower() in ["yes", "y", "ye", "yep", "sure", "ok", "okay", "absolutely", "1", "one"]:
            randomNum = random.randint(1, 1000)
        else:
            break