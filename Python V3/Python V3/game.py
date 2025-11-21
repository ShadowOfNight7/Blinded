import multiprocessing, time, inputimeout, os, asyncio, keyboard, math


#Plan:, pyfiglet
textlength = os.get_terminal_size().columns
screen = [["#"*textlength],
    ["#"*textlength],
    ["#"*textlength],
    ["#"*textlength],
    ["#"*textlength],
    ["#"*textlength],
    ["#"*textlength],
    ["#"*textlength],
    ["#"*textlength],
    ["#"*textlength]]
coords_x, coords_y = 5, 3




while True:
    textlength = os.get_terminal_size().columns
    os.system("cls")

    key = keyboard.is_pressed('a')
    if key == True:
        coords_x -= 1

    for i in screen:
        print(i[0])
    
    screen = [["#"*textlength],
    ["#"*textlength],
    ["#"*textlength],
    ["#"*textlength],
    ["#"*textlength],
    ["#"*textlength],
    ["#"*textlength],
    ["#"*textlength],
    ["#"*textlength],
    ["#"*textlength]]

    x = ""
    y = 0
    for i in screen[coords_y][0]:
        if y != coords_x:
            x += i
        else:
            x += "X"
        y += 1
    screen[coords_y][0] = x

    time.sleep(0.2)
    coords_x += 1


time.sleep(999)

#Research - Each room gives base amount 












#Stats







async def count():
    print(input(">>> "))

async def main():
    await asyncio.gather(count())

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - start
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
