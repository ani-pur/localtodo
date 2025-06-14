import json
import werkzeug.security

#loads file contents 
def load_users(): 
    with open('users.json','r') as file:
        return json.load(file) 

# verify login by checking INPUT PASSWORD hash against stored hashes, returns username correlated to matched hash
def verify_login(input_pass):   
    users=load_users()      #loads users from users.json
    for username, stored_hash in users.items(): 
        if werkzeug.security.check_password_hash(stored_hash,input_pass):       #check for hash match
            return username     #return matching username, else return None
    return None

