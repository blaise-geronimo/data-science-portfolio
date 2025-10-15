
positive_examples = [([1, 2, 3], 2), ([4, 5, 6], 5)]
negative_examples = [([1, 2, 3], 5), ([4, 5, 6], 1)]


def is_member(x, lst):
    return x in lst  # Learned rule


# Positive Examples: Words that should be SHIFTED
shift_examples = [
    ('the', 'SHIFT'),   # Determiners should be shifted
    ('a', 'SHIFT'),
    ('cat', 'SHIFT'),   # Nouns should be shifted initially
    ('fish', 'SHIFT'),
    ('eats', 'SHIFT'),  # Verbs should also be shifted
    ('runs', 'SHIFT')
]

# Negative Examples: Combinations that should be REDUCED
reduce_examples = [
    (('the', 'cat'), 'REDUCE'),  # Determiner + Noun → NP
    (('a', 'fish'), 'REDUCE'),
    (('NP', 'eats'), 'REDUCE'),  # NP + Verb → VP
    (('NP', 'VP'), 'REDUCE'),      # NP + VP → S
    (('Verb'), 'REDUCE')
]


def isdeterminer():
    return True


def isnoun():
    return True


# decides if a word should be shifted based on learned ILP rules.
def should_shift(word, stack):
    # Determiners should always be shifted
    if word.isdet:
        return True
    # nouns should only shift if the stack does NOT already contain an NP

    if word.isnoun and 'NP' not in stack:
        return True

    # verbs should shift if there is already an NP in the stack (so it can form a VP)
    if word.isverb and 'NP' in stack:
        return True

    return False  # Default case: Do not shift if conditions aren’t met


# decides if the top of the stack should be reduced based on ILP rules.
def should_reduce(stack):
    if len(stack) < 2:
        return False  # need at least two elements to reduce anything

    if stack[-1].isverb:
        return True, 'Verb'

    # Rule: Determiner + Noun → NP
    elif (stack[-2], stack[-1]) == ('Det', 'Noun'):
        return True, 'NP'

    # Rule: NP + Verb → VP
    elif (stack[-2], stack[-1]) == ('Verb', 'NP'):
        return True, 'VP'

    # Rule: NP + VP → S (Final Sentence)
    elif (stack[-2], stack[-1]) == ('NP', 'VP'):
        return True, 'S'

    return False  # Default case: No reduction possible

