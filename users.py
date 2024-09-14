import json
import secrets

# Const
CREDENTIALS_FILE = 'data/creds.json'
TOKEN_FILE = 'data/tokens.json'
AUTH_USERS_FILE = 'data/allowedUsers.txt'
WAIT_LIST_FILE = 'data/accessrequests.txt'
CSRF_TOK_FILE = 'data/CSRF_TOK_FILE.json'

# Get all users
def getCreds():
    try:
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    except:
        print("error opening creds")
    return {}


# Save users to JSON file ** Make sure to save the entire thing
def save_credentials(credentials):
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(credentials, f)


# Create a new user
def createUser(user_name, user_password):
   
    # Get Current users
    current_users = getCreds()
    # Check if user already exists
    if user_name in current_users:
        return "User already exists."
    else:
        current_users[user_name] = user_password
        save_credentials(current_users)
        return "User successfully registered. You may now sign-in!"
    

# Get all auth tokens
def getTokens():
    try:
        with open(TOKEN_FILE, "r") as file:
            return json.load(file)
    except:
        print("error opening tokens")
    return {}
    
# Create an auth tokens for the login user
def createToken(username):
    tokens = getTokens()
    new_token = secrets.token_hex(32)
    tokens[new_token] = username
    with open(TOKEN_FILE, 'w') as f:
        json.dump(tokens, f)
    return new_token

# Get all csrf tokens
def getCSRFTokens():
    try:
        with open(CSRF_TOK_FILE, "r") as file:
            return json.load(file)
    except:
        print("error opening tokens")
    return {}


# Create new csrf token when user logs in
def createCSRFToken(username):
    tokens = getCSRFTokens()
    new_token = secrets.token_hex(32)
    tokens[username] = new_token
    with open(CSRF_TOK_FILE, 'w') as f:
        json.dump(tokens, f)
    return new_token

# get the username associated with a csrf token
def getUserForCsrfTok(csrftok):
    tokens = getCSRFTokens()
    for user,user_tok in tokens.items():
        if user_tok == csrftok:
            return user
        return False

# check if the user of the csrf token = the user of the auth token
def checkCsrfToken(token, csrfTok):
    if token and csrfTok:
        tokens = getTokens()
        if getUserForCsrfTok(csrfTok) == tokens[token]:
            return True
    return False

# Retreive the users who can access the class from the data
def getAllowedUsers():
    allowedUsers = []
    try:
        with open(AUTH_USERS_FILE, "r") as file:
            for user in file.read().splitlines():
                allowedUsers.append(user)
            return allowedUsers
    except:
        print("error opening allowed users")
    

# Get the csrf token of a loggend in user
def getcsrftok(token):
    tokens = getTokens()
    if token in tokens:
        username = tokens[token]
        csrftoks = getCSRFTokens()
        csrftok = csrftoks[username]
        return csrftok
    else:
        return None

# Login the user
def login(user_name, user_password, token):
    users = getCreds()
    if token:
        return 0
    elif user_name in users and users[user_name] == user_password:
            token = createToken(user_name)
            createCSRFToken(user_name)
            print(user_name, "just logged in.")
            return token
    else:
        return 1
    

# check if a user as access to the class via their tokens
def checkAccessToClass(token):
    allowedusers = getAllowedUsers()
    tokens = getTokens()
    if token in tokens:
        user = tokens[token]
        if user in allowedusers:
            return True
        else:
            return False

    else: 
        return False
    

# check if the user is the teacher
def isTeacher(token):
    tokens = getTokens()
    if token in tokens:
        user = tokens[token]
        if user.lower() == "teacher":
            return True, user.lower()
        else:
            return False, user.lower()

    else: 
        return False, "foo"


# destroy tokens
def logout(token):
    if not token:
        return
    tokens = getTokens()
    csrftokens = getCSRFTokens()
    if token in tokens:
        username = tokens[token]
    else:
        return
    print(username)
    csrftok = csrftokens[username]
    print(csrftok)
    if token in tokens:
        del tokens[token]
        del csrftokens[username]
        with open(TOKEN_FILE, 'w') as f:
            json.dump(tokens, f)
        with open(CSRF_TOK_FILE, 'w') as file:
            json.dump(csrftokens, file)
        print("Tokens successfully removed")
    else:
        print("Token doesn't exist")


# add a user to the wait list for the class
def add_user_to_wait_list(token):
    tokens = getTokens()
    waitingUsers = getWaitingUsers()
    allowedUsers = getAllowedUsers()
    if token in tokens:
        username = tokens[token]
        if username in waitingUsers:
            return "You already asked for access to the classroom."
        elif username in allowedUsers:
            return "You are already allowed"
        else:
            addUserToWait(username)
            return "Request made successfuly."

    else:
        return "You must loggin first."
    

# retreive all the pending users
def getWaitingUsers():
    waitingUsers = []
    try:
        with open(WAIT_LIST_FILE, "r") as file:
            for user in file.read().splitlines():
                waitingUsers.append(user)
            return waitingUsers
    except:
        print("error opening waiting users")

# Add the user to the wait list
def addUserToWait(username):
    waitingUsers = getWaitingUsers()
    waitingUsers.append(username)
    try:
        with open(WAIT_LIST_FILE, "w") as file:
            for user in waitingUsers:
                file.write(user + '\n')
            return
    except:
        print("error writing to waiting users")


# aadd and remove user from the apropriate files so he is in the class
def addUserToApproved(username):
    approuvedUsers = getAllowedUsers()
    waitingUsers = getWaitingUsers()
    if username in  waitingUsers:
        waitingUsers.remove(username)

    if username in approuvedUsers:
        return "Users is already approuved."
    else:
        approuvedUsers.append(username)
        with open(AUTH_USERS_FILE, "w") as approuvedlist:
            for user in approuvedUsers:
                approuvedlist.write(user + '\n')
        with open(WAIT_LIST_FILE, "w") as waitlist:
            for user in waitingUsers:
                waitlist.write(user + '\n')


# remove the username from the wait list
def removeUserFromWait(username):
    waitingUsers = getWaitingUsers()
    if username in waitingUsers:
        waitingUsers.remove(username)
        with open(WAIT_LIST_FILE, "w") as waitlist:
            for user in waitingUsers:
                waitlist.write(user + '\n')
        return "user denied"
    else:
        return "User is not in waiting list"