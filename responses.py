import json
from users import *
from grades import *

cache = {}


#### Actions

####### USERS MANAGEMENT

def create_user(username,password):      
    json_message = json.dumps({"message": createUser(username,password)})
    response = f"""\
HTTP/1.1 200 OK
Content-Type: application/json

{json_message}
"""
        
    return response



def login_user(username,password, user_token):      

    token = login(username,password, user_token)
    if token == 1:
        json_message = json.dumps({"message":"Invalid username or password"})
        response = f"""\
HTTP/1.1 200 OK
Content-Type: application/json

{json_message}
"""
    elif token == 0:
        json_message = json.dumps({"message":"You must logout first."})
        response = f"""\
HTTP/1.1 200 OK
Content-Type: application/json

{json_message}
"""
    else:
        json_message = json.dumps({"message": "REDIRECTION"})
        response = f"""\
HTTP/1.1 200 OK
Content-Type: application/json
Set-Cookie: token={token}; SameSite=Strict; HttpOnly

{json_message}
"""
        
    return response



def check_class_access(user_token):      

    access = checkAccessToClass(user_token)
    if access:
        json_message = json.dumps({"message":"REDIRECTION"})
        response = f"""\
HTTP/1.1 200 OK
Content-Type: application/json

{json_message}
"""
    else:
        json_message = json.dumps({"message": "You dont have access to this class!!!"})
        response = f"""\
HTTP/1.1 200 OK
Content-Type: application/json

{json_message}
"""
        
    return response


def log_user_out(token):
    logout(token)
    response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html
Set-Cookie: token=; expires=Thu, 01 Jan 1970 00:00:00 GMT

<script>location = '/';</script>
"""
    return response

def addToWaitList(token):
    message = add_user_to_wait_list(token)
    json_message = json.dumps({"message": message})
    response = f"""\
HTTP/1.1 200 OK
Content-Type: application/json

{json_message}
"""
    return response  


def addUserToClass(userToAdd, token, csrfTok):
    isteach, username = isTeacher(token)
    valcsrftok = checkCsrfToken(token, csrfTok)
    if isteach and valcsrftok:
        addUserToApproved(userToAdd)
        response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html
Set-Cookie: token=; expires=Thu, 01 Jan 1970 00:00:00 GMT

<script>location = '/waitlist';</script>
"""
    else:
        response = f"""\
HTTP/1.1 401 YOU SHALL NOT PASS
Content-Type: text

As user : {username} you cant approve or deny users only user : "teacher" does.
"""
    return response


def removeUserFromWaitList(userToDeny, token, csrfTok):
    isteach, username = isTeacher(token)
    if username == "foo":
        return False
    valcsrftok = checkCsrfToken(token, csrfTok)
    if isteach and valcsrftok:
        removeUserFromWait(userToDeny)
        response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html
Set-Cookie: token=; expires=Thu, 01 Jan 1970 00:00:00 GMT

<script>location = '/waitlist';</script>
"""
    else:
        response = f"""\
HTTP/1.1 401 YOU SHALL NOT PASS
Content-Type: text

As user : {username} you cant approve or deny users only user : "teacher" does.
"""
        

    return response



# return data



 #### HTML
def return_home_page():
    if "home" in cache:
        print("returned cached home")
        return cache["home"]
    try:
        with open("html/index.html", "r") as file:
            html = file.read()

        response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html

{html}
"""
        cache["home"] = response
        return response
    except Exception:
        return False

def return_login_page():
    if "login" in cache:
        print("returned cached login")
        return cache["login"]
    try:
        with open("html/login.html", "r") as file:
            html = file.read()

        response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html

{html}
"""
        cache["login"] = response
        return response
    except Exception:
        return False

def return_class_page(token):
    if checkAccessToClass(token):

        if "class" in cache:
            print("returned cached class")
            return cache["class"]
        try:
            with open("html/class.html", "r") as file:
                html = file.read()

            response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html

{html}
"""
            cache["class"] = response
            return response
        except Exception:
            return False
    else:
        response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html

<script>location = '/login';</script>
"""
        return response


def return_grades_page(token):
    if not token:
        response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html

<script>location = '/login';</script>
"""
        return response
    isteach, username = isTeacher(token)
    if checkAccessToClass(token) and isteach:

        if "grades" in cache:
            print("returned cached grades")
            return cache["grades"]
        try:
            with open("html/grades.html", "r") as file:
                html = file.read()

            response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html

{html}
"""
            cache["grades"] = response
        except Exception:
            return False
            
    else:
        response = f"""\
HTTP/1.1 401 YOU SHALL NOT PASS
Content-Type: text

As user : {username} you dont have access to the grades only user : "teacher" does.
"""
        
    return response
         


def return_waitinglist_page(token):
    if not token:
        response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html

<script>location = '/login';</script>
"""
        return response

    try:
        with open("html/pendinglist.html", "r") as file:
            html = file.read()
        csrftok = getcsrftok(token)
        response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html

{html}
<script>const csrftok = "{csrftok}";</script>
"""
        return response
    except Exception:
        return False



### API

def get_students(token):
    if not token:
        response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html

<script>location = '/login';</script>
"""
        return response

    if checkAccessToClass(token):
        students = getAllowedUsers()
        json_message = json.dumps({"students": students})
    else:
        json_message = json.dumps({"message": "You dont have access to this class!!!"})

    response = f"""\
HTTP/1.1 200 OK
Content-Type: application/json

{json_message}
"""
    return response


def get_grades(token):
    if not token:
        response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html

<script>location = '/login';</script>
"""
        return response
    if checkAccessToClass(token):
        isteach, username = isTeacher(token)
        if isteach:
            grades, success = getGrades()

            json_message = json.dumps(grades)

            if success:
                cookie = "Set-Cookie: success=YayYouChangeVincentsgrade"
            else:
                cookie = ""
        else:
            
            message = f"Your username isint \"teacher\" its {username}."
            json_message = json.dumps({"message": message})
    else:
        json_message = json.dumps({"message": "You dont have access to this class!!!"})

    response = f"""\
HTTP/1.1 200 OK
Content-Type: application/json
{cookie}

{json_message}
"""
    return response


def getWaitList(token):
    if not token:
        response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html

<script>location = '/login';</script>
"""
        return response
    students = getWaitingUsers()

    json_message = json.dumps({"students": students})
    response = f"""\
HTTP/1.1 200 OK
Content-Type: application/json

{json_message}
"""
    return response



### CSS


def serve_css(path):
    if path in cache:
        print(f"returned cached css {path}")
        return cache[path]
    try:
        with open(path, 'r') as f:
            css_content = f.read()

        response =  f"""\
HTTP/1.1 200 OK
Content-Type: text/css

{css_content}
"""
        cache[path] = response
        return response
       
    except FileNotFoundError:
        return """\
HTTP/1.1 404 Not Found
Content-Type: text/html

<html>
    <body>
        <h1>404 - CSS File Not Found weirdo</h1>
    </body>
</html>
"""


