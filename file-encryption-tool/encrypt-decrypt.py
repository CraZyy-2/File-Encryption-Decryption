from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os

def encrypt(file, key):
    cipher = AES.new(key, AES.MODE_CBC)
    with open(file, "rb") as f:
        text = f.read()

    # Pad the text and then encrypt
    ctext = cipher.encrypt(pad(text, AES.block_size))

    # Concatenate IV and ciphertext
    iv = cipher.iv
    return iv + ctext

def decrypt(file, key, ivc):
    iv = ivc[:16]  # The first 16 bytes are the IV
    ctext = ivc[16:]  # The rest is the ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    # Decrypt and unpad the text
    with open(file, "wb") as f:
        text = unpad(cipher.decrypt(ctext), AES.block_size)
        f.write(text)

if __name__ == "__main__":
    # Check for existing key file
    key_file = "key.bin"
    if os.path.exists(key_file):
        with open(key_file, "rb") as kf:
            key = kf.read()
    else:
        key = get_random_bytes(16)  # Generate a new random key
        with open(key_file, "wb") as kf:
            kf.write(key)

    choice = input("If you would like to encrypt, type 'E'; if you would like to decrypt, type 'D': ")
    file = input("Enter the name of the file: ")

    if choice.lower() == "e":
        encrypted = encrypt(file, key)
        with open("encrypted", "wb") as f:
            f.write(encrypted)
        print("File encrypted successfully as 'encrypted'.")

    elif choice.lower() == "d":
        with open("encrypted", "rb") as f:
            encrypted = f.read()
            decrypt("decrypted", key, encrypted)
        print("File decrypted successfully as 'decrypted'.")

    else:
        print("Invalid Choice")
