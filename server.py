import socket
import json
from responses import *
import threading
from urllib.parse import unquote, urlparse, parse_qs

HOST = "127.0.0.1"
#HOST = "192.168.2.57"
PORT = 8081

# The max size of the request 
reqsizemax = 2048

def parse_cookies(headers):
    ##### Returns all cookies
    cookies = {}
    for header in headers:
        if header.startswith("Cookie:"):
            cookie_string = header[len("Cookie:"):].strip()
            for cookie in cookie_string.split(";"):
                try:
                    key, value = cookie.split("=", 1)
                    cookies[key.strip()] = value.strip()
                except:
                    return False
    return cookies


def handclient(connection, addr):
            print(f"Connected by {addr}")
            request = connection.recv(reqsizemax).decode("utf-8", errors="replace")

            #print(f"Request:\n{request}")

            # Check path and method get cookies
            lines = request.split("\r\n")
            request_line = lines[0]
            method, path, _ = request_line.split(" ")

            headers, body = request.split("\r\n\r\n", 1)
            headers = headers.split("\r\n")

            cookies = parse_cookies(headers)

            if cookies == False:
                token = False
            else:
                try:
                    token = cookies.get('token', None)
                except:
                    token = False
            
            # Choose what to serve/do
            match (path,method):
                 ## Actions

                case ("/register", "POST"):
                    try:
                        params = json.loads(body)
                        new_username = params.get('new_username', 0)
                        new_password = params.get('new_password', 0)
                        response = create_user(new_username, new_password)
                    except:
                        response = False


                case ("/login", "POST"):
                    try:
                        params = json.loads(body)
                        username = params.get('username', 0)
                        password = params.get('password', 0)
                        response = login_user(username, password, token)
                    except:
                        response = False


                case ("/checkAccessToClass", "POST"):
                    response = check_class_access(token)

                case ("/logout", "GET"):
                    response = log_user_out(token)

                case ("/requestAccess", "POST"):
                    
                    response = addToWaitList(token)
                case ("/calculateSup3rSecretP4th", "POST"):
                    params = json.loads(body)
                    expression = params.get('expression', 0)
                    result = eval(expression)
                    jsonRes =  json.dumps({"result": result})
                    response = f"""\
HTTP/1.1 200 OK
Content-Type: application/json

{jsonRes}
"""

                # Retreive data
                case ("/students", "GET"):
                    response = get_students(token)
                case ("/finalGrades", "GET"):
                    response = get_grades(token)
                case ("/pending", "GET"):
                    response = getWaitList(token)

                ## STATIC
                ### HTML
                case ("/", "GET"):
                    response = return_home_page()
                case ("/login", "GET"):
                    response = return_login_page()
                case ("/class", "GET"):
                    response = return_class_page(token)
                case ("/grades", "GET"):
                    response = return_grades_page(token)
                case ("/waitlist", "GET"):
                    response = return_waitinglist_page(token)
                case ("/routes", "GET"):
                    response = f"""
HERE IS ALL THE ROUTES OF MY CLASS

Unauth access:
/
/login

Students only:
/class

Teacher only:
/grades
/waitlist
/accept
/deny


CSS:
/css/index.css
/css/login.css
/css/class.css"""
                ### CSS
                case ("/css/index.css", "GET"):
                    response = serve_css('css/index.css')
                case ("/css/login.css", "GET"):
                    response = serve_css('css/login.css')
                case ("/css/class.css", "GET"):
                    response = serve_css('css/class.css')
                case _:
                    response = False

### Add / deny users from class
            if(path.startswith("/accept/")):
                path_parts = path.split("/")[2]
    
                if "?" in path_parts:
        # Separate the username from the list of params
                    username, query_string = path_parts.split("?", 1)
        # Extract the CSRF token
                    query_params = parse_qs(query_string)
                    csrfTok = query_params.get("csrftok", [None])[0]  
                else:
                    username = path_parts
                    csrfTok = False

                if username and csrfTok:
                    response = addUserToClass(username, token, csrfTok)
                else:
                    response = False

            elif(path.startswith("/deny/")):
                path_parts = path.split("/")[2]
    
                if "?" in path_parts:
        
                    username, query_string = path_parts.split("?", 1)
       
                    query_params = parse_qs(query_string)
                    csrfTok = query_params.get("csrftok", [None])[0]  
                else:
                    username = path_parts
                    csrfTok = False

                if username and csrfTok:
                    response = removeUserFromWaitList(username, token, csrfTok)
                else:
                    response = False
            # Error message

            if response == False:
                response = f"""\
HTTP/1.1 1337 not cool
Content-Type: text/html

<html>
    <body>
    <div align="center">
        <h1>Error</h1>
        <p>Something went wrong and its probably your fault... Stop doing weird stuff.</p>
    </div>
    </body>
</html>
"""
 # Send the response

            connection.sendall(response.encode("utf-8"))
            connection.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    # Queue
    s.listen(5)

    print(f"My ears are open on {HOST}:{PORT}...")



    while True:
        connection, addr = s.accept()
        client_thread = threading.Thread(target=handclient, args=(connection, addr))
        client_thread.start()
            

           
