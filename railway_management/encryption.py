from cryptography.fernet import Fernet

KEY = b'66Z-GzhWVb9c9RgAChoGvk2q9Vqoc-mdFbCWLJik-d0='

cipher_suite = Fernet(KEY)

def encrypt_data(password):

    encrypt_text = cipher_suite.encrypt(
        password.encode())
    return encrypt_text.decode()

def decrypt_data(encrypted_password):
    decrypted_password = cipher_suite.decrypt(
        encrypted_password).decode()
    return decrypted_password