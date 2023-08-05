import functools


def is_perfect_number_imperative(number):
    if number < 2:
        return False

    sumOfFactor = 0;
    for iterator in range(1, number + 1):
        if number % iterator == 0:
            sumOfFactor += iterator

    return bool(sumOfFactor == number * 2)


def is_perfect_number_functional(number):
    return number > 1 and sum(set(functools.reduce(list.__add__, ([i, number // i] for i in range(1, number) if number % i == 0)))) == number * 2
