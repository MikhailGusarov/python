def search4vowels(phrase: str) -> set:
    """Возвращает гласные, найденные во введенном слове"""
    vowels = set('aoiue')
    return vowels.intersection(set(phrase))


def search4letters(phrase: str, letters: str = 'aeiou') -> set:
    """Возвращает буквы из второго параметра,
найденные в фразе из первого параметра"""
    return set(letters).intersection(set(phrase))
