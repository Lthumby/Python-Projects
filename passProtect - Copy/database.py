import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import time
import subprocess


# encryption
import encrypt
import view_center
#import main

# Database initialization
cred = credentials.Certificate(r'path_to_json_file_firebase')

#app = firebase_admin.initialize_app(cred)

db = firestore.client()

key = encrypt.get_key()

'''doc_ref = db.collection('authenticator').document('spoof')
doc_ref.set({
        'goose': key
    })
'''
def accInputs():
    account = input("\n\n\n\nEnter Name of Account <: ")
    username = input("Enter Username <: ")
    email = input("Enter Email <: ")
    password = input("Enter Password <: ")
    
    # encrypting data
    '''
    1. Encrypt data using AES Encryption, encrypt(string, key) <- store in var
    2. Hash the bytes by using hex(), ex. hex_hash = ^.hex()
    * store hash into database
    '''
    acc = encrypt.encyrpt(account, key).hex()
    user = encrypt.encyrpt(username, key).hex()
    mail = encrypt.encyrpt(email, key).hex()
    pword = encrypt.encyrpt(password, key).hex()
    
    return acc, user, mail, pword

def addInfo():
    # follow 3 step hasing to pass to db
    userData = accInputs()
    account = userData[0]
    username = userData[1]
    email = userData[2]
    password = userData[3]

    #print(account, type(account))

    doc_ref = db.collection('accounts').document(account)
    doc_ref.set({
        'username':username,
        'email':email,
        'password':password,
    })


def accountDisplay():
    subprocess.call("cls", shell=True)
    count = 0
    acc_index = []
    users_ref = db.collection('accounts')
    docs = users_ref.stream()
    for doc in docs:
        count+=1
        hashed_account = doc.id
        byte_account = encrypt.byte_data(hashed_account, key)
        account = encrypt.decrypt(byte_account, key)
        acc_index.append(account)
        
        print(f"{count}. {account}")
        #print(doc.to_dict())

    account_select = input('Enter name of account <: ')

    if account_select == "":
        print("\n\nGOING BACK...")
        time.sleep(0.5)
        view_center.viewCenter(access=True)
    elif account_select not in acc_index:
        print("\n\nINVALID ENTRY, GOING BACK")
        time.sleep(0.5)
        view_center.viewCenter(access=True)
    try:
        acc_data = encrypt.view_account_data(account_select)
        acc_name = acc_data[0]
        acc_hash = acc_data[1]
    except :
        print("ValueError")
        print("\n\nGOING BACK...")
        time.sleep(0.5)
        view_center.viewCenter(access=True)

    '''if account_select == acc_name:
        account_select = acc_hash'''
    
    try:
        subprocess.call("cls", shell=True)
        
        user = acc_data[2]
        pword = acc_data[3]
        email = acc_data[4]
        print(f'''
    -------------------------
    | | | {acc_name} | |
    | 
    | *USERNAME: {user}
    | *PASSWORD: {pword}
    | *EMAIL: {email}
    | 
    | | | | | | | | | | | | | 
        ''')
        back = input("Hit ENTER to go back...")
        if back == '':
            accountDisplay()
        else:
            print("NOPE")
    except:
        pass

def auth():
    
    golden_gate = False
    while golden_gate == False:
        subprocess.call("cls", shell=True)
        
        username = input("Enter Username <: ")
        password = input("Enter Password <: ")
        # accessing token
        
        doc_ref = db.collection('authenticator').document('golden_ticket')
        doc = doc_ref.get()
        doc_data = doc.to_dict()
        admin_user = doc_data['username']
        admin_pass = doc_data['key']
        if doc.exists:
            data = str(doc.to_dict())
        if username == admin_user and password == admin_pass:
            golden_gate = True
            return golden_gate 
        else:
            print("WRONG PASSWORD")
            time.sleep(0.5)
            golden_gate = False
    #return golden_gate
