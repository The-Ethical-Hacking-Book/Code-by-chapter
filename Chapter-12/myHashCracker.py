import hashlib 

def crack_MD5_Hash(hash_to_crack, salt, dictionary_file):
    file = open(dictionary_file, "r")
    for password in file:
        salted_password = (salt + password.strip("\n")).encode('UTF-8')
        if hashlib.md5(salted_password).hexdigest() == hash_to_crack: 
            return password
    return None 

hash_to_crack = 'c94201dbba5cb49dc3a6876a04f15f75'
salt = 'd6a6bc0db10694a2d90e3a69648f3a03'
dict = "/home/kali/Desktop/SecLists/Passwords/darkweb2017-top10000.txt"

password = crack_MD5_Hash(hash_to_crack, salt, dict)
print(password)
