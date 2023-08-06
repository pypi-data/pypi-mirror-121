def implies(x: any, y: any) -> bool:
    """
    Computes the implication of x to y (x => y).

    Logic table is the following one:

    x | y | x=>y
    ------------
    F | F | V
    F | V | V
    V | F | F
    V | V | V

    :param x: antecendet
    :param y: consequent
    :return: true if x implies y, false otherwise
    """
    return (not(bool(x))) or (bool(y))
