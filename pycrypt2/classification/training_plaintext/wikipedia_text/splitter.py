with open("wikipedia_short.txt") as f:
    for i, length in enumerate(list(range(500, 1000, 2)) + list(range(500, 1000, 2))
                               + list(range(500, 1000, 2)) + list(range(500, 1000, 2))):
        with open("..\\wikipedia (" + str(i + 1) + ").txt", mode="w") as f2:
            f2.write(f.read(length).upper())
