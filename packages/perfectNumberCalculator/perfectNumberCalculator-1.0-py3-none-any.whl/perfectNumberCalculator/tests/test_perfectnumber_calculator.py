import perfectNumberCalculator.perfectnumber_calculator

def test_negativeinteger_not_perfect():
    assert (perfectNumberCalculator.perfectnumber_calculator.is_perfect_number_imperative(-1) and \
           perfectNumberCalculator.perfectnumber_calculator.is_perfect_number_functional(-1)) == False
    assert (perfectNumberCalculator.perfectnumber_calculator.is_perfect_number_imperative(-6) and \
           perfectNumberCalculator.perfectnumber_calculator.is_perfect_number_functional(-6)) == False


def test_positiveinteger_not_perfect():
    assert (perfectNumberCalculator.perfectnumber_calculator.is_perfect_number_imperative(0) and \
           perfectNumberCalculator.perfectnumber_calculator.is_perfect_number_functional(0)) == False
    assert (perfectNumberCalculator.perfectnumber_calculator.is_perfect_number_imperative(1) and \
           perfectNumberCalculator.perfectnumber_calculator.is_perfect_number_functional(1)) == False
    assert (perfectNumberCalculator.perfectnumber_calculator.is_perfect_number_imperative(10) and \
           perfectNumberCalculator.perfectnumber_calculator.is_perfect_number_functional(-10)) == False


def test_positiveinteger_perfect():
    assert (perfectNumberCalculator.perfectnumber_calculator.is_perfect_number_imperative(6) and \
           perfectNumberCalculator.perfectnumber_calculator.is_perfect_number_functional(6)) == True
    assert (perfectNumberCalculator.perfectnumber_calculator.is_perfect_number_imperative(28) and \
           perfectNumberCalculator.perfectnumber_calculator.is_perfect_number_functional(28)) == True

