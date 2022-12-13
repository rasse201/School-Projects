def arithmetic_arranger(problems, show_answers):

    # error checking ...

    if len(problems) > 5:
        return "Error: Too many problems. Maximal allowed value is 5."

    operator_count = list(map(lambda x: x.count("+") + x.count("-"), problems))

    for i in operator_count:
        if i != 1:
            return " Error: Operator must be '+' or '-'."

    numbers_only = list(map(lambda x: x.replace("-", "+").split("+"), problems))

    for i in numbers_only:
        if not all(map(lambda x: x.isdigit(), i)):
            return "Error: Numbers must only contain digits."

    for i in numbers_only:
        if not all(map(lambda x: len(x) < 5, i)):
            return "Error: Numbers cannot be more than four digits."

    # done with error checking

    answer_values = list(map(lambda x: str(eval(x)), problems))
    first_row = ""
    second_row = ""
    dashes = ""
    answers = ""

    first_row_numbers = []
    second_row_numbers = []

    for i in numbers_only:
        first_row_numbers.append(i[0])
        second_row_numbers.append(i[1])
        dashes += "--" + "-" * len(max(i)) + "     "
        first_row += "  " + " " * (len(max(i))-len(first_row_numbers[numbers_only.index(i)])) + first_row_numbers[numbers_only.index(i)] + "     "
        if "+" in problems[numbers_only.index(i)]:
            operator = "+"
        else:
           operator = "-"
        second_row += operator + " " * (len(max(i))-len(second_row_numbers[numbers_only.index(i)])+1) + second_row_numbers[numbers_only.index(i)] + "     "
        answers += " " * (len(max(i))-len(answer_values[numbers_only.index(i)])+2) + answer_values[numbers_only.index(i)] + "     "

    if show_answers:
        return '\n'.join((first_row, second_row, dashes, answers))
    else:
        return '\n'.join((first_row, second_row, dashes))



