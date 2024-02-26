from Crypto.Cipher import Blowfish
from Crypto.Hash import SHA256
import bcrypt
import sys

FISHERMAN = "fisherman"
FISHERMAN_PASSWORD = "REDACTED"
userhashes = []
encryptedmessages = {}

def send(msg):
    sys.stdout.write(msg+'\n')
    sys.stdout.flush()

def receive():
    sys.stdout.write(">>> ")
    sys.stdout.flush()
    return sys.stdin.readline().strip()

def exiting():
    send("One fish, two fish, three fish, four, five fish, six fish, seven fish more...")
    send("Please do not fish here, this is my lake! Go somewhere else!")
    send("Bye!")
    exit(1)

def encrypt(username, secret):
    blowfish = Blowfish.new(username, Blowfish.MODE_CTR, nonce=b'', initial_value=0)
    ct = blowfish.encrypt(secret)
    return ct

def encryptsecrets(username, secret):
    global encryptedmessages
    if (len(secret) == 0 or len(secret) > 2048):
        send("The secret is too long or too short!")
        exiting()
    if (username in encryptedmessages and len(encryptedmessages[username]) == 10):
        send("You cannot store more than 10 secrets!")
        exiting()
    encryptedsecret = encrypt(username.encode('utf-8'), secret.encode('utf-8'))
    if (username in encryptedmessages):
        encryptedmessages[username].append(encryptedsecret)
    else:
        encryptedmessages[username] = [encryptedsecret]

def getencryptedsecrets(username):
    if username not in encryptedmessages:
        send("You have 0 encrypted messages!")
        return
    send("You have "+str(len(encryptedmessages[username]))+" encrypted messages!")
    i = 1
    for encrypted in encryptedmessages[username]:
        send(str(i)+". encrypted message")
        send(encrypted.hex())
        i += 1
    send("")

def getdecryptedsecrets(username):
    send("This feature is not yet implemented!")
    send("")

def loggedinmenu(username):
    if (username == FISHERMAN):
        send("Welcome Mister Fisherman!")
    while True:
        send("Choose one of the followings:")
        send("1 - Encrypt secret messages")
        send("2 - Get encrypted secret messages")
        send("3 - Get decrypted secret messages")
        send("4 - Logout")
        choice = receive()
        if (choice == "1"):
            send("Give some secret the store!")
            secret = receive()
            encryptsecrets(username, secret)
            send("")
        elif (choice == "2"):
            getencryptedsecrets(username)
        elif (choice == "3"):
            getdecryptedsecrets(username)
        elif (choice == "4"):
            return
        else:
            send("Invalid choice!")
            exiting()

def login():
    send("Give me your username!")
    username = receive()
    if (len(username) < 4 or len(username) > 50):
        send("Username length is not in range!")
        exiting()
    send("Give me your password!")
    password = receive()
    if (len(password) == 0 or len(password) > 50):
        send("Password length is not in range!")
        exiting()
    sha256 = SHA256.new()
    sha256.update(username.encode('utf-8'))
    sha256.update(password.encode('utf-8'))
    loginhash = sha256.hexdigest().encode('utf-8')
    for userhash in userhashes:
        if (bcrypt.checkpw(loginhash, userhash)):
            send("")
            loggedinmenu(username)
            send("")
            return
    exiting()

def register():
    send("Choose a username!")
    username = receive()
    if (username == FISHERMAN):
        send("Fisherman is already a registered user!")
        exiting()
    if (len(username) < 4 or len(username) > 50):
        send("Username length is not in range!")
        exiting()
    send("Choose a password!")
    password = receive()
    if (len(password) == 0 or len(password) > 50):
        send("Password length is not in range!")
        exiting()
    sha256 = SHA256.new()
    sha256.update(username.encode('utf-8'))
    sha256.update(password.encode('utf-8'))

    pwhash = bcrypt.hashpw(sha256.hexdigest().encode('utf-8'), bcrypt.gensalt())
    global userhashes
    userhashes.append(pwhash)
    send("User '"+username+"' registered with password '"+password+"'!")
    send("")

def mainmenu():
    send("Welcome!")
    while True:
        send("Choose one of the followings:")
        send("1 - Login")
        send("2 - Register")
        send("3 - Exit")
        choice = receive()
        if (choice == "1"):
            login()
        elif (choice == "2"):
            register()
        elif (choice == "3"):
            send("Bye!")
            exit(1)
        else:
            exiting()

def initialize():
    sha256 = SHA256.new()
    sha256.update(FISHERMAN.encode('utf-8'))
    sha256.update(FISHERMAN_PASSWORD.encode('utf-8'))
    pwhash = bcrypt.hashpw(sha256.hexdigest().encode('utf-8'), bcrypt.gensalt())
    global userhashes
    userhashes.append(pwhash)
    flag = open("flag.txt", "r").read()
    encryptsecrets(FISHERMAN, flag)

if __name__=="__main__":
    initialize()
    mainmenu()

