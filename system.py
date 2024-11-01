import random

class CaesarCipher:
    def __init__(self, key):
        self.key = key
        self.alphabet_ua = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
        self.alphabet_en = 'abcdefghijklmnopqrstuvwxyz'


    def encrypt(self, text, language='ua'):
        # self.validate_key()
        alphabet = self.alphabet_ua if language == 'ua' else self.alphabet_en
        shifted_alphabet = alphabet[self.key % len(alphabet):] + alphabet[:self.key % len(alphabet)]
        table = str.maketrans(alphabet, shifted_alphabet)
        return text.translate(table)

    def decrypt(self, text, language='ua'):
        # self.validate_key()
        alphabet = self.alphabet_ua if language == 'ua' else self.alphabet_en
        shifted_alphabet = alphabet[-self.key % len(alphabet):] + alphabet[:-self.key % len(alphabet)]
        table = str.maketrans(alphabet, shifted_alphabet)
        return text.translate(table)


class TrithemiusCipher:
    def __init__(self, A=0, B=0, C=0, key_phrase=None):
        self.A = A
        self.B = B
        self.C = C
        self.key_phrase = key_phrase
        self.alphabet_ua = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
        self.alphabet_en = 'abcdefghijklmnopqrstuvwxyz'

    def encrypt_linear(self, text, language='ua'):
        # self.validate_coefficients(True)
        alphabet = self.alphabet_ua if language == 'ua' else self.alphabet_en
        encrypted_text = []
        for i, char in enumerate(text):
            if char in alphabet:
                step = self.A + self.B * i
                new_pos = (alphabet.index(char) + step) % len(alphabet)
                encrypted_text.append(alphabet[new_pos])
            else:
                encrypted_text.append(char)
        return ''.join(encrypted_text)

    def decrypt_linear(self, text, language='ua'):
        # self.validate_coefficients(True)
        alphabet = self.alphabet_ua if language == 'ua' else self.alphabet_en
        decrypted_text = []
        for i, char in enumerate(text):
            if char in alphabet:
                step = self.A + self.B * i
                new_pos = (alphabet.index(char) - step) % len(alphabet)
                decrypted_text.append(alphabet[new_pos])
            else:
                decrypted_text.append(char)
        return ''.join(decrypted_text)

    def encrypt_nonlinear(self, text, language='ua'):
        # self.validate_coefficients(False)
        alphabet = self.alphabet_ua if language == 'ua' else self.alphabet_en
        encrypted_text = []
        for i, char in enumerate(text):
            if char in alphabet:
                step = self.A**2 + self.B * i + self.C
                new_pos = (alphabet.index(char) + step) % len(alphabet)
                encrypted_text.append(alphabet[new_pos])
            else:
                encrypted_text.append(char)
        return ''.join(encrypted_text)

    def decrypt_nonlinear(self, text, language='ua'):
        # self.validate_coefficients(False)
        alphabet = self.alphabet_ua if language == 'ua' else self.alphabet_en
        decrypted_text = []
        for i, char in enumerate(text):
            if char in alphabet:
                step = self.A ** 2 + self.B * i + self.C
                new_pos = (alphabet.index(char) - step) % len(alphabet)
                decrypted_text.append(alphabet[new_pos])
            else:
                decrypted_text.append(char)
        return ''.join(decrypted_text)

    def encrypt_key_phrase(self, text, language='ua'):
        alphabet = self.alphabet_ua if language == 'ua' else self.alphabet_en
        key_phrase_repeated = (self.key_phrase * (len(text) // len(self.key_phrase) + 1))[:len(text)]
        encrypted_text = []
        for char, key_char in zip(text, key_phrase_repeated):
            if char in alphabet:
                step = alphabet.index(key_char) + 1
                new_pos = (alphabet.index(char) + step) % len(alphabet)
                encrypted_text.append(alphabet[new_pos])
            else:
                encrypted_text.append(char)
        return ''.join(encrypted_text)

    def decrypt_key_phrase(self, text, language='ua'):
        alphabet = self.alphabet_ua if language == 'ua' else self.alphabet_en
        key_phrase_repeated = (self.key_phrase * (len(text) // len(self.key_phrase) + 1))[:len(text)]
        decrypted_text = []
        for char, key_char in zip(text, key_phrase_repeated):
            if char in alphabet:
                step = alphabet.index(key_char) + 1
                new_pos = (alphabet.index(char) - step) % len(alphabet)
                decrypted_text.append(alphabet[new_pos])
            else:
                decrypted_text.append(char)
        return ''.join(decrypted_text)


class BookCipher:
    def __init__(self, pangram=None, language='ua'):
        self.ua_pangrams = pangram if pangram and language=='ua' else (
            "жебракують філософи при ґанку церкви в гадячі, ще й шатро їхнє п'яне знаємо",
            "є місць багато, ґедзю, де фрукт в’ялий їж і шуми, а хвощ не чіпай",
            "доки ж є чаш цих п’ять, фехтуймо ґречно, юнаки щасливі, за її губи",
            "на подушечці форми любої є й ґудзик щоб пір’я геть жовте сховати"
        )

        self.en_pangrams = pangram if pangram and language=='en' else (
            "the quick brown fox jumps over the lazy dog",
            "pack my box with five dozen liquor jugs",
            "how vexingly quick daft zebras jump",
            "waltz, bad nymph, for quick jigs vex"
        )

        self.language = language
        self.table = self.create_table(language)

    def create_table(self, language):
        # створюємо таблицю 10x10 з панграм (нумеруємо 0-9)
        if language == 'ua':
            pangram_string = ''.join(self.ua_pangrams).replace(' ', '').replace(',', '').replace('’', '').replace('-','')
        else:
            pangram_string = ''.join(self.en_pangrams).replace(' ', '').replace(',', '').replace('’', '').replace('-','')

        while len(pangram_string) < 100:
            pangram_string*=2

        table = [pangram_string[i:i + 10] for i in range(0, 100, 10)]
        return table

    def encrypt(self, text):
        encrypted_text = []
        for char in text:
            positions = [(i, j) for i in range(10) for j in range(10) if self.table[i][j].lower() == char.lower()]
            if positions:
                i, j = random.choice(positions)
                encrypted_text.append(f"{i}/{j}")
            else:
                encrypted_text.append(char)
                # якщо символ не знайдено, лишаємо як є, але бажано використовувати панграми, щоб такого не траплялось
        return ' '.join(encrypted_text)

    def decrypt(self, text):
        decrypted_text = []  # Список для збереження дешифрованих слів
        words = text.split('  ')  # Текст розбивається по пробілах на пари

        for word in words:
            decrypted_word = []  # Тимчасовий список для одного дешифрованого слова
            pairs = word.split()  # Розбиваємо кожну пару на символи

            for pair in pairs:
                if len(pair) == 3 and pair[0].isdigit() and pair[1] == '/' and pair[2].isdigit():
                    i, j = int(pair[0]), int(pair[2])
                    decrypted_word.append(self.table[i][j])  # Додаємо відновлений символ до поточного слова
                else:
                    decrypted_word.append(pair)  # Якщо символ не знайдено, залишаємо його як є

            decrypted_text.append(''.join(decrypted_word))

        return ' '.join(decrypted_text)


