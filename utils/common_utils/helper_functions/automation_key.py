from cryptography.fernet import Fernet

from default_config import KEY


def encrypt_pass(text):
    msg = text
    msg = msg.encode()
    fernet = Fernet(KEY)
    ciphertext = fernet.encrypt(msg).decode()
    print(ciphertext)
    return ciphertext


def get_pass(ciphertext):
    fernet = Fernet(KEY)
    if type(ciphertext) is not bytes:
        clear_text = fernet.decrypt(bytes(ciphertext, "utf-8"))
    else:
        clear_text = fernet.decrypt(ciphertext)
    clear_text = clear_text.decode()
    return clear_text


def generate_new_key():
    key = Fernet.generate_key()
    # Store the file to disk to be accessed for en/de:crypting later.
    with open("secret.key", "wb") as new_key_file:
        new_key_file.write(key)
    print(key)
