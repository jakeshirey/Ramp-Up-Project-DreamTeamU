import random

class Cipher:
    letter_keys = {
    0 : "A", 1 : "B", 2 : "C", 3 : "D", 4 : "E", 5 : "F",
    6 : "G", 7 : "H", 8 : "I", 9 : "J", 10: "K", 11: "L",
    12: "M", 13: "N", 14: "O", 15: "P", 16: "Q", 17: "R",
    18: "S", 19: "T", 20: "U", 21: "V", 22: "W", 23: "X",
    24: "Y", 25: "Z", 26: "0", 27: "1", 28: "2", 29: "3",
    30: "4", 31: "5", 32: "6", 33: "7", 34: "8", 35: "9"
    }

    def __init__(self, affine_coeff, affine_const):
        self.affine_coeff = affine_coeff
        self.affine_const = affine_const

        #Create character map for random layer
        self.shuffler = []
        for i in Cipher.letter_keys:
            self.shuffler.append(i)
        random.shuffle(self.shuffler)
        self.random_mapping = {}
        for i in Cipher.letter_keys:
            self.random_mapping[Cipher.letter_keys[i]] = Cipher.letter_keys[self.shuffler[i]]

        #Create character map for affine layer
        self.affine_mapping = {}
        for i in Cipher.letter_keys:
            self.affine_mapping[Cipher.letter_keys[i]] = Cipher.letter_keys[(affine_coeff * i + affine_const) % 36]

        #Create reverse mappings for encryption layers for decryption (swapping works as it is one-to-one)
        self.reverse_affine_mapping = dict([(value, key) for key, value in self.affine_mapping.items()])
        self.reverse_random_mapping = dict([(value, key) for key, value in self.random_mapping.items()])


    def encrypt_random_layer(self, message):
        message = message.upper()
        ciphertext = ""
        for character in message:
            if (character.isalnum()):
                character = self.random_mapping[character]
            ciphertext += character
        return ciphertext

    def encrypt_affine_layer(self, message):
        message = message.upper()
        ciphertext = ""
        for character in message:
            if (character.isalnum()):
                character = self.affine_mapping[character]
            ciphertext += character
        return ciphertext

    def reset_random_layer(self):
        random.shuffle(self.shuffler)
        self.random_mapping.clear()
        for i in Cipher.letter_keys:
            self.random_mapping[Cipher.letter_keys[i]] = Cipher.letter_keys[self.shuffler[i]]
        self.reverse_random_mapping.clear()
        self.reverse_random_mapping = dict([(value, key) for key, value in self.random_mapping.items()])
    
    def decrypt_affine_layer(self, message):
        message = message.upper()
        plaintext = ""
        for character in message:
            if (character.isalnum()):
                character = self.reverse_affine_mapping[character]
            plaintext += character
        return plaintext
    
    def decrypt_random_layer(self, message):
        message = message.upper()
        plaintext = ""
        for character in message:
            if (character.isalnum()):
                character = self.reverse_random_mapping[character]
            plaintext += character
        return plaintext

    def encrypt(self, message):
        message = self.encrypt_random_layer(message)
        message = self.encrypt_affine_layer(message)
        return message

    def decrypt(self, message):
        #Must go in reverse order of encryption layers, capitalization of original message is lost
        message = self.decrypt_affine_layer(message)
        message = self.decrypt_random_layer(message)
        return message

#Main Method
coeff = input("Enter an affine transformation coefficient:")
constant = input("Enter an affine transformation constant:")
cphr = Cipher(int(coeff), int(constant))
command = ""
while(command != "quit"):
    command = input("Enter a command. Options: encrypt, decrypt, reset, properties, quit: ")

    if command == "encrypt":
        message = input("Enter a message to encrypt.")
        message = cphr.encrypt(message)
        print("Encrypted message is: ")
        print(message)
    elif command == "decrypt":
        message = input("Enter a message to decrypt.")
        message = cphr.decrypt(message)
        print("Decrypted message is: ")
        print(message)
    elif command == "reset":
        print("Resetting random layer.")
        cphr.reset_random_layer()
    elif command == "properties":
        print("Cipher properties are as follows:")
        print("Random Layer Map: ")
        print(cphr.random_mapping)
        print("Random Layer Reverse Map:")
        print(cphr.reverse_random_mapping)
        print("Affine Map:")
        print(cphr.affine_mapping)
        print("Affine Layer Reverse Mapping")
        print(cphr.reverse_affine_mapping)
    elif command == "quit":
        print("Ending task.")
    else:
        print("Invalid command. Please try again.")
