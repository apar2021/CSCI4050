#from cryptography.fernet import Fernet

#encryption_key = Fernet.generate_key()

#print(type(encryption_key))
#print(encryption_key)

#aaz = "b'fRz_LtUyI-sqsFffJAa1mPOm9_8h8tLdcVex316VZVQ='"

#encryptor = Fernet(encryption_key)

#encryptor = Fernet(aaz)

# Example dictionary
errors = {"1": "a", "2": "b", "3": "c"}

for error, message in zip(errors.keys(), errors.values()):
    print(error, message)