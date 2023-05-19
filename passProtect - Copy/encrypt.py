from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Using to obtain encryption key
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import hashlib
cred = credentials.Certificate(r'path_to_json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

def hash_data(data: bytes): # data in bytes
    hex_hash = data.hex()
    return hex_hash

def byte_data(hashData: str, byteData: bytes):
    byte_hash = byteData.fromhex(hashData)
    return byte_hash

def get_key():
    doc_ref = db.collection('authenticator').document('spoof')
    spoof_data = doc_ref.get().to_dict()
    int_key = spoof_data['goose'] # int value of key
    key = bytes(int_key)
    return key

def encyrpt(plain_text, key):
    # Using AES Encryption to encrypt plain_text
    cipher = AES.new(key, AES.MODE_CBC)
    cipher_text = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
    iv = cipher.iv
    return iv + cipher_text
    
def decrypt(cipher_text, key):
    #Decrypts the given cipher text using AES decryption.
    iv = cipher_text[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_text = unpad(cipher.decrypt(cipher_text[AES.block_size:]), AES.block_size)
    return decrypted_text.decode()

'''
Original -> Hash (How it is in database)

When viewing in accountDisplay():
1. obtain all accounts in collection('accounts)
2. convert all hashed accounts into bytes using byte_data()
3. convert byte converted accounts to readables by using decrypt()

'''

def view_accounts():
    acc_index = []
    acc_ref = db.collection('accounts')
    docs = acc_ref.stream()
    for doc in docs:
        hashed_account = doc.id
        byte_account = byte_data(hashed_account, get_key())
        account = decrypt(byte_account, get_key())
        acc_index.append((account, hashed_account))
    return acc_index
    #return acc_index, 

#accounts = view_accounts() # list of accounts + hashed accounts
#name_path = accounts[0][0][0]
#hash_path = accounts[0][0][1]
#print(name_path, hash_path)
''' 
view_accounts() >>>
What I have: [('account1', '1dfggfsdbfsb567'),('account1', '1dfggfsdbfsb567')] ect

'''



account = 'john cena'
#print(view_accounts()[0])
'''for x in range(len(view_accounts())):
    # x -> 0,1 [0,1]
    accs = view_accounts()[x][0] # retrieving names for all accounts (no hash)
    if account == accs:
        #print(view_accounts()[x])
        name = accs
        hash = view_accounts()[x][1]
        #print(name, hash)
'''
def view_account_data(account):
    # return acc_hash, acc_name, acc user/email/pass
    acc_list = []
    for x in range(len(view_accounts())):
        # x -> 0,1 [0,1]
        accs = view_accounts()[x][0] # retrieving names for all accounts (no hash)
        if account == accs:
            #print(view_accounts()[x])
            name = accs
            hash = view_accounts()[x][1]
    acc_list.append(name)
    acc_list.append(hash)
    account_name = acc_list[0] # account name
    account_hash = acc_list[1] # account hash
    '''
    1. convert all data to bytes
    2. decrypt data
    '''
    doc_ref = db.collection('accounts').document(account_hash)
    acc = doc_ref.get().to_dict()
    user = acc['username']
    pword = acc['password']
    mail = acc['email']
    #1 hash -> bytes
    b_username = byte_data(user, get_key())
    b_password = byte_data(pword, get_key())
    b_email = byte_data(mail, get_key())
    #2 bytes -> words
    username = decrypt(b_username, get_key())
    password = decrypt(b_password, get_key())
    email = decrypt(b_email, get_key())


    return account_name, account_hash, username, password, email
    #          [0]           [1]          [2]      [3]        [4]


    
    

#view_account_data(account)
