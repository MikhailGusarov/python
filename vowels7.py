vowels = {'a', 'e', 'i', 'o', 'u'}
word = input("Provide a word to search for vowels: ")
rez = vowels.intersection(set(word))
for i in rez:
    print(i)
