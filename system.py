from Crypto.Cipher import DES


class EncryptionDES:
    def __init__(self, mode, key, iv=None):
        self.mode = mode
        self.key = key
        self.iv = iv

    def encrypt(self, plaintext):
        if self.mode == DES.MODE_ECB:
            cipher = DES.new(self.key, self.mode)
        else:
            cipher = DES.new(self.key, self.mode, iv=self.iv)

        padded_text = self.pad(plaintext)
        encrypted = cipher.encrypt(padded_text)

        return (self.iv + encrypted) if self.iv else encrypted

    def decrypt(self, ciphertext):
        if self.mode == DES.MODE_ECB:
            cipher = DES.new(self.key, self.mode)
            decrypted = cipher.decrypt(ciphertext)
        else:
            cipher = DES.new(self.key, self.mode, iv=self.iv)
            decrypted = cipher.decrypt(ciphertext[8:])

        return self.unpad(decrypted)

    @staticmethod
    def pad(text):
        padding_len = 8 - (len(text) % 8)
        return text + bytes([padding_len]) * padding_len

    @staticmethod
    def unpad(text):
        padding_len = text[-1]
        return text[:-padding_len]

