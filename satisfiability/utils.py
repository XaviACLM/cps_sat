from itertools import chain, repeat

def iter_repeat(items, multiplicity):
    """
    takes two iterables, "multiplicity" having integer elements, and generates the items in "items", each repeated
    as many times as indicated by the corresponding element in "multiplicity"

    Ex: repeat("abc",[1,4,2]) -> "abbbbcc"
    """
    yield from chain(*map(repeat, items, multiplicity))
