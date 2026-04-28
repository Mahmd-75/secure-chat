def cesar_encrypt(message, key):
    """Chiffre un message avec le chiffre de César"""
    result = ""
    for char in message:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + key) % 26 + base)
        else:
            result += char
    return result

def cesar_decrypt(message, key):
    return cesar_encrypt(message, -key)

def vigenere_encrypt(message, key):
    """Chiffre un message avec le chiffre de Vigenère (clé alphabétique)"""
    result = ""
    key = key.lower()
    key_index = 0
    for char in message:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_index % len(key)]) - ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
            key_index += 1
        else:
            result += char
    return result

def vigenere_decrypt(message, key):
    """Déchiffre un message chiffré par Vigenère"""
    result = ""
    key = key.lower()
    key_index = 0
    for char in message:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_index % len(key)]) - ord('a')
            result += chr((ord(char) - base - shift) % 26 + base)
            key_index += 1
        else:
            result += char
    return result
