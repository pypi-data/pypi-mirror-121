def series(*args):
    result = 0
    for number in args:
        if number > 0:
            result += number
        else:
            raise ValueError("Please make sure you've entered positive values for your resistors."
                             )
    return result


def parallel(*args):
    result = 0
    for number in args:
        if number > 0:
            result += 1 / number
        else:
            raise ValueError("Please make sure you've entered positive values for your resistors."
                             )
    return 1 / result
