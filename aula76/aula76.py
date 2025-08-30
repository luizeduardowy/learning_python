secret_word = 'codigo'
i = 0

wrong_qty = 0
correct_qty = 0
word_discovered = ''

while i < len(secret_word):
    word_discovered += '*'
    i += 1

while word_discovered != secret_word:
    letter = input('Digite uma letra: ')

    if letter not in secret_word:
        wrong_qty  += 1
        print('Letra errada')
        print('palavra descoberta --> ' + word_discovered)

    else:
        correct_qty += 1
        print('Letra certa')
        i = 0
        while i < len(secret_word):
            if secret_word[i] == letter:
                # word_discovered[i] = letter
                word_discovered = list(word_discovered)
                word_discovered[i] = letter
                word_discovered = "".join(word_discovered)
            i += 1
        print('palavra descoberta --> ' + word_discovered)

print('Parabens a palavra era ' + secret_word)
print('Você errou ' + str(wrong_qty) + ' vezes')
print('Você acertou a palavra em ' + str(correct_qty + wrong_qty) + ' tentativas')