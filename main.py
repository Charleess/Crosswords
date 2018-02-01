""" DM1 """
import numpy as np
import time
from constraint_programming import constraint_programming

def parse_lines(matrix, orient):
    slots = set()
    lines = []
    for i, line in enumerate(matrix):
        # Remove the special characters
        parse_word = False
        current_word = [None, None, None, orient]

        for j, char in enumerate(line):
            if char == "#":
                if current_word[0] is not None:
                    if current_word[1] == current_word[2]:
                        parse_word = False
                        current_word = [None, None, None, orient]
                    else:
                        lines.append(current_word)
                        parse_word = False
                        current_word = [None, None, None, orient]
            else:
                if not parse_word:
                    parse_word = True
                    slots.add((i, j))
                    current_word[0] = i
                    current_word[1] = j
                    current_word[2] = j
                else: 
                    slots.add((i, j))
                    current_word[2] = j
    
    return lines, slots

def get_letters(words_file):
    with open("src/{}".format(words_file), 'r') as file:
        letters = set()
        for line in file:
            for char in line.strip():
                if ord(char.upper()) >= 65 and ord(char.upper()) <= 90:
                    letters.add(char.lower())

    return letters

def get_words(words_file):
    with open("src/{}".format(words_file), 'r') as file:
        words = set()
        for line in file:
            words.add("".join(c.lower() for c in line.strip()))

    return words

def parser(crossword_file, words_file):
    # Read the file
    with open("src/{}".format(crossword_file), 'r') as file:
        matrix = [[char for char in line.strip()] for line in file.readlines()]

    lines, slots = parse_lines(matrix, "L")

    # The columns - Switch indicies
    matrix = np.matrix(matrix)
    matrix = matrix.transpose()
    matrix = matrix.getA()

    columns, _slots = parse_lines(matrix, "C")

    letters = get_letters(words_file)
    words = get_words(words_file)

    return lines, columns, slots, letters, words

def print_sol(sol, filename):
    screen = []
    with open("src/{}".format(filename), 'r') as file:
        for i, line in enumerate(file):
            l = []
            for j, char in enumerate(line.strip()):
                if char == "#":
                    l.append("#")
                else:
                    l.append(sol["-".join([str(i), str(j)])])
            screen.append(l)

    return screen

def run():
    """ Main function
    Parse a file containing a crossword puzzle and an words file to find a possible solution
    Unary constraints are set on every slot => must equal one of the available letters
    Unary constraints are set on every space => must be one of the words with the same length
    """
    lines, columns, slots, letters, words = parser("crossword2.txt", "words2.txt")
    total = lines
    total.extend(columns) # Add the columns at the end
    # Set the variables
    var_1 = {"-".join([str(x), str(y)]): set(letters) for (x, y) in slots} # Letters
    var_2 = {"-".join([str(line[0]), str(line[1]), str(line[2]), str(line[3])]): \
        set(word for word in words if len(word) == line[2] - line[1] + 1) \
        for line in total} # Words
    var = dict(var_1, **var_2) # Unary constraints
    # Create solver for those constraints
    P = constraint_programming(var)

    for space in total:
        length = space[2] - space[1] + 1
        for letter in range(length):
            if space[3] == "L":
                P.addConstraint(
                    "-".join([str(space[0]), str(space[1]), str(space[2]), str(space[3])]), \
                    "-".join([str(space[0]), str(space[1] + letter)]), \
                    set((word, word[letter]) for word in words if len(word) == length)
                )
            else:
                P.addConstraint(
                    "-".join([str(space[0]), str(space[1]), str(space[2]), str(space[3])]), \
                    "-".join([str(space[1] + letter), str(space[0])]), \
                    set((word, word[letter]) for word in words if len(word) == length)
                )

    SOL = P.solve()

    if SOL:
        # Small loop to display the solution
        screen = print_sol(SOL, "crossword2.txt")
        for line in screen:
            print("".join(line))
    else:
        print("No solution")


if __name__ == "__main__":
    t0 = time.time()
    run()
    t1 = time.time()
    print("Completed in {}s".format(round(t1 - t0, 3)))