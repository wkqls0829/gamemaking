

class CaesarCipher:

    def __init__(self):
        self.message_to_return = ""

        self._begin()

    def _begin(self):
        self.mode = input("Do you wish to encrypt or decrypt a message?")
        while self.mode != "encrypt" and self.mode != "decrypt":
            self.mode = input("Please choose between encrypt or decrypt")

        self.message = input("Enter your message:")
        self.key_number = int(input("Enter the key number (1-52)"))
        self.process()
        print("Your Translated text is:")
        print(self.message_to_return)

    def process(self):
        message_list = [ord(m) for m in self.message]
        if self.mode == "encrypt":
            to_add = self.key_number
        else:
            to_add = self.key_number * -1
        for m in message_list:
            if ord('a') <= m <= ord('z'):
                m = (m - ord('a') + to_add) % 26 + ord('a')
            elif ord('A') <= m <= ord('Z'):
                m = (m - ord('A') + to_add) % 26 + ord('A')
            self.message_to_return += str(chr(m))


if __name__ == "__main__":
    CaesarCipher()