from arranger import arithmetic_arranger

raw_problems = input("Type your problems, if you're typing several at once separate them with commas: \n")

problems = raw_problems.replace(" ", "").split(",")

while True:
    show_answers = input("Can the aswers to your problems be shown? (yes/no): \n")

    if show_answers == "yes":
        print(arithmetic_arranger(problems, True))
        break

    elif show_answers == "no":
        print(arithmetic_arranger(problems, False))
        break

    else:
        print("Invalid Operator.")
