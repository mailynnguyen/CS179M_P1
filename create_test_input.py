def create_test_input(): 
    n = 256
    s = n / 4 # 32
    piece = 1 / s

    with open(f"{n}Square4.txt", "w") as output_file:
        # bottom side of square
        for i in range(int(s)):
            output_file.write(f"{(piece * i):.7e}  0\n")
        for i in range(int(s)):
            output_file.write(f"1  {(piece * i):.7e}\n")
        for i in range(int(s)):
            output_file.write(f"{(1 - (piece * i)):.7e}  1\n")
        for i in range(int(s)):
            output_file.write(f"0  {1 - (piece * i):.7e}\n")



create_test_input()