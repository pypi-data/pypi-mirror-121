import perfectCal.perfectNumCalculator

def test_negativeinteger_not_perfect():
    assert (perfectCal.perfectNumCalculator.is_perfect_number_imperative(-1) and \
            perfectCal.perfectNumCalculator.is_perfect_number_functional(-1)) == False
    assert (perfectCal.perfectNumCalculator.is_perfect_number_imperative(-6) and \
            perfectCal.perfectNumCalculator.is_perfect_number_functional(-6)) == False


def test_positiveinteger_not_perfect():
    assert (perfectCal.perfectNumCalculator.is_perfect_number_imperative(0) and \
            perfectCal.perfectNumCalculator.is_perfect_number_functional(0)) == False
    assert (perfectCal.perfectNumCalculator.is_perfect_number_imperative(1) and \
            perfectCal.perfectNumCalculator.is_perfect_number_functional(1)) == False
    assert (perfectCal.perfectNumCalculator.is_perfect_number_imperative(10) and \
            perfectCal.perfectNumCalculator.is_perfect_number_functional(-10)) == False


def test_positiveinteger_perfect():
    assert (perfectCal.perfectNumCalculator.is_perfect_number_imperative(6) and \
            perfectCal.perfectNumCalculator.is_perfect_number_functional(6)) == True
    assert (perfectCal.perfectNumCalculator.is_perfect_number_imperative(28) and \
            perfectCal.perfectNumCalculator.is_perfect_number_functional(28)) == True

