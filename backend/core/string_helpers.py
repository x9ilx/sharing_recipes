LAST_DIGIT = 10
LAST_TWO_DIGIT = 100

NOMINATIVE_CASE = 0
GENITIVE_CASE=  1
DATIVE_CASE = 2

def ru_plural(value, variants):
    variants = variants.split(',')
    value = abs(int(value))

    if value % LAST_DIGIT == 1 and value % LAST_TWO_DIGIT != 11:
        return variants[NOMINATIVE_CASE]

    if (
        value % LAST_DIGIT >= 2
        and value % LAST_DIGIT <= 4
        and (
            value % LAST_TWO_DIGIT < 10 or value % LAST_TWO_DIGIT >= 20
        )
    ):
        return variants[GENITIVE_CASE]

    return variants[DATIVE_CASE]
