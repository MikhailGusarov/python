vowels = ['a', 'e', 'i', 'o', 'u']
found = []
word = input("Provide a word to search for vowels: ")
for letter in word:
    if letter in vowels and letter not in found:
        found.append(letter)
for vowel in found:
    print(vowel)
            
